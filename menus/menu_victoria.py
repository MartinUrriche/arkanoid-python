import pygame
import time
import config

def menu_victoria(eventos):
    # Dibujar fondo
    config.pantalla.blit(config.fondo_victoria_img, (0, 0))

    if config.tiempo_victoria is None:
        config.tiempo_victoria = time.time()

    #despues de 5 segundos pasa a pedir el aka(apodo)
    if time.time() - config.tiempo_victoria >= 5:
        config.tiempo_victoria = None
        config.puntaje_actual = config.puntaje
        config.scoreboard_aka = ""   # ✅ habilita escritura nueva
        # detener música de victoria y pasar a scoreboard (scoreboard cargará su propia música)
        pygame.mixer.music.stop()
        config.estado = "Scoreboard"


