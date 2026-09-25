class Chatbot:

    def __init__(self, nombre):
        self.nombre = nombre

        self.base_conocimiento = {
            "hola": "¡Hola! ¿En qué puedo ayudarte?",
            "adios": "¡Hasta luego, que tengas un buen día!",
            "como estas": "Estoy funcionando correctamente, gracias por preguntar.",
            "quien eres": "Soy un chatbot creado para practicar POO en Python.",    
            "buenos dias": "¡Buenos días! Espero que tengas una excelente jornada.",
            "buenas tardes": "¡Buenas tardes! ¿Qué deseas consultar?",
            "buenas noches": "¡Buenas noches! Estoy disponible para ayudarte.",
            "tu nombre": f"Mi nombre es {self.nombre}.",
            "puedes hacer": "Puedo responder preguntas sobre Python y programación.",
            "ayuda": "Pregúntame sobre clases, objetos, métodos o estructuras de datos.",
            "poo": "POO significa Programación Orientada a Objetos.",
            "clase": "Una clase es un molde utilizado para crear objetos.",
            "objeto": "Un objeto es una instancia creada a partir de una clase.",
            "atributo": "Un atributo es una variable que pertenece a un objeto.",
            "metodo": "Un método es una función definida dentro de una clase.",
            "constructor": "El método __init__ inicializa los atributos del objeto.",
            "herencia": "La herencia permite recibir atributos y métodos de otra clase.",
            "polimorfismo": "El polimorfismo permite distintas versiones de un método.",
            "encapsulamiento": "El encapsulamiento reúne datos y métodos en una clase.",
            "variable": "Una variable guarda un valor para utilizarlo en el programa.",
            "funcion": "Una función es un bloque reutilizable que realiza una tarea.",
            "lista": "Una lista es una colección ordenada y modificable.",
            "tupla": "Una tupla es una colección ordenada que no puede modificarse.",
            "diccionario": "Un diccionario almacena pares de clave y valor.",
            "bucle": "Los bucles for y while permiten repetir instrucciones.",
            "condicional": "if, elif y else permiten tomar decisiones.",
            "pygame": "Pygame es una biblioteca para crear videojuegos con Python.",
            "binario": "El sistema binario utiliza solamente los dígitos 0 y 1.",
            "factorial": "El factorial multiplica los enteros desde 1 hasta un número.",
            "error": "Los errores ayudan a encontrar problemas dentro del código.",
            "snpp": "El SNPP ofrece formación profesional en distintas áreas.",
            "paraguay": "Paraguay es un país de América del Sur.",
            "asuncion": "Asunción es la capital de Paraguay."
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


        # Respuesta cuando no encuentra una palabra conocida
        if self.nombre_usuario:
            return f"{self.nombre_usuario}, no entendí tu mensaje, ¿podrías reformularlo?"

        return "No entendí tu mensaje, ¿podrías reformularlo?"


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
