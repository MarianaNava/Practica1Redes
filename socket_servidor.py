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
    lista_clientes.append(clientAddress)
    print(f"Se conectó {clientAddress}")
    paquete = json.loads(message)
    tipo_request = paquete["tipo"]
    if tipo_request == 0: #Es sign up
        username = paquete["username"]
        password = paquete["password"]
        sign_up = sign_up(username, password) #regresar un mensaje de sign_up 

        respuesta = dict(mensaje = sign_up.get('message'), cookie = sign_up.get('cookie_id')) 
        serverSocket.sendto(json.dumps(respuesta).encode(),clientAddress)
    elif tipo_request == 1: #Es sign_in
        cookie = paquete["cookie"]
        sign_in = sign_in(cookie)
        respuesta = dict(mensaje = sign_in.get('message'))
        serverSocket.sendto(json.dumps(respuesta).encode(),clientAddress)
    elif tipo_request == 2: #Es la partida inicial.
        inicia_partido = jugada() #regresa algo con un message
        if



