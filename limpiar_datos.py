import pandas as pd


df = pd.read_csv("ibex35_historico.csv", sep=';', encoding='utf-8', skiprows=2, index_col=0)
print(df.columns)

df.index = pd.to_datetime(df.index).date

#Apdatamos el formato de las fechas
#df.index = pd.to_datetime(df.index, format= '%Y-%m-%d').date

df.rename(columns={'Unnamed: 1': 'Cierre', 
                   'Unnamed: 2': 'Cierre Ajustado',
                   'Unnamed: 3': 'Maximo',
                   'Unnamed: 4': 'Minimo', 
                   'Unnamed: 5': 'Abrir',
                   'Unnamed: 6': 'Volumen'}, inplace=True)

print(df.index)
print(df.head())

# Comprobamos si hay valores nulos
print(df.isnull().sum())
print("No hay valores nulos")

# Comprobamos si hay ceros
print(df[df['Cierre'] == 0])
print(df[df['Cierre Ajustado'] == 0])
print(df[df['Maximo'] == 0])
print(df[df['Minimo'] == 0])
print(df[df['Abrir'] == 0])
print(df[df['Volumen'] == 0])
print("En el caso del volumen hay un 0 pero hemos comprobado que no es un error")



#Ajustar el date time para que sea el formato solo YYYY-MM-DD, pasar todos los datos numericos a int o float
#Error cuadratico medio, coef de correlación y ver la predicción
#Mirar el formato de los datos y si cuadra con los de la web yahoo finance IBEX 35
#Establecer bien las columnas para que tengan sentido, cambiarles el nombre y hacerlo mejor. 