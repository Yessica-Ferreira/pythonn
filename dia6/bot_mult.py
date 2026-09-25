import random

puntaje = 0

for pregunta in range(5):
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    
    respuesta = int(input(f"Cuanto es: {num1} x {num2}? "))
    
    if respuesta == num1 * num2:
        print("¡Correcto!")
        puntaje += 1
    else:
        print("Incorrecto.")

print(f"Acertaste: {puntaje} de 5")
if(puntaje <3):
    print("Necesitas mejorar")
elif(puntaje <5):
    print("Eres bueno pero falta mejorar")
else:
    print("¡Excelente! Acertaste todas.")