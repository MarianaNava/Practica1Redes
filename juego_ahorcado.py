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
    
    # Pasa la palabra actual a una serie de lineas correspondientes.
    def transforma_a_lineas(self, palabra):
        cadena = ""
        for letra in palabra:
            cadena += "_ "
        return cadena[:-1]

    def __init__(self):
    # seleccionamos una palabra aleatoria del banco de palabras
        self.palabra_actual = self.banco_de_palabras[random.randint(0,len(self.banco_de_palabras)-1)]
        self.errores_j1 = 0
        self.errores_j2 = 0
        self.progreso_palabra_j1 = self.transforma_a_lineas(self.palabra_actual) #Es cuantas posiciones tendra nuestra palabra
        self.progreso_palabra_j2 = self.transforma_a_lineas(self.palabra_actual)

    # Función que regresa una lista con las apariciones de una letra en una cadena.
    def apariciones_letra(self, cadena, letra):
        indices = []
        for i in range(len(cadena)):
            if cadena[i] == letra:
                indices.append(i)
        return indices

    # Dada una letra se actualiza la palabra del jugador 1, sustituyendo sus apariciones.
    # Si la letra no aparece, se incrementa la cantidad de errores.
    def actualiza_palabra_jugador1(self, letra):
        letra = letra.lower()
        apariciones = self.apariciones_letra(self.palabra_actual,letra)
        if apariciones == []:
            self.errores_j1 += 1
            return
        for i in apariciones:
            self.progreso_palabra_j1 = self.progreso_palabra_j1[: i*2] + letra + self.progreso_palabra_j1[(i*2) + 1:]

    # Dada una letra se actualiza la palabra del jugador 2, sustituyendo sus apariciones.
    # Si la letra no aparece, se incrementa la cantidad de errores.
    def actualiza_palabra_jugador2(self, letra):
        letra = letra.lower()
        apariciones = self.apariciones_letra(self.palabra_actual,letra)
        if apariciones == []:
            self.errores_j2 += 1
            return
        for i in apariciones:
            self.progreso_palabra_j2 = self.progreso_palabra_j2[: i*2] + letra + self.progreso_palabra_j2[(i*2) + 1:]


class Jugada_actual:
    # Lista de jugadores involucrados en la partida actual
    jugadores = []
    jugador_turno:int #Variable que indica que jugador le toca tirar, valores 1,2

    jugador_turno = 1
    estado_jugador1 = "continua"
    estado_jugador2 = "continua"
    estado_partida = "continua"

    mensaje_inicial = ""

    def agrega_jugador(self,jugador):
        self.jugadores.append(jugador)

    def obten_jugadores(self):
        return self.jugadores

    def __init__(self):
        #Hacemos verificaciones de que esten jugando dos personas
        while len(self.jugadores)<2:
            self.mensaje_inicial = {"juego": {
                        "jugador1": {
                            "username": "",
                            "estado": "",
                            "progreso": "",
                            "errores": 0
                        }, 
                        "jugador2": {
                            "username": "",
                            "estado": "",
                            "progreso": "",
                            "errores": 0
                        }, 
                        "siguiente_jugador": "",
                        "estado_partida": "no disponible"
                        }
                    }
        
        self.juego = Juego_ahorcado()
        self.jugador1 = self.jugadores[0]
        self.jugador2 = self.jugadores[1]
        self.mensaje_inicial = {"juego": {
                        "jugador1": {
                            "username": self.jugador1,
                            "estado": "continua",
                            "progreso": self.juego.progreso_palabra_j1,
                            "errores": 0
                        }, 
                        "jugador2": {
                            "username": self.jugador2,
                            "estado": "continua",
                            "progreso": self.juego.progreso_palabra_j2,
                            "errores": 0
                        }, 
                        "siguiente_jugador": self.jugador1,
                        "estado_partida": "continua"
                        }
                    }
        
    def dar_mensaje_inicial(self):
        return self.mensaje_inicial
    
    # Actualiza la palabraRegresa la informacion del jugador actualizada
    def jugada(self, letra):
        if self.jugador_turno == 1:
            self.juego.actualiza_palabra_jugador1(letra)
            #Si el jugador tiene 6 errores, entonces pierde.
            if self.juego.errores_j1 >= 6:
                self.estado_jugador1 = "perdedor"
            # Si el jugador tiene menos de 6 errores y ya no hay letras que reemplazar, entonces gana.
            elif self.juego.errores_j1 < 6 and ("_" not in self.juego.progreso_palabra_j1): 
                self.estado_jugador1 = "ganador"
            self.jugador_turno = 2

        elif self.jugador_turno == 2:
            self.juego.actualiza_palabra_jugador2(letra)
            #Si el jugador tiene 6 errores, entonces pierde.
            if self.juego.errores_j2 >= 6:
                self.estado_jugador2 = "perdedor"
            # Si el jugador tiene menos de 6 errores y ya no hay letras que reemplazar, entonces gana.
            elif self.juego.errores_j2 < 6 and ("_" not in self.juego.progreso_palabra_j2): 
                self.estado_jugador2 = "ganador"
            self.jugador_turno = 1

        if((self.estado_jugador1 == "perdedor") and (self.estado_jugador2 == "perdedor")) or (self.estado_jugador1 == "ganador") or (self.estado_jugador2 == "ganador"):
            self.estado_partida = "finalizada"

        return {"juego": {
                        "jugador1": {
                            "username": self.jugador1,
                            "estado": self.estado_jugador1,
                            "progreso": self.juego.progreso_palabra_j1,
                            "errores": self.juego.errores_j1
                            }, 
                        "jugador2": {
                            "username": self.jugador2,
                            "estado": self.estado_jugador2,
                            "progreso": self.juego.progreso_palabra_j2,
                            "errores": self.juego.errores_j2
                            }, 
                        "siguiente_jugador": self.jugador_turno,
                        "estado_partida": self.estado_partida
                        }
                    }

            
            

    # Persistencia de la partida.

    # Código ...