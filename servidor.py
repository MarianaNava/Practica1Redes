from socket import *
import json
import random

class Juego_ahorcado:

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

    # Pasa la palabra actual a una serie de lineas correspondientes.
    def transforma_a_lineas(self, palabra):
        cadena = ""
        for letra in palabra:
            cadena += "_ "
        return cadena[:-1]

    def __init__(self):
    # seleccionamos una palabra aleatoria del banco de palabras
        self.palabra_actual = self.banco_de_palabras[random.randint(0,len(self.banco_de_palabras)-1)]
        self.errores = 0
        self.progreso_palabra = self.transforma_a_lineas(self.palabra_actual) #Es cuantas posiciones tendra nuestra palabra

    # Función que regresa una lista con las apariciones de una letra en una cadena.
    def apariciones_letra(self, cadena, letra):
        indices = []
        for i in range(len(cadena)):
            if cadena[i] == letra:
                indices.append(i)
        return indices

    # Dada una letra se actualiza la palabra, sustituyendo sus apariciones.
    # Si la letra no aparece, se incrementa la cantidad de errores.
    def actualiza_palabra(self, letra):
        letra = letra.lower()
        apariciones = self.apariciones_letra(self.palabra_actual,letra)
        if apariciones == []:
            self.errores += 1
            return
        for i in apariciones:
            self.progreso_palabra = self.progreso_palabra[: i*2] + letra + self.progreso_palabra[(i*2) + 1:]

    def jugar(self):
        juego = "en progreso"
        #while(True):
            #if self.errores == 6:
            #    juego = "finalizado"
            #    self.jugadores.remove()
            #palabra actual y estado 2 opciones 
            #  mandarselo a una clase controlador 
            #  devolver mensaje {"palabra actual": }

    # Recepción de mensajes del cliente y actualización de la partida, con manejo de errores.

class Jugada_actual:
    # Lista de jugadores involucrados en la partida actual
    jugadores = []
    def agrega_jugador(self,jugador):
        self.jugadores.append(jugador)
    def obten_jugadores(self):
        return self.jugadores
    def __init__(self):
        #Hacemos verificaciones de que esten jugando dos personas
        while len(self.jugadores)<2:
            return 
        
            
            
            

    # Persistencia de la partida.
    #jugadores_actuales = []
    #for jugador in Servidor.obten

    # Código ...