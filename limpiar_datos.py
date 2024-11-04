import pandas as pd


df = pd.read_csv("ibex35_historico.csv", sep=';', decimal= ',', encoding='utf-8')
print(df.columns)
#Apdatamos el formato de las fechas
df.index = pd.to_datetime(df.index, format= '%Y-%m-%d')
print(df.index)

#Ajustar el date time para que sea el formato solo YYYY-MM-DD, pasar todos los datos numericos a int o float
#Error cuadratico medio, coef de correlación y ver la predicción
#Mirar el formato de los datos y si cuadra con los de la web yahoo finance IBEX 35
#Establecer bien las columnas para que tengan sentido, cambiarles el nombre y hacerlo mejor. 