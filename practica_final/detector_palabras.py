import ssl
from urllib import request
from urllib.error import HTTPError, URLError

import certifi


PALABRAS_NO_PERMITIDAS = [
    "coño",
    "bobo",
    "culiao",
    "pinche",
    "estupido",
    "estupida",
]


def verificar_web(url):
    solicitud = request.Request(
        url,
        headers={"User-Agent": "PracticaPython/1.0 (uso educativo)"},
    )
    contexto_ssl = ssl.create_default_context(cafile=certifi.where())

    try:
        with request.urlopen(
            solicitud,
            timeout=15,
            context=contexto_ssl,
        ) as respuesta:
            contenido = respuesta.read().decode("utf-8", errors="ignore").lower()
    except HTTPError as error:
        return f"Error HTTP {error.code}: el sitio rechazó la solicitud."
    except URLError as error:
        return f"No se pudo conectar con el sitio: {error.reason}"
    except ValueError:
        return "La dirección ingresada no es válida."

    palabras_encontradas = []

    for palabra in PALABRAS_NO_PERMITIDAS:
        if palabra in contenido:
            palabras_encontradas.append(palabra)

    return palabras_encontradas


if __name__ == "__main__":
    url = "https://es.wiktionary.org/wiki/Wikcionario:Insultos_regionales"

    print("\n------------------------------")
    print("Informe del sitio:")
    print(verificar_web(url))
