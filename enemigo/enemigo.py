import pygame
import random
import config

enemigos_vivos = False

def generar_grilla(filas, columnas, x_inicial, y_inicial, sep_x, sep_y):
    enemigos = []

    for fila in range(filas):
        for columna in range(columnas):
            tipo = random.randint(1, 3)

            x = x_inicial + columna * sep_x
            y = y_inicial + fila * sep_y

            bloque = config.crear_bloque(x, y, tipo)
            enemigos.append(bloque)

    return enemigos


def bloquear_recibir_golpe(bloque):
    bloque["vidas"] -= 1

    if bloque["vidas"] <= 0:
        bloque["visible"] = False
        return

    bloque["indice_imagen"] += 1

    if bloque["indice_imagen"] < len(bloque["imagenes"]):
        imagen_original = pygame.image.load(
            bloque["imagenes"][bloque["indice_imagen"]]
        ).convert_alpha()

        ancho = imagen_original.get_width() // 2
        alto = imagen_original.get_height() // 2

        bloque["imagen"] = pygame.transform.scale(imagen_original, (ancho, alto))


def dibujar_bloque(bloque):
    if bloque["visible"]:
        config.pantalla.blit(bloque["imagen"], bloque["rect"])
