import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt


# Cargar y escalar los datos
df = pd.read_csv("ibex35_historico_limpio.csv", sep=';', decimal=',', encoding='utf-8', index_col=0)
data = df['Cierre'].values.reshape(-1, 1)

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Dividir en entrenamiento y prueba (80% para entrenamiento)
train_data_len = int(np.ceil(len(scaled_data) * .8))
train_data = scaled_data[0:train_data_len,:]
val_data = scaled_data[train_data_len-60:,:]

''''
Error cuadrático medio: 121.7012923207298
Error absoluto medio: 97.40514243521342
Error absoluto porcentual medio: 1.0379286622469546


'''


#dividir los datos en conjuntos de entrenamiento y prueba
x_train = []
y_train = []
x_val = []
y_val = []

for i in range(60,len(train_data)):
    x_train.append(train_data[i-60:i,0])
    y_train.append(train_data[i,0])

for i in range(60,len(val_data)):
    x_val.append(val_data[i-60:i,0])
    y_val.append(val_data[i,0])

# Convertir a numpy arrays
x_train, y_train = np.array(x_train), np.array(y_train)
x_val, y_val = np.array(x_val), np.array(y_val)

# Redimensionar los datos
x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1)) #0 num muestras y 1 num pasos de cada muestra (60)
x_val = np.reshape(x_val, (x_val.shape[0],x_val.shape[1],1))

# Definir el modelo LSTM
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(64, return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=25)) 
model.add(Dense(units=1)) 

# Compilar el modelo
model.compile(optimizer='adam', loss='mean_squared_error')


# Entrenar el modelo
history = model.fit(x_train, y_train, epochs=20, batch_size=32, validation_data=(x_val, y_val))

# Graficar la pérdida
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.title('Pérdida del modelo')
plt.legend()
plt.savefig('imgs/perdida_modelo_lstm.png')
plt.show()


# Predecir los precios
predictions = model.predict(x_val)
predictions = scaler.inverse_transform(predictions)

# Desescala los valores de y_val para los cálculos de métricas y errores
y_val_unscaled = scaler.inverse_transform(y_val.reshape(-1, 1))


# Calcular el intervalo de confianza
errors = predictions - scaler.inverse_transform(y_val.reshape(-1, 1))
std_dev = np.std(errors)

'''# Intervalo de confianza del 68%
confidence_68 = std_dev * 1
upper_bound_68 = predictions + confidence_68
lower_bound_68 = predictions - confidence_68
print('Intervalo de confianza del 68%:', confidence_68)
'''
# Intervalo de confianza del 70%
confidence_70 = std_dev * 1.5
upper_bound_70 = predictions + confidence_70
lower_bound_70 = predictions - confidence_70
print('Intervalo de confianza del 73%:', confidence_70)

# Calcular métricas con valores desescalados
rmse = np.sqrt(np.mean((predictions - y_val_unscaled) ** 2))
print('Error cuadrático medio:', rmse)

mae = np.mean(np.abs(predictions - y_val_unscaled))
print('Error absoluto medio:', mae)

mape = np.mean(np.abs(predictions - y_val_unscaled) / np.abs(y_val_unscaled)) * 100
print('Error absoluto porcentual medio:', mape)

# Crear el DataFrame de validación con los valores reales y predicciones
val_index = df.index[train_data_len:]  # Índices correspondientes a los datos de validación
valid = pd.DataFrame(data={'Cierre': y_val_unscaled.flatten()}, index=val_index)
valid['Predictions'] = predictions.flatten()
valid['Upper Bound 73'] = upper_bound_70.flatten()
valid['Lower Bound 73'] = lower_bound_70.flatten()

# Graficar resultados con el nuevo intervalo de confianza
plt.figure(figsize=(16, 8))
plt.plot(valid['Cierre'], label='Real')
plt.plot(valid['Predictions'], label='Predicciones')
plt.fill_between(valid.index, lower_bound_70.flatten(), upper_bound_70.flatten(), color='red', alpha=0.2, label='Intervalo de Confianza 70%')
plt.title('Modelo LSTM con Intervalo de Confianza')
plt.xlabel('Fecha')
plt.ylabel('Cierre')
plt.legend()
plt.show()



