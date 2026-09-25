# Cálculo de temperatura

while True:
    entrada = input("Ingrese la temperatura (0 para salir): ")

    try:
        temperatura = float(entrada)
    except ValueError:
        print("Entrada inválida. Ingrese un número.")
        continue

    if temperatura == 0:
        print("Programa finalizado.")
        break

    if temperatura >= 28:
        print("Encender aire acondicionado.")
    elif temperatura <= 18:
        print("Encender calefacción.")
    else:
        print("Temperatura agradable.")
