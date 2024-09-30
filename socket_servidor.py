from socket import *
import json
from api import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
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
        sign_up = sign_up(username, password) #regresar un mensaje de sign_up 

        respuesta = dict(message = sign_up.get('message'), cookie = sign_up.get('cookie_id')) 
        serverSocket.sendto(json.dumps(respuesta).encode(),clientAddress)
    elif tipo_request == 1: #Es sign_in
        cookie = paquete["cookie"]
        sign_in = sign_in(cookie)
        respuesta = dict(message = sign_in.get('message'))
        serverSocket.sendto(json.dumps(respuesta).encode(),clientAddress)
    elif tipo_request == 2: 

        lista_clientes.append(clientAddress)
        inicia_partido = jugada() #regresa algo con un message

        jugador1 = inicia_partido["jugador1"]
        jugador2 = inicia_partido["jugador2"]
        
        for i in range(2):
            clientAddress = lista_clientes[i]
            if i == 0:
                mensaje = "Jugador 1"
                respuesta = dict(message= mensaje,jugador1= jugador1,jugador2= jugador2)
                serverSocket.sendto(json.dumps(respuesta).encode(), clientAddress)
            else:
                mensaje = "Jugador 2"
                respuesta = dict(message= mensaje,jugador1= jugador1,jugador2= jugador2)
                serverSocket.sendto(json.dumps(respuesta).encode(), clientAddress)




