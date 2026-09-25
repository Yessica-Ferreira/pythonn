dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
ventas = [1200, 1450, 980, 1600, 1750, 2100, 1330]

total = sum(ventas)  # Calcular la suma de todas las ventas

promedio = sum(ventas) / len(ventas)  # Calcular el promedio de ventas

indice_max = ventas.index(max(ventas))  # Obtener el índice de la venta máxima

print("Total de ventas:", total)
print("Promedio de ventas:", promedio)
print("Día de la venta máxima:", dias[indice_max])


 