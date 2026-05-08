import pygame
import config

ESTADO_MUSICA = {"menu": False}  

def menu_inicial(eventos):

    if not ESTADO_MUSICA["menu"]:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(config.musica_menu)
        pygame.mixer.music.play(-1)   # loop
        ESTADO_MUSICA["menu"] = True  # marcamos que ya está sonando
        config.musica_menu_activa = True

    #fondo
    config.pantalla.blit(config.fondo_menu_inicial_img,(0,0))
    

    # Dibujar botones 
    config.pantalla.blit(config.boton_iniciar_img, config.boton_iniciar)
    config.pantalla.blit(config.boton_salir_img, config.boton_salir_inicial)

    # --- MANEJO DE EVENTOS ---
    for evento in eventos:   # <<< USAMOS LOS EVENTOS QUE LLEGAN
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if config.boton_salir_inicial.collidepoint(evento.pos):
                pygame.mixer.music.stop()
                ESTADO_MUSICA["menu"] = False
                config.musica_menu_activa = False
                print("SALIR")
                config.estado = "salir"

            if config.boton_iniciar.collidepoint(evento.pos):
                # Paramos la musica del menú y cambiamos al nivel.
                pygame.mixer.music.stop()
                ESTADO_MUSICA["menu"] = False
                config.musica_menu_activa = False
                config.estado = "Nivel_1"
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                pygame.mixer.music.stop()
                ESTADO_MUSICA["menu"] = False
                config.musica_menu_activa = False
                config.musica_nivel_iniciada = False
                config.estado = "Nivel_1"

