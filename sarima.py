import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Cargar datos
df = pd.read_csv("ibex35_historico_limpio.csv", sep=';', decimal=',', encoding='utf-8', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df.index)  # Asegurarse de que el índice es datetime
print("DATOS CARGADOS CORRECTAMENTE")

# Establecemos frecuencia diaria
df = df.asfreq('D')

# Dividir en conjuntos de entrenamiento y prueba
train = df['Cierre'][:'2021-12-31']
test = df['Cierre']['2022-01-01':]
print("DATOS DIVIDIDOS CORRECTAMENTE")

# Prueba de estacionariedad y diferenciación
def verificar_estacionariedad(serie):
    resultado = adfuller(serie.dropna())
    p_valor = resultado[1]
    if p_valor < 0.05:
        print("La serie es estacionaria (p-valor:", p_valor, ")")
        return serie, 0  # Sin diferenciación
    else:
        print("La serie no es estacionaria (p-valor:", p_valor, ")")
        return serie.diff().dropna(), 1  # Aplicar diferenciación

serie_train, d = verificar_estacionariedad(train)
print("SERIE DE ENTRENAMIENTO VERIFICADA CORRECTAMENTE")

# ACF y PACF para identificar p y q
plot_acf(serie_train, lags=40)
plot_pacf(serie_train, lags=40)
plt.show()
print("ACF Y PACF GRAFICADOS CORRECTAMENTE")

# Parámetros de SARIMA
p, q, d = 3, 2, 1  # Ajusta según observaciones en ACF y PACF
P, Q, D, s = 1, 1, 1, 365  # Estacionalidad anual
print("PARÁMETROS DE SARIMA ESTABLECIDOS CORRECTAMENTE")

# Modelo SARIMA
model = SARIMAX(train, order=(p, d, q), seasonal_order=(P, D, Q, s))
sarima_fit = model.fit(disp=False)
print(sarima_fit.summary())
print("MODELO SARIMA AJUSTADO CORRECTAMENTE")

# Pronóstico y visualización
pred = sarima_fit.get_prediction(start=test.index[0], end=test.index[-1], dynamic=False)
pred_mean = pred.predicted_mean
pred_ci = pred.conf_int()

plt.figure(figsize=(10, 6))
plt.plot(train, label="Entrenamiento")
plt.plot(test, label="Prueba", color="green")
plt.plot(pred_mean, label="Pronóstico SARIMA", color="orange")
plt.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='orange', alpha=0.2)
plt.legend()
plt.show()
print("PREDICCIÓN Y VISUALIZACIÓN REALIZADAS CORRECTAMENTE")