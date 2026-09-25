import wikipedia
wikipedia.set_lang("es")

class Chatbot:

    def __init__(self, nombre):
        self.nombre = nombre

        self.base_conocimiento = {
            "hola": "¡Hola! ¿En qué puedo ayudarte?",
            "adios": "¡Hasta luego, que tengas un buen día!",
            "como estas": "Estoy funcionando correctamente, gracias por preguntar.",
            "quien eres": "Soy un chatbot creado para practicar POO en Python."
        }

        self.historial = []
        self.nombre_usuario = None


    def responder(self, mensaje):
        mensaje = mensaje.lower().strip()
        self.historial.append(mensaje)

        # Detectar cuando el usuario dice su nombre
        if "me llamo" in mensaje:
            nombre = mensaje.replace("me llamo", "").strip()

            if nombre != "":
                self.nombre_usuario = nombre.title()

                return f"¡Mucho gusto, {self.nombre_usuario}!"


        # Buscar una palabra clave en la base de conocimiento
        for clave, respuesta in self.base_conocimiento.items():

            if clave in mensaje:
                if self.nombre_usuario:
                    return f"{self.nombre_usuario}, {respuesta}"
                return respuesta


        # Consultar Wikipedia cuando no encuentra una palabra conocida
        try:
            return wikipedia.summary(mensaje, sentences=2)
        except wikipedia.exceptions.DisambiguationError:
            return "El término es ambiguo. Por favor, sé más específico."
        except Exception:
            return "No encontré información, ¿podrías reformularlo?"


    def agregar_conocimiento(self, clave, respuesta):
        self.base_conocimiento[clave.lower()] = respuesta


    def mostrar_historial(self):
        print("\n--- HISTORIAL DE CONVERSACIÓN ---")

        for mensaje in self.historial:
            print(mensaje)


def main():
    
    bot = Chatbot("ChatBot-Yessi")


    # Agregar 3 nuevos conocimientos
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
        f"{bot.nombre}: ¡Hola! Escribe 'salir' para terminar la conversación."
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
