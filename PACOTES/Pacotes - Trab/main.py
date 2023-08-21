from graf import Graficos
import pandas as pd

# df = pd.read_csv('IRIS.csv')
# df['species'].replace({"Iris-setosa":1, "Iris-versicolor":2, "Iris-virginica":3}, inplace=True)
# df.to_csv('IRIS.csv')


#grafico = Graficos('testpiz.csv') 
grafico = Graficos('test.csv') 
#grafico = Graficos('testbar.csv') 

cores = ['pink','coral','purple','lightgreen','goldenrod']
labels = [r'Vendas', r'Gastos', r'Lucros',r'Aluguéis',r'Despesas']



#grafico.pizza('coluna1','Gráfico de Vendas Lanchonete UFPI',labels,cores)
#grafico.linha('coluna1','coluna2',legenda='vendas',tit='Grafico de Linha',xlabel='x',ylabel='y',label='')
#grafico.barra('coluna1','coluna2',legenda='Idade dos Dragões de House Of The Dragon',tit='Idade',xlabel='Nome dos Dragões',ylabel='Idade')
grafico.ponto('coluna1','coluna2',legenda='vendas',tit='Grafico de Ponto',xlabel='x',ylabel='y')