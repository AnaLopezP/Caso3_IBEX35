from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
from analisis_datos import adf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import acf, pacf
import warnings
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np


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
acf_values = acf(series_diff1, nlags=40)  
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

#d = 1, q = {1,2,3}, p = {1,2,3} (recomienda mejor 2 y 3)

# Evaluamos el modelo ARIMA con distintos valores de p y q

warnings.filterwarnings("ignore")  # Ignorar advertencias para facilitar la búsqueda

best_aic = float("inf")
best_order = None
best_model = None

for p in range(1, 4):  # Cambia los límites si deseas probar más valores
    for q in range(1, 4):
        try:
            model = ARIMA(train, order=(p, d, q))
            fitted_model = model.fit()
            if fitted_model.aic < best_aic:
                best_aic = fitted_model.aic
                best_order = (p, d, q) #(3,1,2) mejores valores
                best_model = fitted_model
        except Exception as e:
            continue

print(f"Mejor orden encontrado: {best_order} con AIC: {best_aic}")



# Predicciones
steps = len(test)
predictions = best_model.forecast(steps=steps)

# Métricas de evaluación
mae = mean_absolute_error(test, predictions)
rmse = np.sqrt(mean_squared_error(test, predictions))
print(f"MAE: {mae}")
print(f"RMSE: {rmse}")

# Gráfico de las predicciones
plt.figure(figsize=(12, 6))
plt.plot(train, label="Entrenamiento")
plt.plot(test, label="Prueba", color="orange")
plt.plot(test.index, predictions, label="Predicciones", color="green")
plt.legend()
plt.show()
plt.savefig('imgs/prediccion_vs_real_arima.png')

#Miramos residuos
residuals = best_model.resid
plot_acf(residuals, lags=40)
plt.title("ACF de los residuos")
plt.show()
plt.savefig('imgs/acf_residuos_arima.png')