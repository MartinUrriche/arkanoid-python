import pygame
import config
import enemigo.enemigo as enemigo
import menus.menu_inicial as menu_inicial
import niveles.nivel_1 as nivel_1
import menus.menu_pausa as menu_pausa
import menus.menu_configuraciones as menu_configuraciones
import menus.menu_victoria as menu_victoria
import menus.scoreboard as scoreboard
import menus.menu_derrota as menu_derrota

pygame.init()

corriendo = True
reloj = pygame.time.Clock()

while corriendo:
    eventos = pygame.event.get()

    # Procesar QUIT global
    for evento in eventos:
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit() 

    # Estados
    if config.estado == "salir":
        pygame.quit()
        exit()

    elif config.estado == "menu_inicial":
        menu_inicial.menu_inicial(eventos)

    elif config.estado == "Nivel_1":
        if not config.nivel_1_cargado:
            config.enemigos = enemigo.generar_grilla(
                filas=1,
                columnas=1,
                x_inicial=80,
                y_inicial=50,
                sep_x=120,
                sep_y=90
            )
            config.nivel_1_cargado = True
        nivel_1.nivel_1(eventos)
    
    elif config.estado == "Menu_pausa":
        menu_pausa.menu_pausa(eventos)
    
    elif config.estado == "Configuraciones":
        menu_configuraciones.menu_configuracion(eventos)
    
    elif config.estado == "Victoria":
        menu_victoria.menu_victoria(eventos)
        
    elif config.estado == "Derrota":
        menu_derrota.menu_derrota(eventos)

    
    elif config.estado == "Scoreboard":
        scoreboard.menu_scoreboard(eventos)

    pygame.display.flip()
    reloj.tick(60)

