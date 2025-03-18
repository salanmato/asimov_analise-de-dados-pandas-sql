import pandas as pd

# Perguntas
## 1. Carregue os conjuntos de dados em dois DataFrames diferentes e combine-os em um único DataFrame
df_gasolina_2000 = pd.read_csv('gasolina_2000+.csv')
df_gasolina_2010 = pd.read_csv('gasolina_2010+.csv')


df_gasolina = pd.concat([df_gasolina_2000, df_gasolina_2010], ignore_index=True) 
df_gasolina = df_gasolina.drop(columns={'Unnamed: 0': 'Index_Original'}) # removendo o index
df_gasolina

## 2. Investigue as colunas e entenda o conjunto de dados usando o head() e info()

df_gasolina.head() # analisando as primeiras linhas

df_gasolina.info() #analisando as colunas e seus tipos.

## 3. Selecione a terceira entrada da coluna DATA INICIAL e verifique seu tipo
terceira_entrada = df_gasolina.loc[2] # o dataframe começa no index 0
terceira_entrada

## 4. Utilizando o método pd.to_datetime(), converta as colunas DATA INICIAL e DATA FINAL para Timestamp / Datetime
df_gasolina['DATA INICIAL'] = pd.to_datetime(df_gasolina['DATA INICIAL'])
df_gasolina['DATA FINAL'] = pd.to_datetime(df_gasolina['DATA FINAL'])

## 5. Crie uma nova coluna para representar mês e ano mm-aaaa, utilizando a coluna DATA FINAL como referência
df_gasolina['MÊS-ANO'] = df_gasolina['DATA FINAL'].dt.strftime('%m-%Y')

## 6. Utilizano o value_counts(), liste todos os tipos de produtos contidos na base de dados.
df_gasolina['PRODUTO'].value_counts()

## 7. Filtre o DataFrame para obter apenas dados da 'GASOLINA COMUM'. Grave em uma nova variável.
df_gasolina[(df_gasolina['PRODUTO'] == 'GASOLINA COMUM')]

## 8. Qual o preço médio de revenda da gasolina em agosto de 2008?
df_gasolina_ago_2008 = df_gasolina[(df_gasolina['MÊS-ANO'] == '08-2008') & (df_gasolina['PRODUTO'] == 'GASOLINA COMUM')]
df_gasolina_ago_2008_gasolina = df_gasolina_ago_2008[['PREÇO MÉDIO REVENDA']].mean()
df_gasolina_ago_2008_gasolina

## 9. Qual o preço médio de revenda da gasolina em maio de 2014 em São Paulo?
df_gasolina_mai_2014 = df_gasolina[(df_gasolina['MÊS-ANO'] == '05-2014') & (df_gasolina['ESTADO'] == 'SAO PAULO') & (df_gasolina['PRODUTO'] == 'GASOLINA COMUM')]
df_gasolina_mai_2014_gasolina = df_gasolina_mai_2014[['PREÇO MÉDIO REVENDA']].mean()
df_gasolina_mai_2014_gasolina

## 10. Você consegue descobrir em quais estados a gasolina ultrapassou a barreira dos R$5.00? E quando isso ocorreu?
df_gasolina_maior_q_5 = df_gasolina[(df_gasolina['PRODUTO'] == 'GASOLINA COMUM') & (df_gasolina['PREÇO MÉDIO REVENDA'] > 5)]
df_gasolina_maior_q_5[['PRODUTO', 'ESTADO', 'PREÇO MÉDIO REVENDA', 'MÊS-ANO']] # só com mês e ano
df_gasolina_maior_q_5[['PRODUTO', 'ESTADO', 'PREÇO MÉDIO REVENDA', 'DATA INICIAL', 'DATA FINAL']] # com datas iniciais e finais


## 11. Qual a média de preço dos estados da região sul em 2012?
# supondo que ainda seja o preço de revenda
df_gasolina_sul_2012 = df_gasolina[(df_gasolina['DATA FINAL'].dt.year == 2012) & (df_gasolina['REGIÃO'] == 'SUL')  & (df_gasolina['PRODUTO'] == 'GASOLINA COMUM')]
df_gasolina_sul_2012_gasolina = df_gasolina_sul_2012[['PREÇO MÉDIO REVENDA']].mean()
df_gasolina_sul_2012_gasolina

## 12. Você consegue obter uma tabela contendo a variação percentual ano a ano para o estado do Rio de Janeiro?
df_gasolina_rj = df_gasolina[df_gasolina['ESTADO'] == 'RIO DE JANEIRO']
df_gasolina_rj['ANO'] = df_gasolina_rj['DATA FINAL'].dt.year
df_anual = df_gasolina_rj.groupby('ANO')['PREÇO MÉDIO REVENDA'].mean().reset_index() # fiz com valor médio
df_anual = df_gasolina_rj.groupby('ANO')['PREÇO MÉDIO REVENDA'].last().reset_index() # solução com o último valor
df_anual['PREÇO MÉDIO REVENDA'] = round(df_anual['PREÇO MÉDIO REVENDA'],2)
df_anual['VARIAÇÃO ABSOLUTA'] = df_anual['PREÇO MÉDIO REVENDA'].diff()
df_anual['VARIAÇÃO PERCENTUAL'] = round((df_anual['PREÇO MÉDIO REVENDA'].pct_change()) * 100, 2)
df_anual


## Desafio: Crie uma tabela contendo uma série temporal com a diferença absoluta 
## e percentual entre os valores mais baratos e caros.
## Apresente também ao lado os estados na qual os maiores e menores preços foram registrados.

tabela_agrupada = df_gasolina.groupby(df_gasolina['DATA FINAL'].dt.year).agg(
    preco_min = ('PREÇO MÉDIO REVENDA', 'min'),
    estado_preco_min = ('ESTADO', lambda x: x[df_gasolina.loc[x.index, 'PREÇO MÉDIO REVENDA'].idxmin()]),
    preco_max = ('PREÇO MÉDIO REVENDA', 'max'),
    estado_preco_max = ('ESTADO', lambda x: x[df_gasolina.loc[x.index, 'PREÇO MÉDIO REVENDA'].idxmax()]),
).reset_index()

tabela_agrupada['DIFERENÇA ABSOLUTA'] = tabela_agrupada['preco_max'] - tabela_agrupada['preco_min']
tabela_agrupada['DIFERENÇA PERCENTUAL'] = round(((tabela_agrupada['preco_max'] - tabela_agrupada['preco_min']) * 100),2) # round pra quebrar as vírgulas


# não entendi muito bem as funções, algum dia eu reviso.
tabela_agrupada