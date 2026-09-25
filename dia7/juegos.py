import random

import pygame


pygame.init()

ancho = 700
alto = 600
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Laberinto en movimiento")
reloj = pygame.time.Clock()

AZUL = (35, 90, 220)
BLANCO = (245, 247, 250)
GRIS = (205, 210, 220)
NEGRO = (25, 25, 30)
ROJO = (210, 55, 65)
VERDE = (45, 180, 90)
AMARILLO = (255, 215, 45)

fuente = pygame.font.Font(None, 32)
fuente_pequena = pygame.font.Font(None, 24)

radio = 15
velocidad_jugador = 5
NIVEL_MAXIMO = 5
inicio = (ancho // 2, alto - 30)
x, y = inicio

meta = pygame.Rect(ancho // 2 - 55, 10, 110, 38)

datos_obstaculos = [
    (80, 105, 190, 24, 2),
    (390, 190, 230, 24, -3),
    (170, 275, 150, 24, 4),
    (360, 360, 260, 24, -2),
    (60, 445, 210, 24, 5),
]

def crear_obstaculos():
    nuevos_obstaculos = []

    for pos_x, pos_y, obstaculo_ancho, obstaculo_alto, velocidad in datos_obstaculos:
        nuevos_obstaculos.append(
            {
                "rectangulo": pygame.Rect(
                    pos_x, pos_y, obstaculo_ancho, obstaculo_alto
                ),
                "velocidad": velocidad,
            }
        )

    return nuevos_obstaculos


obstaculos = crear_obstaculos()

nivel = 1
choques = 0
juego_completado = False
corriendo = True

while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                corriendo = False
            elif evento.key == pygame.K_r:
                x, y = inicio
                nivel = 1
                choques = 0
                juego_completado = False
                obstaculos = crear_obstaculos()

    teclas = pygame.key.get_pressed()

    if not juego_completado:
        if teclas[pygame.K_RIGHT]:
            x += velocidad_jugador
        if teclas[pygame.K_LEFT]:
            x -= velocidad_jugador
        if teclas[pygame.K_UP]:
            y -= velocidad_jugador
        if teclas[pygame.K_DOWN]:
            y += velocidad_jugador

        x = max(radio, min(x, ancho - radio))
        y = max(radio, min(y, alto - radio))

        for obstaculo in obstaculos:
            rectangulo = obstaculo["rectangulo"]
            rectangulo.x += obstaculo["velocidad"]

            if rectangulo.left <= 0:
                rectangulo.left = 0
                obstaculo["velocidad"] = abs(obstaculo["velocidad"])
            elif rectangulo.right >= ancho:
                rectangulo.right = ancho
                obstaculo["velocidad"] = -abs(obstaculo["velocidad"])

        circulo = pygame.Rect(
            x - radio,
            y - radio,
            radio * 2,
            radio * 2,
        )

        colision = False
        for obstaculo in obstaculos:
            if circulo.colliderect(obstaculo["rectangulo"]):
                colision = True
                break

        if colision:
            x, y = inicio
            choques += 1
        elif circulo.colliderect(meta):
            if nivel == NIVEL_MAXIMO:
                juego_completado = True
            else:
                nivel += 1
                x, y = inicio

                for obstaculo in obstaculos:
                    rectangulo = obstaculo["rectangulo"]
                    ancho_anterior = rectangulo.width
                    ancho_nuevo = random.randint(110, 290)

                    while ancho_nuevo == ancho_anterior:
                        ancho_nuevo = random.randint(110, 290)

                    rectangulo.width = ancho_nuevo
                    rectangulo.x = random.randint(0, ancho - ancho_nuevo)

                    direccion = 1 if obstaculo["velocidad"] > 0 else -1
                    rapidez_nueva = abs(obstaculo["velocidad"]) + 1
                    obstaculo["velocidad"] = direccion * rapidez_nueva

    ventana.fill(BLANCO)

    pygame.draw.rect(ventana, VERDE, meta, border_radius=8)
    pygame.draw.rect(ventana, NEGRO, meta, 2, border_radius=8)

    texto_meta = fuente_pequena.render("META", True, BLANCO)
    ventana.blit(texto_meta, texto_meta.get_rect(center=meta.center))

    for altura_linea in (93, 178, 263, 348, 433):
        pygame.draw.line(ventana, GRIS, (0, altura_linea), (ancho, altura_linea), 1)

    for obstaculo in obstaculos:
        pygame.draw.rect(
            ventana,
            ROJO,
            obstaculo["rectangulo"],
            border_radius=5,
        )

    pygame.draw.circle(ventana, AMARILLO, inicio, radio + 5, 2)
    pygame.draw.circle(ventana, AZUL, (x, y), radio)
    pygame.draw.circle(ventana, NEGRO, (x, y), radio, 2)

    texto_nivel = fuente.render(
        f"Nivel: {nivel}/{NIVEL_MAXIMO}", True, NEGRO
    )
    texto_choques = fuente.render(f"Choques: {choques}", True, NEGRO)
    texto_ayuda = fuente_pequena.render(
        "Flechas: mover    R: reiniciar juego    Esc: salir",
        True,
        NEGRO,
    )

    ventana.blit(texto_nivel, (15, 12))
    ventana.blit(texto_choques, (ancho - texto_choques.get_width() - 15, 12))
    ventana.blit(
        texto_ayuda,
        texto_ayuda.get_rect(center=(ancho // 2, 70)),
    )

    if juego_completado:
        panel = pygame.Rect(90, 225, ancho - 180, 140)
        pygame.draw.rect(ventana, BLANCO, panel, border_radius=12)
        pygame.draw.rect(ventana, VERDE, panel, 4, border_radius=12)

        texto_final = fuente.render(
            "¡Completaste los 5 niveles!", True, VERDE
        )
        texto_reinicio = fuente_pequena.render(
            "Presiona R para comenzar de nuevo", True, NEGRO
        )
        ventana.blit(
            texto_final,
            texto_final.get_rect(center=(ancho // 2, 270)),
        )
        ventana.blit(
            texto_reinicio,
            texto_reinicio.get_rect(center=(ancho // 2, 320)),
        )

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
