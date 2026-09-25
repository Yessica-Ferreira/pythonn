# programa para calcular IMC 
print("Calculadora de IMC")
peso = float(input("Digite su peso (kg): "))
estatura = float(input("Digite su estatura (m): "))

imc = peso / (estatura * estatura)

print("Su IMC es: ", str(imc))
