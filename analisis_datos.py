import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose

df = pd.read_csv("ibex35_historico_limpio.csv", sep=';', decimal=',', encoding='utf-8', index_col=0)

# Aplicar la descomposición a cada columna
for column in df.columns:
    decomposition = seasonal_decompose(df[column], model='additive', period=7)
    
    # Graficar los componentes para cada columna
    fig, axes = plt.subplots(4, 1, sharex=True, figsize=(10, 8))
    fig.suptitle(f'Descomposición de la Serie Temporal: {column}')
    
    decomposition.observed.plot(ax=axes[0], title='Observado')
    decomposition.trend.plot(ax=axes[1], title='Tendencia')
    decomposition.seasonal.plot(ax=axes[2], title='Estacionalidad')
    decomposition.resid.plot(ax=axes[3], title='Residuo')
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()