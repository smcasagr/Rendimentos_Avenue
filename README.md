# Rendimentos Avenue
 Script simples para separar os dados de dividendos do extrato BR-CSV da corretora Avenue.

 Este script é especialmente criado para quem utiliza a planilha do Douglas Lombello ([dlombello](https://www.dlombelloplanilhas.com/)) para
 o controle de investimentos, uma vez que a planilha gerada pelo script separa e ordena os dividendos de acordo com a formatação da aba "Rendimentos"
 da planlha citada.

 O funcionamento do script é simples: a partir da leitura do .CSV do extrato da conta da Avenue, é gerado
 um novo arquivo .xlsx devidamente formatado nos moldes da planilha acima citada. Assim, basta copiar os
 dados gerados pelo script e colá-los na aba de rendimentos da planilha dlombello.

Para rodar o script:
 1. Colocar o arquivo .CSV na mesma pasta onde o script.py (ou o arquivo ipynb) se encontra;
 2. Se rodar pela linha de comando:
    - ```input_file```: Caminho onde o arquivo ```*.BR-csv``` gerado pela corretora se encontra, incluíndo o nome deste arquivo.
    - ```--summarize=``` \
      ```True```: Caso queira gerar o arquivo Excel com os totalizadores no final de cada mês; \
      ```False```: Caso queira gerar o arquivo Excel sem totalizadores.
    - ```output_file```: Caminho para o diretório onde se deseja salvar o arquivo gerado pelo script, incuíndo o nome do arquivo.

Também é possível rodar via Jupyter Notebook, como consta no exemplo contido no repositório.

Obs.: Os valores do arquivo do repositório são fictícios.

---
This is a simple script to split the dividend and tax data from the BR-CSV file of the Avenue brokerage statement.

This script is intended to be used with the [dlombello](https://www.dlombelloplanilhas.com/) spreadsheet, as the output separates and orders the dividend
data in the same format as the mentioned spreadsheet.

The script is easy to understand: from the .csv file reading, the script generates a .xslx file formatted is the same 
way as dlombello spreadsheet. Thus, one only need to copy the data generated by the script and past on the "Income" tab 
of the dlombello spreadsheet.

To run the script:
 1. Place the .CSV file in the same folder where the script.py (or the ipynb file) is located;
 2. If running on command line:
    - ```input_file```: Path where the ```*.BR-csv``` file generated by the broker is located, including the name of this file.
    - ```--summarize=``` \
      ```True```: In case you want to generate the Excel file with the totalizers at the end of each month; \
      ```False```: If you want to generate the Excel file without totalizers.
    - ```output_file```: Path to the directory where one want to save the file generated by the script, including the file name.
 
It is also possible to run via Jupyter Notebook, as stated in the repository.

Note: The repository file values are fake.
