import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller

# Cargar datos
df = pd.read_csv("ibex35_historico_limpio.csv", sep=';', decimal=',', encoding='utf-8', index_col=0)
df.index = pd.to_datetime(df.index)

# Asegurar que la frecuencia es diaria
df = df.asfreq('D')

# Verificar estacionariedad
def es_estacionaria(serie):
    resultado = adfuller(serie)
    p_valor = resultado[1]
    return p_valor < 0.05

if not es_estacionaria(df['Cierre']):
    print("La serie no es estacionaria; aplicar diferencias.")
    df['Cierre_diff'] = df['Cierre'].diff().dropna()

print("Llego hasta aqui")
# Entrenar el modelo SARIMA. asumimos estacionalidad anual
modelo = SARIMAX(df['Cierre'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 365), enforce_stationarity=False, enforce_invertibility=False)
resultado = modelo.fit(disp=False)

# Resumen del modelo
print(resultado.summary())

# Pronóstico
prediccion = resultado.get_forecast(steps=30)
pred_ci = prediccion.conf_int()

# Gráfica de pronóstico
plt.figure(figsize=(10,5))
plt.plot(df['Cierre'], label='Cierre Observado')
plt.plot(prediccion.predicted_mean, label='Pronóstico', color='red')
plt.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='pink', alpha=0.3)
plt.legend()
plt.show()


# da este error: statsmodels.tools.sm_exceptions.MissingDataError: exog contains inf or nans
# mirar variables exógenas