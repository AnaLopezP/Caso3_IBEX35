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



