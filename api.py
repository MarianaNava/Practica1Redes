#from fastapi import FastAPI
import secrets
from juego_ahorcado import Jugada_actual
import ast

#app = FastAPI()

users = {} #almacena los usuarios, quien sabe si lo ocupemos.
cookie_jar = []
#@app.get("/")
#async def root():
#    return {"message": "Bienvenido a Ahorcado multijugador!"}



def sign_up(username, password): #Primero registrate para que pueda crear la cookie
    user = users.get(username)
    if user:
        return{"message": "User alredy exist"}
    
    new_user_id = len(users) + 1
    new_user = {
        "username": username,
        "password": password,
        "user_id": new_user_id
    }
    users[username] = new_user
    cookie_id = secrets.token_urlsafe(16) 
    new_cookie = {"username": username, "cookie_id": cookie_id }
    cookie_jar.append(new_cookie)
    return {"message": "User registered successfully", "cookie_id": cookie_id }


def sign_in(cookie): #Una vez registrado ya solo necesitamos la cookie para saber quien es y validarlo
    
    user = ""
    for galletita in cookie_jar:
        if cookie == galletita["cookie_id"]:
            username = galletita["username"]
            #hacer redirect con estado inicial del juego
            jugada_actual = Jugada_actual() #Iniciamos la jugada
            jugada_actual.agrega_jugador(username)
             
            return{"message": "Successful loggin"}
  
    return {"message": "Not Found User"}

#Función que guarda el estado actual de la partida, donde esta se describe en forma de diccionario
def guarda_estado(estado_actual):
    with open("solucion.txt", "w") as myfile:
        myfile.write(estado_actual)
#Función que dado un estado que leerá del archivo solucion.txt realiza una nueva instancia del juego
def lee_juego_actual():
    with open("solucion.txt", "r") as myfile:
        estado = myfile.read()
        estado = ast.literal_eval(estado)

def jugada_estado(letra= ""):
    #Estado posible para el mensaje de regreso:
    #{
    # "juego": {
    # "jugador1": {
    #   "username": username
    #   "estado": ganador/perdedor/continua,
    #   "progreso": La palabra adivinada hasta el momento,
    #   "errores": Número que representa la cantidad de errores que lleva,donde los posibles valores van del 0..6.
    # }, 
    # "jugador2": {
    #   "username": username
    #   "estado": ganador/perdedor/continua,
    #   "progreso": La palabra adivinada hasta el momento,
    #   "errores": Número que representa la cantidad de errores que lleva,donde los posibles valores van del 0..6.
    # }, 
    # "siguiente_jugador": El jugador con el tiro siguiente.
    # "estado_partida": finalizada, continua, no_disponible
    # }
    #}
    instance_jugada_actual= Jugada_actual()#se guarda el mensaje inicial()
    jugada_actual = lee_juego_actual()
    instance_jugada_actual.sobreescribir_juego(jugada_actual)
    if jugada_actual['juego']["estado_partida"] == "no disponible":
        return {"message": "No_disponible"}
    
    elif jugada_actual['juego']["estado_partida"] == "finalizada":
        datos_jugador1 = jugada_actual["juego"]["jugador1"]
        datos_jugador2 = jugada_actual["juego"]["jugador2"]

        if(datos_jugador1["estado"]=="perdedor" and datos_jugador2["estado"]=="perdedor"):
            return {"message":"Perdida"}
        elif(datos_jugador1["estado"]=="ganador" and datos_jugador2["estado"]=="ganador"):
            return {"message":"Empate"}
        elif (datos_jugador1["estado"]=="ganador"):
            username = datos_jugador1["username"]
            return {"message": "Ganador1", "username":username}
        else :
            username = datos_jugador2["username"]
            return {"message": "Ganador2", "username":username}
        
    else: #la partida continua ie. jugada_actual["estado_partida"]=="continua"
        #Si tenemos una accion a realizar, la realizamos 
        if len(letra)>0:

            jugada = jugada_actual.jugada(letra)
            juego_actual = jugada["juego"] #siempre nos regresan algo de tipo juego con el estado del juego actual, turno siguiente y los valores de los jugadores
        return {"message":"Continua","juego": juego_actual}
    

    
    


