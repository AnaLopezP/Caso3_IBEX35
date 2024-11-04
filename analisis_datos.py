import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

#Alditiva o multiplicativa

df = pd.read_csv("ibex35_historico_limpio.csv", sep=';', decimal=',', encoding='utf-8', index_col=0)

# Aplicar la descomposición a cada columna

decomposition = seasonal_decompose(df['Cierre'], model='additive', period=90)

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
fig.savefig('ibex35_hist_tend_observ.png')
fig1.savefig('ibex35_hist_estacional_residuo.png')
