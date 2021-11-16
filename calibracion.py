# En este primer algoritmo sirve para convertir un numero dado en un rango establecido
# en un porcentaje del 0 al 100 en ese rango
# RANGO
# en el aire = 0%
max = 2600
# en el agua = 100%
min = 1400
# Numero
num  = 2000
# Algoritmo para convertir de electronico a porcentual
rango = max - min
recorrido = num - min 
porcentaje = (rango - recorrido)/rango
print(porcentaje)
# Algoritmo para convertir de porcentual a electronico
numero =  max - porcentaje*(max-min)
print(numero)


 

