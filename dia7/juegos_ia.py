import math
import random

import pygame


pygame.init()

ANCHO = 900
ALTO = 650
FPS = 60
NIVEL_MAXIMO = 5
NUCLEOS_POR_NIVEL = 3

RADIO_JUGADOR = 14
VELOCIDAD_JUGADOR = 260
VELOCIDAD_DASH = 650
DURACION_DASH = 0.18
RECARGA_DASH = 1.35

INICIO = pygame.Vector2(ANCHO // 2, ALTO - 55)
PORTAL = pygame.Vector2(ANCHO // 2, 112)
RADIO_PORTAL = 27

FONDO_1 = (5, 8, 24)
FONDO_2 = (11, 18, 43)
AZUL_NEON = (50, 185, 255)
CIAN = (60, 245, 230)
VERDE = (70, 255, 145)
ROJO = (255, 70, 105)
MAGENTA = (245, 70, 220)
NARANJA = (255, 145, 55)
AMARILLO = (255, 225, 75)
BLANCO = (240, 248, 255)
GRIS = (125, 145, 180)

ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Neon Escape")
reloj = pygame.time.Clock()

fuente_titulo = pygame.font.Font(None, 92)
fuente_grande = pygame.font.Font(None, 54)
fuente = pygame.font.Font(None, 32)
fuente_pequena = pygame.font.Font(None, 23)


def crear_fondo():
    fondo = pygame.Surface((ANCHO, ALTO))

    for y in range(ALTO):
        mezcla = y / ALTO
        color = tuple(
            int(FONDO_1[i] * (1 - mezcla) + FONDO_2[i] * mezcla)
            for i in range(3)
        )
        pygame.draw.line(fondo, color, (0, y), (ANCHO, y))

    for x in range(0, ANCHO, 50):
        pygame.draw.line(fondo, (18, 30, 65), (x, 75), (x, ALTO), 1)

    for y in range(100, ALTO, 50):
        pygame.draw.line(fondo, (18, 30, 65), (0, y), (ANCHO, y), 1)

    return fondo


FONDO = crear_fondo()


def escribir(superficie, texto, tipo_fuente, color, centro=None, esquina=None):
    imagen = tipo_fuente.render(texto, True, color)
    rectangulo = imagen.get_rect()

    if centro is not None:
        rectangulo.center = centro
    elif esquina is not None:
        rectangulo.topleft = esquina

    superficie.blit(imagen, rectangulo)
    return rectangulo


def circulo_toca_rectangulo(posicion, radio, rectangulo):
    cercano_x = max(rectangulo.left, min(posicion.x, rectangulo.right))
    cercano_y = max(rectangulo.top, min(posicion.y, rectangulo.bottom))
    distancia_x = posicion.x - cercano_x
    distancia_y = posicion.y - cercano_y
    return distancia_x**2 + distancia_y**2 <= radio**2


def dibujar_brillo_circular(superficie, posicion, radio, color):
    alcance = radio + 24
    capa = pygame.Surface((alcance * 2, alcance * 2), pygame.SRCALPHA)
    centro = (alcance, alcance)

    pygame.draw.circle(capa, (*color, 20), centro, radio + 22)
    pygame.draw.circle(capa, (*color, 40), centro, radio + 14)
    pygame.draw.circle(capa, (*color, 75), centro, radio + 7)

    superficie.blit(
        capa,
        (int(posicion.x - alcance), int(posicion.y - alcance)),
    )


class Particula:
    def __init__(self, posicion, color, velocidad, vida, tamano):
        self.posicion = pygame.Vector2(posicion)
        self.color = color
        self.velocidad = pygame.Vector2(velocidad)
        self.vida = vida
        self.vida_maxima = vida
        self.tamano = tamano

    def actualizar(self, dt):
        self.posicion += self.velocidad * dt
        self.velocidad *= 0.97
        self.vida -= dt
        return self.vida > 0

    def dibujar(self, superficie):
        intensidad = max(0, self.vida / self.vida_maxima)
        color = tuple(int(valor * intensidad) for valor in self.color)
        radio = max(1, int(self.tamano * intensidad))
        pygame.draw.circle(
            superficie,
            color,
            (round(self.posicion.x), round(self.posicion.y)),
            radio,
        )


class Laser:
    def __init__(self, y, ancho_laser, velocidad, direccion, color):
        self.x = random.randint(0, ANCHO - ancho_laser)
        self.rectangulo = pygame.Rect(self.x, y, ancho_laser, 24)
        self.velocidad = velocidad * direccion
        self.color = color

    def actualizar(self, dt):
        self.x += self.velocidad * dt
        self.rectangulo.x = round(self.x)

        if self.rectangulo.left <= 0:
            self.rectangulo.left = 0
            self.x = self.rectangulo.x
            self.velocidad = abs(self.velocidad)
        elif self.rectangulo.right >= ANCHO:
            self.rectangulo.right = ANCHO
            self.x = self.rectangulo.x
            self.velocidad = -abs(self.velocidad)

    def dibujar(self, superficie):
        margen = 16
        tamano = (self.rectangulo.width + margen * 2, self.rectangulo.height + margen * 2)
        capa = pygame.Surface(tamano, pygame.SRCALPHA)

        pygame.draw.rect(
            capa,
            (*self.color, 30),
            capa.get_rect(),
            border_radius=18,
        )
        pygame.draw.rect(
            capa,
            (*self.color, 65),
            capa.get_rect().inflate(-12, -12),
            border_radius=12,
        )
        superficie.blit(
            capa,
            (self.rectangulo.x - margen, self.rectangulo.y - margen),
        )

        pygame.draw.rect(superficie, (25, 20, 45), self.rectangulo, border_radius=7)
        interior = self.rectangulo.inflate(-6, -8)
        pygame.draw.rect(superficie, self.color, interior, border_radius=5)
        pygame.draw.line(
            superficie,
            BLANCO,
            (interior.left + 8, interior.top + 2),
            (interior.right - 8, interior.top + 2),
            2,
        )


class Nucleo:
    def __init__(self, posicion):
        self.posicion = pygame.Vector2(posicion)
        self.fase = random.uniform(0, math.tau)

    def dibujar(self, superficie, tiempo):
        pulso = math.sin(tiempo * 4 + self.fase)
        radio = 10 + int(pulso * 2)
        dibujar_brillo_circular(superficie, self.posicion, radio, CIAN)

        pygame.draw.circle(
            superficie,
            CIAN,
            (round(self.posicion.x), round(self.posicion.y)),
            radio,
        )
        pygame.draw.circle(
            superficie,
            BLANCO,
            (round(self.posicion.x), round(self.posicion.y)),
            max(3, radio // 3),
        )

        angulo = tiempo * 2.5 + self.fase
        satelite = self.posicion + pygame.Vector2(math.cos(angulo), math.sin(angulo)) * 18
        pygame.draw.circle(
            superficie,
            CIAN,
            (round(satelite.x), round(satelite.y)),
            3,
        )


class Juego:
    def __init__(self):
        self.activo = True
        self.estado = "menu"
        self.pausa = False
        self.animacion = 0
        self.mejor_puntaje = 0
        self.particulas = []
        self.lasers = []
        self.nucleos = []
        self.estrellas = [
            {
                "x": random.randrange(ANCHO),
                "y": random.randrange(ALTO),
                "velocidad": random.uniform(8, 28),
                "tamano": random.choice((1, 1, 1, 2)),
            }
            for _ in range(90)
        ]

        self.posicion = pygame.Vector2(INICIO)
        self.direccion_anterior = pygame.Vector2(0, -1)
        self.rastro = []
        self.nivel = 1
        self.vidas = 3
        self.puntaje = 0
        self.tiempo_juego = 0
        self.invulnerable = 0
        self.dash_restante = 0
        self.recarga_dash = 0
        self.sacudida = 0
        self.aviso = ""
        self.tiempo_aviso = 0

    def nueva_partida(self):
        self.estado = "jugando"
        self.pausa = False
        self.nivel = 1
        self.vidas = 3
        self.puntaje = 0
        self.tiempo_juego = 0
        self.invulnerable = 0
        self.dash_restante = 0
        self.recarga_dash = 0
        self.sacudida = 0
        self.particulas.clear()
        self.preparar_nivel()

    def preparar_nivel(self):
        self.posicion = pygame.Vector2(INICIO)
        self.direccion_anterior = pygame.Vector2(0, -1)
        self.rastro.clear()
        self.lasers.clear()
        self.nucleos.clear()

        cantidad_lasers = 4 + (self.nivel - 1) // 2
        posiciones_y = [
            int(185 + indice * (325 / max(1, cantidad_lasers - 1)))
            for indice in range(cantidad_lasers)
        ]
        colores_laser = (MAGENTA, ROJO, NARANJA, MAGENTA, ROJO, NARANJA)

        for indice, pos_y in enumerate(posiciones_y):
            ancho_minimo = 135 + self.nivel * 10
            ancho_maximo = min(360, 245 + self.nivel * 20)
            ancho_laser = random.randint(ancho_minimo, ancho_maximo)
            rapidez = 85 + self.nivel * 25 + indice * 16 + random.randint(-8, 12)
            direccion = 1 if indice % 2 == 0 else -1
            self.lasers.append(
                Laser(
                    pos_y,
                    ancho_laser,
                    rapidez,
                    direccion,
                    colores_laser[indice % len(colores_laser)],
                )
            )

        limites = [135] + posiciones_y + [565]
        zonas_seguras = [
            (limites[indice] + limites[indice + 1]) // 2
            for indice in range(len(limites) - 1)
        ]

        for pos_y in random.sample(zonas_seguras, NUCLEOS_POR_NIVEL):
            self.nucleos.append(
                Nucleo((random.randint(75, ANCHO - 75), pos_y))
            )

        self.aviso = f"NIVEL {self.nivel}"
        self.tiempo_aviso = 1.4

    def crear_explosion(self, posicion, color, cantidad):
        for _ in range(cantidad):
            angulo = random.uniform(0, math.tau)
            rapidez = random.uniform(70, 240)
            velocidad = pygame.Vector2(math.cos(angulo), math.sin(angulo)) * rapidez
            self.particulas.append(
                Particula(
                    posicion,
                    color,
                    velocidad,
                    random.uniform(0.35, 0.8),
                    random.randint(3, 7),
                )
            )

    def manejar_evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return

        if evento.key == pygame.K_ESCAPE:
            if self.estado == "menu":
                self.activo = False
            else:
                self.estado = "menu"
                self.pausa = False
            return

        if self.estado == "menu":
            if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.nueva_partida()
            return

        if self.estado == "jugando":
            if evento.key == pygame.K_p:
                self.pausa = not self.pausa
            elif evento.key == pygame.K_r:
                self.nueva_partida()
            elif (
                evento.key == pygame.K_SPACE
                and not self.pausa
                and self.recarga_dash <= 0
            ):
                self.dash_restante = DURACION_DASH
                self.recarga_dash = RECARGA_DASH
                self.crear_explosion(self.posicion, AZUL_NEON, 8)
            return

        if self.estado in ("victoria", "derrota"):
            if evento.key in (pygame.K_RETURN, pygame.K_r, pygame.K_SPACE):
                self.nueva_partida()

    def actualizar_estrellas(self, dt):
        for estrella in self.estrellas:
            estrella["y"] += estrella["velocidad"] * dt
            if estrella["y"] > ALTO:
                estrella["y"] = 0
                estrella["x"] = random.randrange(ANCHO)

    def actualizar(self, dt):
        self.animacion += dt
        self.actualizar_estrellas(dt)
        self.particulas = [
            particula
            for particula in self.particulas
            if particula.actualizar(dt)
        ]

        if self.sacudida > 0:
            self.sacudida = max(0, self.sacudida - dt)

        if self.tiempo_aviso > 0:
            self.tiempo_aviso = max(0, self.tiempo_aviso - dt)

        if self.estado != "jugando" or self.pausa:
            return

        self.tiempo_juego += dt
        self.invulnerable = max(0, self.invulnerable - dt)
        self.recarga_dash = max(0, self.recarga_dash - dt)

        estaba_en_dash = self.dash_restante > 0
        self.dash_restante = max(0, self.dash_restante - dt)

        teclas = pygame.key.get_pressed()
        direccion = pygame.Vector2(0, 0)

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            direccion.x += 1
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            direccion.x -= 1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            direccion.y += 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            direccion.y -= 1

        if direccion.length_squared() > 0:
            direccion = direccion.normalize()
            self.direccion_anterior = pygame.Vector2(direccion)

        if estaba_en_dash:
            direccion_movimiento = self.direccion_anterior
            rapidez = VELOCIDAD_DASH
        else:
            direccion_movimiento = direccion
            rapidez = VELOCIDAD_JUGADOR

        if direccion_movimiento.length_squared() > 0:
            self.posicion += direccion_movimiento * rapidez * dt
            self.rastro.append(pygame.Vector2(self.posicion))
            self.rastro = self.rastro[-18:]

        self.posicion.x = max(
            RADIO_JUGADOR,
            min(self.posicion.x, ANCHO - RADIO_JUGADOR),
        )
        self.posicion.y = max(
            82 + RADIO_JUGADOR,
            min(self.posicion.y, ALTO - 32 - RADIO_JUGADOR),
        )

        for laser in self.lasers:
            laser.actualizar(dt)

        if not estaba_en_dash and self.invulnerable <= 0:
            for laser in self.lasers:
                if circulo_toca_rectangulo(
                    self.posicion,
                    RADIO_JUGADOR,
                    laser.rectangulo,
                ):
                    self.recibir_impacto()
                    return

        for nucleo in self.nucleos[:]:
            if self.posicion.distance_to(nucleo.posicion) <= RADIO_JUGADOR + 13:
                self.nucleos.remove(nucleo)
                self.puntaje += 250 * self.nivel
                self.crear_explosion(nucleo.posicion, CIAN, 18)

                if not self.nucleos:
                    self.aviso = "PORTAL DESBLOQUEADO"
                    self.tiempo_aviso = 1.3

        portal_abierto = not self.nucleos
        if (
            portal_abierto
            and self.posicion.distance_to(PORTAL)
            <= RADIO_JUGADOR + RADIO_PORTAL
        ):
            self.completar_nivel()

    def recibir_impacto(self):
        self.vidas -= 1
        self.sacudida = 0.35
        self.crear_explosion(self.posicion, ROJO, 28)
        self.rastro.clear()

        if self.vidas <= 0:
            self.estado = "derrota"
            self.mejor_puntaje = max(self.mejor_puntaje, self.puntaje)
        else:
            self.posicion = pygame.Vector2(INICIO)
            self.invulnerable = 1.2
            self.aviso = "IMPACTO - ESCUDO PERDIDO"
            self.tiempo_aviso = 1.1

    def completar_nivel(self):
        self.crear_explosion(PORTAL, VERDE, 40)
        self.puntaje += 1000 * self.nivel

        if self.nivel >= NIVEL_MAXIMO:
            self.estado = "victoria"
            self.mejor_puntaje = max(self.mejor_puntaje, self.puntaje)
        else:
            self.nivel += 1
            self.vidas = min(3, self.vidas + 1)
            self.preparar_nivel()

    def dibujar_estrellas(self, superficie):
        for estrella in self.estrellas:
            brillo = 120 + int(
                90 * (math.sin(self.animacion * 2 + estrella["x"]) + 1) / 2
            )
            color = (brillo, brillo, min(255, brillo + 25))
            pygame.draw.circle(
                superficie,
                color,
                (round(estrella["x"]), round(estrella["y"])),
                estrella["tamano"],
            )

    def dibujar_portal(self, superficie):
        abierto = not self.nucleos
        color = VERDE if abierto else (100, 75, 145)
        pulso = int(math.sin(self.animacion * 4) * 4)

        dibujar_brillo_circular(
            superficie,
            PORTAL,
            RADIO_PORTAL + pulso,
            color,
        )

        for extra in (12, 5, 0):
            pygame.draw.circle(
                superficie,
                color,
                (round(PORTAL.x), round(PORTAL.y)),
                RADIO_PORTAL + extra + pulso,
                2,
            )

        pygame.draw.circle(
            superficie,
            FONDO_1,
            (round(PORTAL.x), round(PORTAL.y)),
            RADIO_PORTAL - 6,
        )

        etiqueta = "PORTAL ABIERTO" if abierto else "PORTAL BLOQUEADO"
        escribir(
            superficie,
            etiqueta,
            fuente_pequena,
            color,
            centro=(PORTAL.x, PORTAL.y + 52),
        )

    def dibujar_jugador(self, superficie):
        cantidad = len(self.rastro)
        for indice, punto in enumerate(self.rastro):
            intensidad = (indice + 1) / max(1, cantidad)
            color = tuple(int(valor * intensidad * 0.55) for valor in AZUL_NEON)
            radio = max(2, int(RADIO_JUGADOR * intensidad * 0.8))
            pygame.draw.circle(
                superficie,
                color,
                (round(punto.x), round(punto.y)),
                radio,
            )

        visible = self.invulnerable <= 0 or int(self.invulnerable * 12) % 2 == 0
        if not visible:
            return

        dibujar_brillo_circular(
            superficie,
            self.posicion,
            RADIO_JUGADOR,
            AZUL_NEON,
        )
        pygame.draw.circle(
            superficie,
            AZUL_NEON,
            (round(self.posicion.x), round(self.posicion.y)),
            RADIO_JUGADOR,
        )
        pygame.draw.circle(
            superficie,
            BLANCO,
            (round(self.posicion.x - 4), round(self.posicion.y - 4)),
            4,
        )

    def dibujar_hud(self, superficie):
        panel = pygame.Surface((ANCHO, 76), pygame.SRCALPHA)
        panel.fill((4, 8, 24, 225))
        superficie.blit(panel, (0, 0))
        pygame.draw.line(superficie, AZUL_NEON, (0, 75), (ANCHO, 75), 2)

        escribir(
            superficie,
            f"NIVEL {self.nivel}/{NIVEL_MAXIMO}",
            fuente,
            BLANCO,
            esquina=(20, 14),
        )
        escribir(
            superficie,
            f"PUNTAJE {self.puntaje:06d}",
            fuente,
            CIAN,
            esquina=(180, 14),
        )

        recogidos = NUCLEOS_POR_NIVEL - len(self.nucleos)
        escribir(
            superficie,
            f"NÚCLEOS {recogidos}/{NUCLEOS_POR_NIVEL}",
            fuente,
            AMARILLO,
            esquina=(430, 14),
        )

        escribir(superficie, "ESCUDOS", fuente_pequena, GRIS, esquina=(690, 10))
        for indice in range(3):
            color = VERDE if indice < self.vidas else (45, 55, 75)
            pygame.draw.circle(superficie, color, (715 + indice * 29, 43), 10)
            pygame.draw.circle(superficie, BLANCO, (715 + indice * 29, 43), 10, 1)

        pygame.draw.rect(superficie, (35, 45, 70), (20, 54, 130, 8), border_radius=4)
        disponible = 1 - min(1, self.recarga_dash / RECARGA_DASH)
        pygame.draw.rect(
            superficie,
            AZUL_NEON,
            (20, 54, int(130 * disponible), 8),
            border_radius=4,
        )
        escribir(superficie, "DASH", fuente_pequena, GRIS, esquina=(155, 48))

    def dibujar_menu(self, superficie):
        escribir(
            superficie,
            "NEON ESCAPE",
            fuente_titulo,
            AZUL_NEON,
            centro=(ANCHO // 2, 150),
        )
        escribir(
            superficie,
            "Cruza el laberinto. Reúne energía. Escapa.",
            fuente,
            BLANCO,
            centro=(ANCHO // 2, 215),
        )

        ancho_boton = 330 + int(math.sin(self.animacion * 3) * 8)
        boton = pygame.Rect(0, 0, ancho_boton, 66)
        boton.center = (ANCHO // 2, 315)
        pygame.draw.rect(superficie, (18, 45, 78), boton, border_radius=15)
        pygame.draw.rect(superficie, CIAN, boton, 2, border_radius=15)
        escribir(
            superficie,
            "ENTER PARA JUGAR",
            fuente_grande,
            CIAN,
            centro=boton.center,
        )

        instrucciones = (
            "Flechas o WASD: mover",
            "Espacio: atravesar láseres con dash",
            "P: pausa    R: reiniciar    Esc: salir",
            "Recoge 3 núcleos para abrir el portal",
        )
        for indice, linea in enumerate(instrucciones):
            escribir(
                superficie,
                linea,
                fuente,
                GRIS if indice < 3 else AMARILLO,
                centro=(ANCHO // 2, 415 + indice * 38),
            )

        if self.mejor_puntaje > 0:
            escribir(
                superficie,
                f"MEJOR PUNTAJE: {self.mejor_puntaje}",
                fuente,
                VERDE,
                centro=(ANCHO // 2, 590),
            )

    def dibujar_panel_final(self, superficie, victoria):
        velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        velo.fill((2, 5, 18, 205))
        superficie.blit(velo, (0, 0))

        panel = pygame.Rect(150, 145, 600, 365)
        color = VERDE if victoria else ROJO
        pygame.draw.rect(superficie, (10, 18, 40), panel, border_radius=24)
        pygame.draw.rect(superficie, color, panel, 3, border_radius=24)

        titulo = "¡ESCAPASTE!" if victoria else "MISIÓN FALLIDA"
        subtitulo = (
            "Completaste los cinco sectores"
            if victoria
            else "Tus escudos se agotaron"
        )

        escribir(
            superficie,
            titulo,
            fuente_titulo,
            color,
            centro=(ANCHO // 2, 225),
        )
        escribir(
            superficie,
            subtitulo,
            fuente,
            BLANCO,
            centro=(ANCHO // 2, 290),
        )
        escribir(
            superficie,
            f"Puntaje final: {self.puntaje}",
            fuente_grande,
            CIAN,
            centro=(ANCHO // 2, 350),
        )
        escribir(
            superficie,
            f"Tiempo: {self.tiempo_juego:.1f} segundos",
            fuente,
            GRIS,
            centro=(ANCHO // 2, 400),
        )
        escribir(
            superficie,
            "ENTER o R para jugar otra vez",
            fuente,
            AMARILLO,
            centro=(ANCHO // 2, 465),
        )

    def dibujar(self, pantalla):
        escena = pygame.Surface((ANCHO, ALTO))
        escena.blit(FONDO, (0, 0))
        self.dibujar_estrellas(escena)

        if self.estado == "menu":
            self.dibujar_menu(escena)
        else:
            for laser in self.lasers:
                laser.dibujar(escena)

            self.dibujar_portal(escena)

            for nucleo in self.nucleos:
                nucleo.dibujar(escena, self.animacion)

            for particula in self.particulas:
                particula.dibujar(escena)

            self.dibujar_jugador(escena)
            self.dibujar_hud(escena)

            escribir(
                escena,
                "Flechas/WASD: mover   ESPACIO: dash   P: pausa   ESC: menú",
                fuente_pequena,
                GRIS,
                centro=(ANCHO // 2, ALTO - 14),
            )

            if self.tiempo_aviso > 0 and self.estado == "jugando":
                ancho_aviso = max(320, len(self.aviso) * 15)
                caja = pygame.Rect(0, 0, ancho_aviso, 58)
                caja.center = (ANCHO // 2, ALTO // 2)
                pygame.draw.rect(escena, (8, 15, 38), caja, border_radius=14)
                pygame.draw.rect(escena, CIAN, caja, 2, border_radius=14)
                escribir(
                    escena,
                    self.aviso,
                    fuente,
                    BLANCO,
                    centro=caja.center,
                )

            if self.pausa and self.estado == "jugando":
                velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
                velo.fill((2, 5, 18, 185))
                escena.blit(velo, (0, 0))
                escribir(
                    escena,
                    "PAUSA",
                    fuente_titulo,
                    CIAN,
                    centro=(ANCHO // 2, ALTO // 2 - 25),
                )
                escribir(
                    escena,
                    "Presiona P para continuar",
                    fuente,
                    BLANCO,
                    centro=(ANCHO // 2, ALTO // 2 + 45),
                )

            if self.estado == "victoria":
                self.dibujar_panel_final(escena, True)
            elif self.estado == "derrota":
                self.dibujar_panel_final(escena, False)

        pantalla.fill(FONDO_1)
        desplazamiento = (0, 0)
        if self.sacudida > 0:
            fuerza = max(1, int(self.sacudida * 24))
            desplazamiento = (
                random.randint(-fuerza, fuerza),
                random.randint(-fuerza, fuerza),
            )

        pantalla.blit(escena, desplazamiento)


juego = Juego()

while juego.activo:
    dt = min(reloj.tick(FPS) / 1000, 0.035)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            juego.activo = False
        else:
            juego.manejar_evento(evento)

    juego.actualizar(dt)
    juego.dibujar(ventana)
    pygame.display.flip()

pygame.quit()
