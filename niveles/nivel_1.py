import pygame
import config
import enemigo.enemigo as enemigo

pygame.mixer.init()

def reiniciar_nivel():
    # Pelota quieta, en posición inicial 
    config.pelota_superficie.centerx = config.girasol_superficie.centerx
    config.pelota_superficie.bottom = config.girasol_superficie.top

    # Velocidad original del nivel
    config.velocidad_pelota = [3, -3]
 
    # bandera de si la pelota fue lanzada
    config.pelota_lanzada = False


def nivel_1(eventos):

     # --- CONTROL DE SONIDO DEL NIVEL ---
    if not config.musica_nivel_iniciada:
        # Reproducir sonido inicial una sola vez
        canal = config.sonido_inicio_juego.play()
        if canal:
            canal.set_endevent(pygame.USEREVENT + 10)
        config.musica_nivel_iniciada = True


    # Cuando termina el sonido de inicio, comienza música del nivel
    for evento in eventos:
        if evento.type == pygame.USEREVENT + 10:
            # Solo cargar música si no está sonando
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.load(config.MUSICA_NIVEL_1)
                pygame.mixer.music.play(-1)

            # Limpiamos el evento
            pygame.event.clear(pygame.USEREVENT + 10)
    
    # Fondo del nivel
    config.pantalla.blit(config.fondo_nivel_1, (0, 0))

    # dibujar enemigo
    for bloque in config.enemigos:
        enemigo.dibujar_bloque(bloque)

    #Dibujar corazon
    for corazon in config.corazones_superficie:
        config.pantalla.blit(config.corazon_img, corazon)

    # Dibujar girasol
    config.pantalla.blit(config.girasol_img, config.girasol_superficie)

    # Mantener pelota arriba del girasol
    if config.pelota_lanzada == False:
        config.pelota_superficie.centerx = config.girasol_superficie.centerx
        config.pelota_superficie.bottom = config.girasol_superficie.top

    # Dibujar pelota
    config.pantalla.blit(config.pelota_img, config.pelota_superficie)

    # Texto puntaje
    texto = config.font.render(f"Puntaje: {config.puntaje}", True, (255, 255, 255))
    config.pantalla.blit(texto, (config.ANCHO - 200 , config.ALTO - 50))

    # ------ PROCESAR EVENTOS ------
    for evento in eventos:

        if evento.type == pygame.QUIT:
            config.estado = "salir"
        
        # Menu pausa
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                config.nivel_guardado["pelota_pos"] = config.pelota_superficie.topleft
                config.nivel_guardado["velocidad_pelota"] = config.velocidad_pelota.copy()
                config.nivel_guardado["pelota_lanzada"] = config.pelota_lanzada
                config.nivel_guardado["personaje_posicion"] = config.girasol_superficie.topleft
                config.estado = "Menu_pausa"

        # Lanzar pelota con click
        if evento.type == pygame.MOUSEBUTTONDOWN and config.pelota_lanzada == False:
            config.pelota_lanzada = True

    teclas = pygame.key.get_pressed()

    # ------ LÓGICA DE LA PELOTA ------
    if config.pelota_lanzada:

        # Movimiento
        config.pelota_superficie.x += config.velocidad_pelota[0]
        config.pelota_superficie.y += config.velocidad_pelota[1]

        # Rebotes contra las paredes
        if config.pelota_superficie.left <= 0 or config.pelota_superficie.right >= config.ANCHO:
            config.velocidad_pelota[0] *= -1

        if config.pelota_superficie.top <= 0:
            config.velocidad_pelota[1] *= -1

        # Movimiento del girasol (solo cuando la pelota ya fue lanzada)
        if teclas[pygame.K_LEFT] and config.girasol_superficie.left > 0:
            config.girasol_superficie.x -= 7
        if teclas[pygame.K_RIGHT] and config.girasol_superficie.right < config.ANCHO:
            config.girasol_superficie.x += 7
        
        # Rebote con el girasol
        if config.pelota_superficie.colliderect(config.girasol_superficie):
            config.pelota_superficie.bottom = config.girasol_superficie.top
            config.velocidad_pelota[1] *= -1

        # Colisión con los zombies (rebote correcto según lado)
        for bloque in config.enemigos:
            if bloque["visible"] and config.pelota_superficie.colliderect(bloque["rect"]):

                # Centros para calcular el lado del impacto
                centro_pelota_x = config.pelota_superficie.centerx
                centro_pelota_y = config.pelota_superficie.centery
                centro_bloque_x = bloque["rect"].centerx
                centro_bloque_y = bloque["rect"].centery

                dx = centro_pelota_x - centro_bloque_x
                dy = centro_pelota_y - centro_bloque_y

                # Decidir si el rebote es horizontal o vertical
                if abs(dx) > abs(dy):
                    # Rebote lateral
                    config.velocidad_pelota[0] *= -1
                    if dx > 0:
                        config.pelota_superficie.left = bloque["rect"].right
                    else:
                        config.pelota_superficie.right = bloque["rect"].left
                else:
                    # Rebote vertical
                    config.velocidad_pelota[1] *= -1
                    if dy > 0:
                        config.pelota_superficie.top = bloque["rect"].bottom
                    else:
                        config.pelota_superficie.bottom = bloque["rect"].top

                # Aplicar daño al zombie
                enemigo.bloquear_recibir_golpe(bloque)
                config.puntaje += 10
                break  # solo un zombie por frame

        # ✅ VICTORIA: si TODOS los bloques ya no están visibles
        todos_invisibles = True

        for b in config.enemigos:
            if b["visible"]:
                todos_invisibles = False
                break

        if todos_invisibles:
            pygame.event.clear()
            pygame.mixer.music.stop()

            pygame.mixer.music.load(config.MUSICA_VICTORIA)
            pygame.mixer.music.play(0)

            # reinicia vidas
            config.cantidad_vidas = 3
            config.corazones_superficie = [
                config.corazon_img.get_rect(topleft=(30, 10)),
                config.corazon_img.get_rect(topleft=(60, 10)),
                config.corazon_img.get_rect(topleft=(90, 10))
            ]

            # resetea la posicion original de la pelota
            config.pelota_lanzada = False
            config.velocidad_pelota = [3, -3]
            config.pelota_superficie.centerx = config.girasol_superficie.centerx
            config.pelota_superficie.bottom = config.girasol_superficie.top

            # zombis nuevos
            config.enemigos.clear()
            config.nivel_1_cargado = False

            #reinicia la musica
            config.musica_nivel_iniciada = False

            config.nivel_1_cargado = False
            config.tiempo_victoria = None
            config.estado = "Victoria"
            return


        # Si toca el suelo pierde
        if config.pelota_lanzada and config.pelota_superficie.bottom >= config.ALTO:
            config.sonido_derrota.play()
            config.cantidad_vidas -= 1

            if config.cantidad_vidas > 0:
                config.corazones_superficie.pop()
                reiniciar_nivel()
                return   # ✅ seguir jugando normalmente

            else:
                # ✅ DERROTA FINAL (RESET TOTAL DE PARTIDA)

                pygame.mixer.music.stop()
                config.sonido_game_over.play()

                # reinicia vidas
                config.cantidad_vidas = 3
                config.corazones_superficie = [
                    config.corazon_img.get_rect(topleft=(30, 10)),
                    config.corazon_img.get_rect(topleft=(60, 10)),
                    config.corazon_img.get_rect(topleft=(90, 10))
                ]

                # resetea la posicion original de la pelota
                config.pelota_lanzada = False
                config.velocidad_pelota = [3, -3]
                config.pelota_superficie.centerx = config.girasol_superficie.centerx
                config.pelota_superficie.bottom = config.girasol_superficie.top

                # zombis nuevos
                config.enemigos.clear()
                config.nivel_1_cargado = False

                #reinicia la musica
                config.musica_nivel_iniciada = False

                #se mueve al la img de la derrota
                config.estado = "Derrota"
                config.tiempo_game_over = pygame.time.get_ticks()
                return



