from socket import *
import json
from api import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
print("1")
serverSocket.bind(('', serverPort)) # '' toma como default el localhost
print('El servidor está listo')
lista_clientes = []
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    
    print(f"Se conectó {clientAddress}")
    paquete = json.loads(message)
    tipo_request = paquete["tipo"]
    if tipo_request == 0: #Es sign up
        username = paquete["username"]
        password = paquete["password"]
        instance = sign_up(username, password) #regresar un mensaje de sign_up 

        respuesta = dict(message = instance.get('message'), cookie = instance.get('cookie_id')) 
        serverSocket.sendto(json.dumps(respuesta).encode(),clientAddress)
    elif tipo_request == 1: #Es sign_in
        cookie = paquete["cookie"]
        instance = sign_in(cookie)
        respuesta = dict(message = instance.get('message'))
        serverSocket.sendto(json.dumps(respuesta).encode(),clientAddress)
        lista_clientes.append(clientAddress)
    elif tipo_request == 2: 
        letra = paquete["letra"]
        partido = jugada_estado(letra) #iniciamos la partida,jugada_estado es de api, puede regresar partida no_disponible, finalizada o continua
        #cachamos el mensaje.
        mensaje = partido["message"]
        if mensaje == "Continua":
            partido_juego = partido["juego"]
            jugador1 = partido_juego["jugador1"]
            jugador2 = partido_juego["jugador2"]
            siguiente_jugador = partido_juego["siguiente_jugador"]
            for i in range(2):
                clientAddress = lista_clientes[i] #Quien primero hizo log in esta agregado en la lista de clientes y a su vez se agrega primero a la lista de jugadores

                if i == 0:
                    mensaje = "Jugador 1"
                    respuesta = dict(message= mensaje,jugador1 = jugador1,jugador2= jugador2, siguiente_jugador = siguiente_jugador)
                    serverSocket.sendto(json.dumps(respuesta).encode(), clientAddress)

                else:
                    mensaje = "Jugador 2"
                    respuesta = dict(message= mensaje,jugador1= jugador1,jugador2= jugador2, siguiente_jugador = siguiente_jugador)
                    serverSocket.sendto(json.dumps(respuesta).encode(), clientAddress)

        elif mensaje == "Perdida":
            respuesta = dict(message = "Ambos perdieron T_T")
            serverSocket.sendto(json.dumps(respuesta).encode(), clientAddress)

        elif mensaje == "Empate":
            respuesta = dict(message = "Es un empate!")
            serverSocket.sendto(json.dumps(respuesta).encode(), clientAddress)

        elif mensaje == "Ganador1":
            username = partido["username"]
            respuesta = dict(message = "Gano el usuario:" + username)
            serverSocket.sendto(json.dumps(respuesta).encode(), clientAddress)

        elif mensaje == "Ganador2":
            username = partido["username"]
            respuesta = dict(message ="Gano el usuario:" + username)
            serverSocket.sendto(json.dumps(respuesta).encode(), clientAddress)

        else: #No disponible
            respuesta = dict(message = "No suficientes usuarios :( ")
            serverSocket.sendto(json.dumps(respuesta).encode(), clientAddress)











