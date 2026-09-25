meses = (
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
)

numero_mes = int(input("Ingrese un número del 1 al 12: "))

if 1 <= numero_mes <= 12:
    print(f"El mes correspondiente es {meses[numero_mes - 1]}.")
else:
    print("Número inválido.")
