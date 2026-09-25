import os

import google.generativeai as genai


api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Error: falta configurar la variable GEMINI_API_KEY.")
    raise SystemExit

genai.configure(api_key=api_key)
modelo = genai.GenerativeModel("gemini-3.6-flash")


class Chatbot:
    def __init__(self, nombre):
        self.nombre = nombre
        self.base_conocimiento = {
            "hola": "¡Hola! ¿En qué puedo ayudarte?",
            "adios": "¡Hasta luego, que tengas un buen día!",
            "como estas": "Estoy funcionando correctamente.",
            "quien eres": "Soy un chatbot creado con POO y Gemini."
        }
        self.historial = []
        self.nombre_usuario = None

    def responder(self, mensaje):
        mensaje_original = mensaje.strip()
        mensaje_normalizado = mensaje_original.lower()

        self.historial.append(mensaje_original)

        if "me llamo" in mensaje_normalizado:
            nombre = mensaje_normalizado.replace("me llamo", "").strip()

            if nombre:
                self.nombre_usuario = nombre.title()
                return f"¡Mucho gusto, {self.nombre_usuario}!"

        for clave, respuesta in self.base_conocimiento.items():
            if clave in mensaje_normalizado:
                if self.nombre_usuario:
                    return f"{self.nombre_usuario}, {respuesta}"

                return respuesta

        try:
            resultado = modelo.generate_content(mensaje_original)
            return resultado.text
        
        except Exception as error:
         print(f"Error real: {type(error).__name__}: {error}")
         return "No pude comunicarme con Gemini."

    def agregar_conocimiento(self, clave, respuesta):
        self.base_conocimiento[clave.lower().strip()] = respuesta

    def mostrar_historial(self):
        print("\n--- HISTORIAL DE CONVERSACIÓN ---")

        for mensaje in self.historial:
            print(mensaje)


def main():
    bot = Chatbot("ChatBot-Gemini")

    bot.agregar_conocimiento(
        "python",
        "Python es un lenguaje de programación."
    )

    bot.agregar_conocimiento(
        "curso",
        "Estamos aprendiendo Programación Orientada a Objetos."
    )

    bot.agregar_conocimiento(
        "gracias",
        "¡De nada! Estoy para ayudarte."
    )

    print(
        f"{bot.nombre}: ¡Hola! Escribe 'salir' para terminar."
    )

    while True:
        entrada = input("Tú: ")

        if entrada.lower().strip() == "salir":
            print(f"{bot.nombre}: ¡Hasta pronto!")
            bot.mostrar_historial()
            break

        respuesta = bot.responder(entrada)
        print(f"{bot.nombre}: {respuesta}")


if __name__ == "__main__":
    main()
