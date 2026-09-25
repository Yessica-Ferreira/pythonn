from controller import ControladorTraduccion

def main():
    controlador = ControladorTraduccion()

    while True:
        print("\n--- TRADUCTOR ---")
        print("1. Cargar palabra")
        print("2. Traducir")
        print("3. Salir")

        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            espanol = input("Escribe la palabra en español: ").strip()
            ingles = input("Escribe la traducción en inglés: ").strip()

            controlador.cargar_palabra(espanol, ingles)
            print("Palabra cargada correctamente.")

        elif opcion == "2":
            espanol = input("Escribe la palabra que deseas traducir: ").strip()
            resultado = controlador.traducir(espanol)

            if resultado is not None:
                print(f"Traducción: {resultado}")
            else:
                print("No se encontró la palabra.")

        elif opcion == "3":
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
