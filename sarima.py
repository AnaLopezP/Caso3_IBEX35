import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Leer datos limpios
df = pd.read_csv("ibex35_historico_limpio.csv", sep=';', decimal=',', encoding='utf-8', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df.index)  # Asegurarse de que el índice es datetime

# indico que el indice es diario
df = df.asfreq('D')

# Verificar estacionariedad y aplicar diferencias si es necesario
def es_estacionaria(serie):
    resultado = adfuller(serie)
    p_valor = resultado[1]
    return p_valor < 0.05

# Diferenciar la serie si no es estacionaria
if not es_estacionaria(df['Cierre']):
    df['Cierre_diff'] = df['Cierre'].diff().dropna()
    serie = df['Cierre_diff'].dropna()
    print("Aplicada diferencia para estacionariedad.")
else:
    serie = df['Cierre']
    print("La serie es estacionaria.")

# Definir los parámetros del modelo SARIMA
p, d, q = 1, 1, 1  # Cambia estos valores si tienes una mejor estimación
P, D, Q, s = 1, 1, 1, 365  # s=365 para estacionalidad anual

# Entrenar el modelo SARIMA
model = SARIMAX(serie, order=(p, d, q), seasonal_order=(P, D, Q, s))
sarima_fit = model.fit(disp=False)

# Mostrar resumen del modelo
print(sarima_fit.summary())

# Predecir y graficar
pred = sarima_fit.get_prediction(start=-365)  # Cambia este rango según tus datos
pred_ci = pred.conf_int()

plt.figure(figsize=(10, 6))
plt.plot(df['Cierre'], label="Observado")
plt.plot(pred.predicted_mean, label="Predicción SARIMA", color='orange')
plt.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='orange', alpha=0.2)
plt.legend()
plt.show()

# NO es estacionario, asi que hay que ver como hacerlo (pone estacionalidad anual)
# statsmodels.tools.sm_exceptions.MissingDataError: exog contains inf or nans