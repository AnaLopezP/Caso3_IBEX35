import pandas as pd


df = pd.read_csv("ibex35_historico.csv", sep=';', decimal=',', encoding='utf-8', skiprows=2, index_col=0)
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

df.index.name = 'Fecha'
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

#Comprobamos el tipo de los valores
print(df.dtypes)

#Redondeamos los valores a dos decimales
df = df.round(2)
print(df.head())

#exportamos el dataframe
df.to_csv('ibex35_historico_limpio.csv', sep=';', decimal=',', encoding='utf-8')

# Normalizamos los datos para mejorar la eficiencia del modelo
df = (df - df.mean()) / df.std()
print(df.head())
print(df.tail())

#Ajustar el date time para que sea el formato solo YYYY-MM-DD, pasar todos los datos numericos a int o float HECHO
#Error cuadratico medio, coef de correlación y ver la predicción HECHO
#Mirar el formato de los datos y si cuadra con los de la web yahoo finance IBEX 35 HECHO
#Establecer bien las columnas para que tengan sentido, cambiarles el nombre y hacerlo mejor. HECHO

#----------------PANDEMIA ---------------------

# Define el rango de fechas a excluir
inicio_pandemia = pd.to_datetime("2020-03-01")
fin_pandemia = pd.to_datetime("2021-03-31")

# estraer el índice
df = df.reset_index()
df['Fecha'] = pd.to_datetime(df['Fecha'])

print(df.columns)

# Filtra el DataFrame excluyendo las fechas dentro del rango de la pandemia
df_filtrado = df[(df['Fecha'] < inicio_pandemia) | (df['Fecha'] > fin_pandemia)]

df_filtrado.set_index('Fecha', inplace=True)

print(df_filtrado.loc['2020-02-27':'2021-04-02'])

#Exportamos el nuevo dataframe
df_filtrado.to_csv('ibex35_historico_limpio_sin_pandemia.csv', sep=';', decimal=',', encoding='utf-8')

