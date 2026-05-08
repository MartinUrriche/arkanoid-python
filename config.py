import pygame

ANCHO, ALTO = 800, 600

pygame.init()
pygame.mixer.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("No es plantas VS zombies")

# Musica
musica_menu = "assets/sonidos/musica_menu.mp3"
MUSICA_NIVEL_1 = "assets/sonidos/musica_nivel_1.mp3"
MUSICA_VICTORIA = "assets/sonidos/musica_victoria.mp3"
MUSICA_PUNTAJE = "assets/sonidos/puntajes.mp3"

#  Efectos de sonido
sonido_inicio_juego = pygame.mixer.Sound("assets/sonidos/zombies_comming.mp3")
sonido_golpe_simple = pygame.mixer.Sound("assets/sonidos/golpe_simple.mp3")
sonido_derrota = pygame.mixer.Sound("assets/sonidos/perdiste.mp3")
sonido_game_over = pygame.mixer.Sound("assets/sonidos/zombies_ganan.mp3")

#fuente
font = pygame.font.SysFont("Arial", 30)

# Estado global del juego
estado = "menu_inicial"

# Botones menú inicial
boton_iniciar_img = pygame.image.load('assets/img botones/boton.iniciar.png').convert_alpha()
boton_iniciar = boton_iniciar_img.get_rect(center = (ANCHO // 2, ALTO // 2 - 50))


boton_salir_img = pygame.image.load('assets/img botones/boton.salir.png').convert_alpha()
boton_salir_inicial = boton_salir_img.get_rect(center=(ANCHO // 2, ALTO // 2 + 50))

#fondo imagen menu incial
fondo_menu_inicial_img = pygame.image.load('assets/img fondos/maxresdefault.jpg').convert_alpha()
fondo_menu_inicial_img = pygame.transform.scale(fondo_menu_inicial_img, (ANCHO, ALTO))

#Fondo imagen menu pausa
fondo_menu_pausa_img = pygame.image.load('assets/img fondos/fondo_pausa.jpg').convert_alpha()
fondo_menu_pausa_img = pygame.transform.scale(fondo_menu_pausa_img,(ANCHO, ALTO))

#botones menu pausa
boton_jugar_img = pygame.image.load('assets/img botones/boton.jugar.png').convert_alpha()
boton_jugar = boton_jugar_img.get_rect(center = (ANCHO // 2, ALTO // 2 - 50))

boton_salir_pausa_img = pygame.image.load('assets/img botones/boton.salir.png').convert_alpha()
boton_salir_pausa = boton_salir_pausa_img.get_rect(center=(ANCHO // 2, ALTO // 2 + 100))

# boton configuraciones
boton_configuraciones_img = pygame.image.load('assets/img botones/boton.configuraciones.png').convert_alpha()
boton_configuraciones = boton_configuraciones_img.get_rect(center = (ANCHO // 2, ALTO // 2 + 25))

#Fondo configuraciones
fondo_configuraciones_img = pygame.image.load('assets/img fondos/fondo_pausa.jpg').convert_alpha()
fondo_configuraciones_img = pygame.transform.scale(fondo_configuraciones_img, (ANCHO,ALTO))

#FONDO NIVEL_1
fondo_nivel_1 = pygame.image.load('assets/img personajes/kindpng_1950544.png').convert_alpha()
fondo_nivel_1 = pygame.transform.scale(fondo_nivel_1, (ANCHO, ALTO))

#girasol imagen
girasol_img = pygame.image.load('assets/img personajes/Girasol 2.1.png')
girasol_img = pygame.transform.scale(girasol_img, (100, 100))
girasol_superficie = girasol_img.get_rect(center = (ANCHO // 2, ALTO // 2 + 200))

#PELOTA IMAGEN
pelota_img = pygame.image.load('assets/img personajes/bala.png')
pelota_img = pygame.transform.scale(pelota_img, (20,20))
pelota_superficie = pelota_img.get_rect(center = (ANCHO // 2, girasol_superficie.top))
velocidad_pelota = [3, -3]
pelota_lanzada = False

#Vidas imagen
corazon_img = pygame.image.load('assets/img corazones/corazon.png')
corazon_img = pygame.transform.scale(corazon_img, (30,30))
corazones_superficie = [
    corazon_img.get_rect(topleft = (30, 10)),
    corazon_img.get_rect(topleft = (60, 10)),
    corazon_img.get_rect(topleft = (90, 10))
    ]
cantidad_vidas = 3

#Botones menú principal
boton_niveles  = pygame.Rect(300, 200, 200, 60)
boton_opciones = pygame.Rect(300, 280, 200, 60)
boton_creditos = pygame.Rect(300, 360, 200, 60)
boton_salir    = pygame.Rect(300, 440, 200, 60)

#Guardar nivel
nivel_guardado = {
    "pelota_pos": None,
    "velocidad_pelota": None,
    "pelota_lanzada": None,
    "personaje_posicion": None
}

#creacion de enemigo
enemigos = []
nivel_1_cargado = False
def crear_bloque(x, y, tipo):
    bloque = {}

    if tipo == 1:
        bloque["vidas"] = 1
        bloque["imagenes"] = [
            'assets/img personajes/zombie_base.png'
        ]

    elif tipo == 2:
        bloque["vidas"] = 2
        bloque["imagenes"] = [
            'assets/img personajes/zombie_2.png',
            'assets/img personajes/zombie_base.png'
        ]

    elif tipo == 3:
        bloque["vidas"] = 3
        bloque["imagenes"] = [
            'assets/img personajes/zombie_3.png',
            'assets/img personajes/zombie_3_1.png',
            'assets/img personajes/zombie_base.png'
        ]

    # primera img cargada
    imagen_original = pygame.image.load(bloque["imagenes"][0]).convert_alpha()

    ancho = imagen_original.get_width() // 2
    alto = imagen_original.get_height() // 2

    bloque["imagen"] = pygame.transform.scale(imagen_original, (ancho, alto))
    bloque["rect"] = bloque["imagen"].get_rect(topleft=(x, y))
    bloque["indice_imagen"] = 0
    bloque["visible"] = True

    return bloque

#fondo victoria
fondo_victoria_img = pygame.image.load('assets/img ganaste/plants-vs-zombies-background-jkn7bebm6m8h7dzc.jpg').convert_alpha()
fondo_victoria_img = pygame.transform.scale(fondo_victoria_img, (ANCHO, ALTO))

#Fondo derrota
fondo_game_over_img = pygame.image.load("assets/img game over/Plants_vs._Zombies_1_Game_Over.webp").convert_alpha()
fondo_game_over_img = pygame.transform.scale(fondo_game_over_img, (ANCHO, ALTO))
tiempo_game_over = None


#tiempo en el que se mantiene en la pantalla de victoria
tiempo_victoria = None

#puntaje
puntaje = 0
puntaje_actual = 0

# Imagen de fondo del scoreboard
scoreboard_img = pygame.image.load('assets/img scoreboard/Captura.jpg').convert_alpha()
scoreboard_img = pygame.transform.scale(scoreboard_img, (ANCHO, ALTO))
# Estado interno del scoreboard
scoreboard_estado = "input"   # "input" para escribir nombre, "mostrar" para ver el ranking
tiempo_scoreboard = None      # para contar los 5 segundos cuando se muestra el ranking


# Fuente para escribir el nombre en el scoreboard
scoreboard_font = pygame.font.SysFont("Courier", 28, bold=True)

# aca se guarda el aka
scoreboard_aka = ""

# la ruta donde se guarda el json
RUTA_JSON = "scoreboard.json"


#   Banderas de control de música / eventos
musica_nivel_iniciada = False   # para que el inicio (sound) se reproduzca solo 1 vez al entrar al nivel
musica_menu_activa = False      # para no reiniciar música del menú cada frame
musica_score_activa = False     # para el scoreboard
