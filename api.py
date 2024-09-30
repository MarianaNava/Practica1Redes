#from fastapi import FastAPI
import secrets
from servidor import Juego_ahorcado
from servidor import Jugada_actual

#app = FastAPI()

users = {} #almacena los usuarios, quien sabe si lo ocupemos.
cookie_jar = []
#@app.get("/")
#async def root():
#    return {"message": "Bienvenido a Ahorcado multijugador!"}

#@app.post("/sign_up")
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

#@app.post("/sign_in")
def sign_in(cookie): #Una vez registrado ya solo necesitamos la cookie para saber quien es y validarlo
    
    user = ""
    for galletita in cookie_jar:
        if cookie == galletita["cookie_id"]:
            username = galletita["username"]
            Jugada_actual.agrega_jugador(username)
            #hacer redirect con estado inicial del juego
             
            return{"message": "Successful loggin"}
  
    return {"message": "Not Found User"}

#@app.get("/jugada")
def jugada(letra:None, jugador:None):
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
    jugada_actual = Jugada_actual() 
    datos_jugador1 = jugada_actual["juego"]["jugador1"]
    datos_jugador2 = jugada_actual["juego"]["jugador2"]
    if jugada_actual["estado_partida"] == "no_disponible":
        return {"message": "no_disponible"}
    
    elif jugada_actual["estado_partida"] == "finalizada":

        if(datos_jugador1["estado"]=="perdedor" and datos_jugador2["estado"]=="perdedor"):
            return {"message":"Perdida"}
        elif(datos_jugador1["estado"]=="ganador" and datos_jugador2["estado"]=="ganador"):
            return {"message":"Empate"}
        elif (datos_jugador1["estado"]=="Ganador"):
            username = datos_jugador1["username"]
            return {"message": "Ganador1", "username":username}
        else :
            username = datos_jugador2["username"]
            return {"message": "Ganador2", "username":username}
    else: #la partida continua 
        return {"message":"Continua","jugador1": datos_jugador1,"jugador2": datos_jugador2}
    




        return{}


