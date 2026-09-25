numeros = []

for posicion in range(5):
    numero = float(input(f"Ingrese el número {posicion + 1}: "))
    numeros.append(numero)

print("Lista de números:", numeros)
print("Suma de los números:", sum(numeros))
