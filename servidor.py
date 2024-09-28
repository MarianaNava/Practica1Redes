from socket import *
import json
import random

# Validación de sesión y envío de cookies.

# Código ...

# Lógica del juego Ahorcado.

banco_de_palabras = ["cielo", "burbuja", "caracol", "piano", "aspiradora", "mariposa",
                     "pavo", "caramelo", "banjo", "flor", "perfume", "llama",
                     "bicicleta", "estrella", "guitarra", "microscopio", "rompecabezas",
                     "ballena", "submarino", "abeja", "joyero", "gatito", "pirata",
                     "disco", "tornado", "oboe", "uvas", "lentes", "gacela",
                     "brillantina", "equipaje", "cacahuates", "oruga", "colcha",
                     "maracas", "bolsillo", "violonchelo", "reloj", "catedral", "tijera",
                     "tortuga", "nuez", "pantalla", "cometa", "lavanda", "telescopio",
                     "pimienta", "cebra", "bolsa", "cafetera", "vela", "canguro", "fuego",
                     "muelle", "cereza", "taller", "cascada", "lupa", "trompeta", "cactus",
                     "cuadro", "sombra", "pelo", "cena", "bote", "lago", "cuna"]

estados = [
    """
    _____
    |   |
    |
    |
    |
    |
    """,
    """
    _____
    |   |
    |   O
    |
    |
    |
    """,
    """
    _____
    |   |
    |   O
    |   |
    |
    |
    """,
    """
    _____
    |   |
    |   O
    |  /|
    |
    |
    """,
    """
    _____
    |   |
    |   O
    |  /|\\
    |
    |
    """,
    """
    _____
    |   |
    |   O
    |  /|\\
    |  /
    |
    """,
    """
    _____
    |   |
    |   O
    |  /|\\
    |  / \\
    |
    """
]

def transforma_a_lineas(palabra):
    cadena = ""
    for letra in palabra:
        cadena += "_ "
    return cadena[:-1]

# seleccionamos una palabra aleatoria del banco de palabras
palabra_actual = banco_de_palabras[random.randint(0,len(banco_de_palabras))]
errores = 0
progreso_palabra = transforma_a_lineas(palabra_actual)





#mensaje = dict(progreso = La palabra adivinada hasta el momento.
#    estado = estados[errores]
#    juego = "en progreso"
#    siguiente_jugador = El jugador con el tiro siguiente.)



# Recepción de mensajes del cliente y actualización de la partida, con manejo de errores.

# Código ...

# Persistencia de la partida.

# Código ...