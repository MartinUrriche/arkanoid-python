import pygame
import config

def menu_derrota(eventos):
    # Dibujar imagen de derrota
    config.pantalla.blit(config.fondo_game_over_img, (0, 0))

    # Iniciar timer la primera vez
    if config.tiempo_game_over is None:
        config.tiempo_game_over = pygame.time.get_ticks()


    # Después de 5 segundos → volver al menú
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - config.tiempo_game_over >= 5000:
        config.estado = "menu_inicial"
        config.tiempo_game_over = None  #reinicia el tiempo de la img a none
        return


