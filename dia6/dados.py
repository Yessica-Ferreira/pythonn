import random
import time

intentos = 0
historial = []

while True:
    intentos += 1

    print("\nLanzando los dados...")
    time.sleep(1)

    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    historial.append((dado1, dado2))

    print(f"Intento {intentos}: {dado1} - {dado2}")

    if dado1 == dado2:
        print(f"¡Has sacado un doble en {intentos} intentos!")
        break

    print("No es un doble. Tirando nuevamente...")
    time.sleep(1)

print("Historial:", historial)