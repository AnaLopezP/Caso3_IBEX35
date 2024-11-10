import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt

# Cargar datos y preprocesar
df = pd.read_csv("ibex35_historico_limpio.csv", sep=';', decimal=',', encoding='utf-8', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df.index)
df = df.asfreq('D')
df = df[['Cierre']]

# Dividir en entrenamiento y prueba
train = df[:'2021-12-31']
test = df['2022-01-01':]

# Escalar los datos entre 0 y 1
scaler = MinMaxScaler(feature_range=(0, 1))
train_scaled = scaler.fit_transform(train)
test_scaled = scaler.transform(test)

# Función para preparar los datos en formato de secuencias
def create_sequences(data, seq_length=60):
    X, y = [], []
    for i in range(seq_length, len(data)):
        X.append(data[i-seq_length:i, 0])  # Secuencia de `seq_length` días anteriores
        y.append(data[i, 0])               # Valor objetivo siguiente
    return np.array(X), np.array(y)

# Crear secuencias de entrenamiento y prueba
seq_length = 60  # Número de días previos para predecir el siguiente día
X_train, y_train = create_sequences(train_scaled, seq_length)
X_test, y_test = create_sequences(test_scaled, seq_length)

# Reshape para LSTM (samples, time steps, features)
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

# Crear el modelo LSTM
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')

# Entrenar el modelo
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# Realizar predicciones
predicted_values = model.predict(X_test)
predicted_values = scaler.inverse_transform(predicted_values)  # Invertir escalado

# Invertir escalado para los valores de prueba
y_test_unscaled = scaler.inverse_transform(y_test.reshape(-1, 1))

# Visualizar los resultados
plt.figure(figsize=(12, 6))
plt.plot(test.index[seq_length:], y_test_unscaled, label="Valores reales")
plt.plot(test.index[seq_length:], predicted_values, label="Predicciones LSTM", color="orange")
plt.title("Predicción de IBEX 35 con LSTM")
plt.xlabel("Fecha")
plt.ylabel("Cierre")
plt.legend()
plt.show()
