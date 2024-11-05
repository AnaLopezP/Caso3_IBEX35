from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
from analisis_datos import adf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf, pacf

#cargamos los datos
df = pd.read_csv("ibex35_historico_limpio.csv", sep=';', decimal=',', encoding='utf-8', index_col=0)

#dividimos los datos en train y test
train = df['Cierre'][:'2021-12-31']
test = df['Cierre']['2022-01-01':]

#Modelo ARIMA

# Prueba inicial
if not adf(df):
    # Diferenciación de primer orden
    series_diff1 = df['Cierre'].diff().dropna()
    if adf(series_diff1):
        d = 1
    else:
        # Si es necesario, diferenciación de segundo orden
        series_diff2 = series_diff1.diff().dropna()
        if adf(pd.DataFrame(series_diff2, columns=['Cierre'])):
            d = 2
else:
    d = 0  # Ya es estacionaria

print(f"Valor seleccionado para d: {d}")

# Pasamos a una serie unidimensional
series_diff1 = series_diff1.squeeze() if d > 0 else df['Cierre']

# Calcular valores ACF y PACF
acf_values = acf(series_diff1, nlags=40)   # Cambia nlags según necesites
pacf_values = pacf(series_diff1, nlags=40)

# Imprimir los valores
print("Valores de ACF:")
print(acf_values)
print("\nValores de PACF:")
print(pacf_values)

# Gráficos de ACF y PACF en la serie diferenciada (si d > 0)
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
plot_acf(series_diff1, lags=40, ax=axes[0])
plot_pacf(series_diff1, lags=40, ax=axes[1])
plt.show()



'''
model = ARIMA(series, order=(p, d, q))
fitted_model = model.fit()
predictions = fitted_model.forecast(steps=12)'''