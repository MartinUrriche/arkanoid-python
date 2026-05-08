import pygame
import json
import config


def ordenar_por_puntaje(elemento):
    return elemento["puntaje"]


#  Guarda el puntaje en JSON
def guardar_score(nombre, puntaje):
    try:
        with open(config.RUTA_JSON, "r") as archivo:
            datos = json.load(archivo)
    except:
        datos = []

    # Agregamos otro puntaje
    datos.append({"nombre": nombre, "puntaje": puntaje})

    # Ordenamos con sort de mayor a menor
    datos.sort(key=ordenar_por_puntaje, reverse=True)

    # Solo guardamos 10 posiciones
    datos = datos[:10]

    # Guardamos el archivo
    with open(config.RUTA_JSON, "w") as archivo:
        json.dump(datos, archivo, indent=4)



def menu_scoreboard(eventos):

    # Inicia música del Scoreboard
    if not getattr(config, "musica_score_activa", False):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(config.MUSICA_PUNTAJE)
        pygame.mixer.music.play(-1)
        config.musica_score_activa = True

    # Fondo del Scoreboard
    config.pantalla.blit(config.scoreboard_img, (0, 0))

    #  Escribe nuestro apodo en mayúsculas, en blanco 
    texto_nombre = config.scoreboard_font.render(
        config.scoreboard_aka, False, (255, 255, 0)
    )
    config.pantalla.blit(texto_nombre, (620, 560))

    # Crea un rect que va apareciendo cada 0.5 segundos
    tiempo_actual = pygame.time.get_ticks()
    if (tiempo_actual // 500) % 2 == 0:
        x_cursor = 620 + texto_nombre.get_width() + 10
        pygame.draw.rect(config.pantalla, (255, 255, 0), (x_cursor, 580, 20, 5))

    # CARGAR SCORES DEL JSON
    try:
        with open(config.RUTA_JSON, "r") as archivo:
            datos = json.load(archivo)
    except:
        datos = []

    # -------- POSICIONES EN PANTALLA --------
    columna_score_x = 360
    columna_name_x = 560
    filas_y = [125, 145, 165, 185, 205, 225, 245, 265, 285, 305]

    # -------- DIBUJAR PUNTAJES --------
    for i in range(len(datos)):
        if i < 10:
            jugador = datos[i]

            texto_score = config.scoreboard_font.render(
                str(jugador["puntaje"]), True, (255, 255, 255)
            )
            texto_nombre_rank = config.scoreboard_font.render(
                jugador["nombre"], True, (255, 255, 255)
            )

            config.pantalla.blit(texto_score, (columna_score_x, filas_y[i]))
            config.pantalla.blit(texto_nombre_rank, (columna_name_x, filas_y[i]))

    # -------- MANEJO DE TECLADO --------
    for evento in eventos:
        if evento.type == pygame.KEYDOWN:

            # ENTER → guardar nombre y volver al menú
            if evento.key == pygame.K_RETURN and len(config.scoreboard_aka) > 0:
                guardar_score(config.scoreboard_aka, config.puntaje_actual)
                config.scoreboard_aka = ""

                pygame.mixer.music.stop()
                config.musica_score_activa = False
                config.estado = "menu_inicial"

            # BORRAR LETRA
            elif evento.key == pygame.K_BACKSPACE:
                config.scoreboard_aka = config.scoreboard_aka[:-1]

            # AGREGAR LETRAS Y NÚMEROS
            else:
                if len(config.scoreboard_aka) < 10:
                    caracter = evento.unicode.upper()
                    if caracter.isalnum():
                        config.scoreboard_aka += caracter
