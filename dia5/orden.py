# ordenamiento burbuja

precios = [5, 2 , 9, 1, 5, 6]
print("Precios antes del ordenamiento:", precios)
n = len(precios)
for i in range(n - 1):
    for j in range(n - i - 1):
        if precios[j] < precios[j + 1]:
            aux = precios[j]
            precios[j] = precios[j + 1]
            precios[j + 1] = aux
print("Precios después del ordenamiento:", precios)
