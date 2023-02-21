import sys
import pandas as pd
import fire

class ReadAvenueCSV():

    def __init__(self, input_file, summarizer=False):
        """
        When creating the object, it is necessary to pass the csv file generated by Avenue.
        
        Important to note that the CSV file to be generated by the Avenue Report must be the
        "BR.csv" format.

        Parameters
        =======
        input_file : string
            Path, with the file name, where the .csv file is located;
            Or the .csv file name, if the file is located in the same folder of the .py script

        summarizer : bool
            True - Summarize totals at the end of each month
            False - Generates the output file without the summarizer
        """
        try:            
            self.df_input_file = pd.read_csv(input_file, sep=';', parse_dates=True)
            self.summarizer = summarizer
            
            self.__clean_report_file(self.df_input_file)
            self.df_sheet = self.__create_df_sheet(self.df_input_file)
        except FileNotFoundError:
            self.df_input_file = False
            print(f"Arquivo {input_file} Inexistente")

    def generate_file(self, output_file_name='proventos_avenue'):
        """
        Convert the dataframe with the formatted data into a CSV file.

        Parameters
        =======
        file_name : string
            Name of the file that will be generated - by default, the name will be "proventos_avenue"
        """
        self.df_sheet.to_excel(output_file_name.split(".")[0] + '.xlsx')

    def __clean_report_file(self, df):
        """
        Delete unused columns and rename the remaining columns with the same name used by the dlombello spreadsheet.

        Parameters
        =======
        df : DataFrame
            Dataframe containing the loaded .csv data.
        """
        df.drop(columns='Hora', inplace=True)
        df.rename(columns={'Valor (U$)': 'Valor', 'Saldo da conta (U$)': 'Saldo'}, inplace=True)        
        df.set_index('Data', inplace=True)

    def __read_dividends(self, df_input_file):
        """
        Read the dataframe containing the CSV data and extract the rows that contain the dividends.

        Parameters
        ========
        df_input_file : DataFrame
            Dataframe with the loaded CSV data.

        Output
        =======
        df_dividends : DataFrame
            Formatted the dataframe containing information about dividends, including the payer and 
            the amount paid.
        """
        dividend_rows = df_input_file[(df_input_file['Descrição'].str.contains('Dividendos')) & (~df_input_file['Descrição'].str.contains('Impostos'))]
        dividend_data = []

        for i, row in dividend_rows.iterrows():
            ticker = row['Descrição'][row['Descrição'].index(" ")+1:row['Descrição'].index(".")]
            date = row['Liquidação']
            event = 'DIVIDENDO'
            gross_value = row['Valor']

            dividend_data.append({
                'ativo': ticker,
                'data': date,
                'evento': event,
                'valorBruto': gross_value
            })
        
        df_dividends = pd.DataFrame(dividend_data)
        df_dividends.set_index('data', inplace=True)

        return df_dividends

    def __read_taxes(self, df_input_file):
        """
        Read the dataframe containing the CSV data and extract the rows that contain the dividend taxes paid.

        Parameters
        ========
        df_input_file : DataFrame
            Dataframe with the loaded CSV data.

        Output
        =======
        df_taxes : DataFrame
            Formatted the dataframe containing information about dividend taxes.
        """
        taxes_rows = df_input_file[df_input_file['Descrição'].str.contains('Impostos')]
        tax_data = []
        
        for i, row in taxes_rows.iterrows():
            ticker = row['Descrição'][row['Descrição'].index("dos")+4:row['Descrição'].index(".")]
            date = row['Liquidação']
            tax = row['Valor']
            broker = 'AVENUE'
            currency = 'USD'
            irrf = 0.0
            
            tax_data.append({
                'data': date,
                'ativo': ticker,
                'imposto': tax,
                'corretora': broker,
                'moeda': currency,
                'irrf': irrf})
        
        df_taxes = pd.DataFrame(tax_data)
        df_taxes.set_index('data', inplace=True)

        return df_taxes

    def __create_df_sheet(self, df_input_file):
        """
        This function performs the merge of the dataframes containing the extracted data of dividends and taxes, 
        and formats it in the same shape as utilized by the dlombello spreadsheet

        Parameters
        ========
        df_input_file : DataFrame
            Dataframe with the loaded CSV data.

        Output
        =======
        df_sheet : DataFrame
            Merged and formatted dataframe containing the extracted dividend e taxes data.

        """

        cols_sheet = ['ativo', 'date', 'evento', 'valorLiq', 'irrf',  'moeda', 'corretora']
        
        df_sheet = pd.DataFrame(columns=cols_sheet)

        df_dividends = self.__read_dividends(df_input_file)
        df_taxes = self.__read_taxes(df_input_file)
        
        df_merged = pd.merge(df_dividends, df_taxes, on=['data', 'ativo'], how='left')
        
        df_sheet = df_merged.copy()
        df_sheet.reset_index(inplace=True)
        
        df_sheet['valorLiq'] = df_sheet['valorBruto'] + df_sheet['imposto']
        df_sheet.loc[df_sheet['valorLiq'].isnull(), 'valorLiq'] = df_sheet['valorBruto']

        df_sheet = self.__format_type_dfsheet(df_sheet)

        if self.summarizer:
            df_sheet = self.__create_summarizer(df_sheet)

        return df_sheet

    def __create_summarizer(self, df_sheet):
        """
        Create the totalizers at the end of each month

        Parameters
        =======
        df_sheet : DataFrame
            The formatted dataframe that contains the data about dividends and taxes.

        Output
        =======
        df_sheet : DataFrame
            The formatted dataframe with the summarizers at the end of each month.

        """
        frame = df_sheet.reset_index()\
                        .groupby('mes', as_index=False)\
                        .agg({
                            'valorLiq': 'sum',
                            'valorBruto': 'sum',
                            'imposto': 'sum',
                            'mes': 'max',
                            'index': 'max'
                        }, ignore_index=True)\
                        .assign(evento='TOTAL').set_index('index')
        
        df_sheet = pd.concat([df_sheet, frame]).sort_index(ignore_index=True)
        df_sheet.drop(columns='mes', inplace=True)

        return df_sheet

    def __format_type_dfsheet(self, df_formatted):
        """
        Auxiliary function used to create an additional column, which contains the month of each entry row.

        Parameters
        =======
        df : DataFrame
            Merged and formatted dataframe containing the extracted dividend e taxes data.

        df_sheet : DataFrame
            Merged and formatted dataframe containing the auxiliary column.
        """
        df_sheet = df_formatted[['ativo', 'data', 'evento', 'valorLiq', 'irrf', 'moeda', 'corretora', 'valorBruto', 'imposto']]

        df_sheet = df_sheet.assign(mes=pd.to_datetime(df_sheet['data'], format='%d/%m/%Y').dt.to_period("M"))
        
        return df_sheet

    def extract(self, input_file, summarize, output_file):
        """
        The function extracts the data from an input file, parse to the dlombello's spreadsheet format, and generate an Excel output file.

        Parameters
        =======
        input_file : string
            Path, with the file name, where the .csv file is located;
            Or the .csv file name, if the file is located in the same folder of the .py script
        
        summarize : bool
            True - Summarize totals at the end of each month
            False - Generates the output file without the summarizer

        output_file : string
            Path, with the file name, where the formatted Excel file will be saved.
            It is important to note that the file extension will be automatically placed be the script. 
        """
        obj = ReadAvenueCSV(input_file=input_file, summarizer=summarize)
        obj.generate_file(output_file_name=output_file)        

def main():
    fire.Fire(ReadAvenueCSV.extract)

if __name__ == "__main__":
    main()    
