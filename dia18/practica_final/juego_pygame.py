import random

import pygame


ANCHO = 800
ALTO = 600
FPS = 60

COLOR_FONDO = (13, 19, 33)
COLOR_JUGADOR = (65, 214, 164)
COLOR_OBSTACULO = (245, 91, 91)
COLOR_TEXTO = (240, 244, 255)
COLOR_SECUNDARIO = (157, 170, 196)


def crear_obstaculo():
    ancho = random.randint(45, 110)
    alto = random.randint(25, 55)
    posicion_x = random.randint(0, ANCHO - ancho)
    return pygame.Rect(posicion_x, -alto, ancho, alto)


def dibujar_texto(pantalla, texto, fuente, color, posicion, centrado=False):
    superficie = fuente.render(texto, True, color)
    rectangulo = superficie.get_rect()

    if centrado:
        rectangulo.center = posicion
    else:
        rectangulo.topleft = posicion

    pantalla.blit(superficie, rectangulo)


def reiniciar_partida(jugador, obstaculos):
    jugador.centerx = ANCHO // 2
    jugador.bottom = ALTO - 35
    obstaculos.clear()
    return 0, pygame.time.get_ticks(), False


def main():
    pygame.init()

    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Esquiva los bloques")
    reloj = pygame.time.Clock()

    fuente_titulo = pygame.font.SysFont("Segoe UI", 46, bold=True)
    fuente_normal = pygame.font.SysFont("Segoe UI", 24)
    fuente_pequena = pygame.font.SysFont("Segoe UI", 18)

    jugador = pygame.Rect(ANCHO // 2 - 30, ALTO - 80, 60, 35)
    obstaculos = []
    estrellas = [
        (random.randint(0, ANCHO), random.randint(0, ALTO), random.randint(1, 2))
        for _ in range(70)
    ]

    puntuacion = 0
    ultimo_obstaculo = pygame.time.get_ticks()
    juego_terminado = False
    ejecutando = True

    while ejecutando:
        reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                elif evento.key == pygame.K_r and juego_terminado:
                    puntuacion, ultimo_obstaculo, juego_terminado = reiniciar_partida(
                        jugador,
                        obstaculos,
                    )

        teclas = pygame.key.get_pressed()

        if not juego_terminado:
            velocidad_jugador = 7

            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                jugador.x -= velocidad_jugador
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                jugador.x += velocidad_jugador

            jugador.x = max(0, min(jugador.x, ANCHO - jugador.width))

            momento_actual = pygame.time.get_ticks()
            intervalo = max(280, 750 - puntuacion * 12)

            if momento_actual - ultimo_obstaculo >= intervalo:
                obstaculos.append(crear_obstaculo())
                ultimo_obstaculo = momento_actual

            velocidad_obstaculos = min(14, 5 + puntuacion // 8)

            for obstaculo in obstaculos[:]:
                obstaculo.y += velocidad_obstaculos

                if obstaculo.colliderect(jugador):
                    juego_terminado = True
                elif obstaculo.top > ALTO:
                    obstaculos.remove(obstaculo)
                    puntuacion += 1

        pantalla.fill(COLOR_FONDO)

        for x, y, radio in estrellas:
            pygame.draw.circle(pantalla, (47, 61, 88), (x, y), radio)

        pygame.draw.rect(pantalla, COLOR_JUGADOR, jugador, border_radius=8)

        for obstaculo in obstaculos:
            pygame.draw.rect(
                pantalla,
                COLOR_OBSTACULO,
                obstaculo,
                border_radius=6,
            )

        dibujar_texto(
            pantalla,
            f"Puntuación: {puntuacion}",
            fuente_normal,
            COLOR_TEXTO,
            (24, 20),
        )
        dibujar_texto(
            pantalla,
            "Mover: flechas o A/D · Salir: Esc",
            fuente_pequena,
            COLOR_SECUNDARIO,
            (24, 54),
        )

        if juego_terminado:
            capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            capa.fill((5, 9, 18, 205))
            pantalla.blit(capa, (0, 0))

            dibujar_texto(
                pantalla,
                "¡Fin del juego!",
                fuente_titulo,
                COLOR_TEXTO,
                (ANCHO // 2, ALTO // 2 - 55),
                centrado=True,
            )
            dibujar_texto(
                pantalla,
                f"Puntuación final: {puntuacion}",
                fuente_normal,
                COLOR_JUGADOR,
                (ANCHO // 2, ALTO // 2 + 5),
                centrado=True,
            )
            dibujar_texto(
                pantalla,
                "Presiona R para volver a jugar",
                fuente_normal,
                COLOR_SECUNDARIO,
                (ANCHO // 2, ALTO // 2 + 50),
                centrado=True,
            )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
