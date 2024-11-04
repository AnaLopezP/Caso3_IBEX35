#Installar yfinance

import yfinance as yf
import pandas as pd

#Definir el símbolo de IBEX 35
symbol = "^IBEX"

#Descargar datos históricos desde 2012-01-01 hasta hoy
data = yf.download(symbol, start="2012-01-01", end=pd.Timestamp.today())

#Mostrar los primeros registros
print(data.head())

#Guardar los datos en un archivo CSV
data.to_csv("ibex35_historico.csv", sep=';', decimal= ',', encoding='utf-8')
