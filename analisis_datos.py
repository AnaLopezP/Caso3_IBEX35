import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

#Alditiva o multiplicativa

df = pd.read_csv("ibex35_historico_limpio.csv", sep=';', decimal=',', encoding='utf-8', index_col=0)

# Aplicar la descomposición a cada columna

decomposition = seasonal_decompose(df['Cierre'], model='additive', period=365)

# Graficar los componentes (Observado, Tendencia)
fig, axes = plt.subplots(2, 1, sharex=True, figsize=(10, 5))
fig.suptitle(f'Descomposición de la Serie Temporal: Cierre')

decomposition.observed.plot(ax=axes[0], title='Observado')
decomposition.trend.plot(ax=axes[1], title='Tendencia')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

# Graficar los componentes (Estacionalidad, Residuo)
fig1, axes = plt.subplots(2, 1, sharex=True, figsize=(10, 5))
fig1.suptitle(f'Descomposición de la Serie Temporal: Cierre')

decomposition.seasonal.plot(ax=axes[0], title='Estacionalidad')
decomposition.resid.plot(ax=axes[1], title='Residuo')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()

#Guardamos las gráficas
fig.savefig('imgs/ibex35_hist_tend_observ.png')
fig1.savefig('imgs/ibex35_hist_estacional_residuo.png')

#Ver lógica de la curva de tendencia y estacionalidad
'''
Bajada en 2012 --> Mirar
Maximo finales 2014 principios 2015

Calcular ciclos (estacionario) --> analizar picos
Ver residuos
indicar tendencia
¿Es estacionario? --> Ver si vale para el modelo o no
Dividir por fechas, ej: 2023-2024 y ver así más en concreto

'''

#Ver maximos y minimos

# Sacamos las filas que tienen un cierre alrededor de 8000
tendencia = decomposition.trend
print(tendencia[tendencia < 8000])


# saco las fechas de todas las filas entre estos valores
a = tendencia[tendencia < 8000].index
for i in a:
    print(i)
# print(df[ 7500 > df['Cierre'] > 8500])
