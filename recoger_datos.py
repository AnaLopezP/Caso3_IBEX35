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

#Ajustar el date time para que sea el formato solo YYYY-MM-DD, pasar todos los datos numericos a int o float
#Error cuadratico medio, coef de correlación y ver la predicción
#Mirar el formato de los datos y si cuadra con los de la web yahoo finance IBEX 35
#Establecer bien las columnas para que tengan sentido, cambiarles el nombre y hacerlo mejor. 