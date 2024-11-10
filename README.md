# Caso3_IBEX35

## TENDENCIA
Tendencia ascendende pero muy hardcore
Tenemos dos boquetes (ver fecha exacta y el por qué) y un medio boquete que parece una bajada normal
Las fechas exactas de los dos boqueten son:
(Hay que tener en cuenta que hemos cogido los valores más bajos, pero la bajada puede abarcar más periodo de tiempo)
### Boquete 1
Del 18/09/2012 - 06/02/2013 
El bajo valor en el IBEX 35 alrededor de 2012-2013 se debe principalmente a la crisis financiera en Europa, que fue particularmente dura para España. Durante ese periodo, varios países europeos, incluyendo España, enfrentaron serios problemas económicos debido a la crisis de deuda soberana en la eurozona, que comenzó en 2009 y alcanzó uno de sus puntos más críticos alrededor de 2012.
### Boquete 2 (pandemia)
Del 08/06/2020 - 13/01/2021
sabemos que la razón es la pandemia, que empezó en marzo de 2020.
## ESTACIONALIDAD
Tenemos que ver cada cuanto se repite (osea aislar el ciclo)
Como están muy marcados, pordemos decir que es una estacionalidad fuerte (depende de estaciones) pero lo veremos cuando aislemos el ciclo.
Factor estacional confiable

## RESIDUO
Vemos que el residuo es irregular y suele estar cerca del 0, eso quiere decir que está gucci (obviando la pandemia)

## Prueba de Dickey-Fuller Aumentada (ADF) 
Es una prueba para ver si la serie es estacionaria. Lo que hace es evaluar si una serie tiene una raíz  unitaria (p_valor), lo que sugiere que es no estacionaria.

Si el p-valor es menor que 0.05, se rechaza la hipótesis nula (que tiene raíz unitaria) y la serie es estacionaria. En caso contrario se acepta y la serie no es estacionaria.

## Prueba de Mann-Kendall 
Es para ver si hay tendencia. Un valor de p bajo (p < 0.05) sugiere una tendencia significativa.
La dirección de la tendencia se determina mediante el signo de la estadística de prueba.

# MODELOS
## ARIMA
Series temporales estacionarias. Sin tendencia, o estacionalidad marcada. 
### Preparación:
- Estacionaria pero no mucho
- p: orden autorregresion (AR). grafo autocorrelación parcial (PACF). Ver PACF, ver en que punto se corta (p), cuándo los valores caen a cero o cerca de cero
- d: orden diferenciacion (d = 1 o 2). Se mira con prueba de Dickey-Fuller Aumentada (ADF), si p > 0.05 --> diferenciando la serie una vez y vuelve a realizar la prueba de estacionaridad. Si después de una diferenciación la serie se vuelve estacionaria, entonces d = 1. Si no otra vez. (d = 2)
- q: orden media movil (MA). usar grafico autocorrelacion para elegirlo. Ver ACF, el punto de corte (q)

AFC (q): 
Valores Positivos: Indican que hay una correlación positiva entre la serie y su valor retrasado. Por ejemplo, un valor de 0.014 en el lag 1 sugiere que hay una ligera tendencia positiva en la serie a corto plazo.

Valores Negativos: Indican una correlación negativa. Por ejemplo, en el lag 4, el valor -0.020 sugiere que cuando el valor en t−4 es alto, el valor actual t tiende a ser bajo, y viceversa.

Valores Cercanos a Cero: Indican que no hay correlación significativa entre la serie y sus retardos en esos lags. Por ejemplo, los valores como 0.001 y -0.031 son muy cercanos a cero, lo que sugiere que no hay una relación significativa entre esos valores.
Lag 1 a 5: Los valores son relativamente pequeños (entre 0.014 y -0.028). Esto sugiere que la autocorrelación es débil en estos lags.
Lag 6 a 10: Vemos un ligero aumento y disminución, pero aún no hay picos significativos.
Lag 11 y más: Los valores siguen siendo pequeños y algunos negativos. La mayoría está cerca de cero.

Recomendación (q):
Dado que los valores de ACF no muestran una caída abrupta en los primeros lags, podría ser que el modelo no necesite muchos términos de media móvil, o que incluso necesites explorar modelos más complejos si es que hay un comportamiento más subyacente que no se capta con un q bajo. 
Comienza con un q=1 y prueba el modelo.
Evalúa el rendimiento y observa si hay patrones significativos en los residuos.
Prueba valores mayores si notas que el modelo no captura bien la serie.

AIC
El AIC (Criterio de Información de Akaike, por sus siglas en inglés: Akaike Information Criterion) es una métrica que se usa para evaluar la calidad de modelos estadísticos, especialmente útil para comparar modelos con diferentes números de parámetros, como los modelos ARIMA.

Menor AIC indica un mejor ajuste relativo. Cuanto más bajo sea el valor de AIC, mejor equilibrio tiene el modelo entre ajuste y complejidad.

Evaluar residuos
Para asegurarte de que el modelo captura bien la serie, verifica que los residuos del modelo no tengan patrones claros y sean aproximadamente ruido blanco.

Conclusiones
Todos los rezagos de la ACF de los residuos, excepto el 0, están dentro de la banda de confianza, y
No se observan patrones significativos en los residuos,
esto sugiere que el modelo (3,1,2) es adecuado y ha logrado capturar bien la dinámica de la serie.

## SARIMA
Tiene los mismos parámetros que el ARIMA, además de 
P,D,Q,s: para el componente estacional.
P: orden estacional autorregresivo (SAR).
D: número de diferencias estacionales.
Q: orden estacional de media móvil (SMA).
s: periodo estacional (por ejemplo, 12 para datos mensuales o 365 para datos diarios si hay estacionalidad anual).

Conclusión: descartamos completamente esta opción debido a problemas al converger. 




