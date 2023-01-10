# Rendimentos_Avenue
 Script simples para separar os dados de dividendos do extrato BR-CSV da corretora Avenue.

 Este script é especialmente criado para quem utiliza a planilha do Douglas Lombello (dlombello) para
 o controle de investimentos.

 O funcionamento do script é simples: a partir da leitura do .CSV do extrato da conta da Avenue, é gerado
 um novo arquivo .xlsx devidamente formatado nos moldes da planilha acima citada. Assim, basta copiar os
 dados gerados pelo script e colá-los na aba de rendimentos da planilha.

Para rodar o script:
    * colocar o arquivo .CSV na mesma pasta onde o script.py se encontra;
    * na command line: python rendimentos.py nome_do_arquivo_csv true_false_sumarizador nome_output_file

Também é possível rodar via Jupyter Notebook, como consta no repositório.

 Obs.: Os valores do arquivo do repositório são fictícios.
