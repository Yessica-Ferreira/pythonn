# Calculo de Ecuacion Cuadratica
print("Calculo de Ecuacion Cuadratica")
a = float(input("ingrese el coeficiente de x^2: "))
b = float(input("ingrese el coeficiente de x: "))
c = float(input("ingrese el termino independiente: "))

x1 = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
x2 = (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)

print("Las soluciones de la ecuacion son: ", str(x1), "y", str(x2))