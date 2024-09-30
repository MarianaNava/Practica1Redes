from socket import *
import json

serverName = 'localhost' # 127.0.0.1 (referencia a mi misma maquina)
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM) # SOCK_DGRAM para decir que vamos a usar UDP

def socket_sign_up():
    username = input('Introduce tu username: ')
    password = input('Introduce tu contraseña: ')
    dictmensaje = dict(username=username,password=password,tipo=0)
    mensajejson = json.dumps(dictmensaje)
    clientSocket.sendto(mensajejson.encode(),(serverName, serverPort)) # encode para pasarlo a una secuencia de bytes
    respuesta, serverAddress = clientSocket.recvfrom(2048)
    mensaje_respuesta = json.loads(respuesta) #Debe responde algo de tipo {"messaje": ... , "cookie":...}
    clientSocket.close()
    return mensaje_respuesta 


def socket_sign_in(cookie):
    dictmensaje = dict(cookie= cookie,tipo=1)
    mensajejson = json.dumps(dictmensaje)
    clientSocket.sendto(mensajejson.encode(),(serverName, serverPort)) # encode para pasarlo a una secuencia de bytes
    respuesta, serverAddress = clientSocket.recvfrom(2048)
    mensaje_respuesta = json.loads(respuesta) #Debe responde algo de tipo {"messaje": ... }
    clientSocket.close()
    return mensaje_respuesta 

def socket_ahorcado_inicial():
    dictmensaje = dict(tipo=2)
    mensajejson = json.dumps(dictmensaje)
    clientSocket.sendto(mensajejson.encode(),(serverName, serverPort)) # encode para pasarlo a una secuencia de bytes
    respuesta, serverAddress = clientSocket.recvfrom(2048)
    mensaje_respuesta = json.loads(respuesta) #Debe responde algo de tipo {"messaje": ... }
    clientSocket.close()
    return mensaje_respuesta 

def socket_movimiento():
    movimiento = input('Dame una letra: ')
    dictmensaje = dict(movimiento= movimiento,tipo=3)
    mensajejson = json.dumps(dictmensaje)
    clientSocket.sendto(mensajejson.encode(),(serverName, serverPort)) # encode para pasarlo a una secuencia de bytes
    respuesta, serverAddress = clientSocket.recvfrom(2048)
    mensaje_respuesta = json.loads(respuesta) #Debe responde algo de tipo {"messaje": ... , "cookie":...}
    clientSocket.close()
    return mensaje_respuesta 


def __main__():
    estados_error = [
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
    peticion_sign_up = socket_sign_up()
    mensaje_cuerpo = peticion_sign_up["message"]
    print(mensaje_cuerpo)
    username_invalid:bool
    cookie:str
    if mensaje_cuerpo == "User alredy exist":
        print(mensaje_cuerpo)
        username_invalid = True
    else:
        username_invalid = False
        cookie = peticion_sign_up["cookie_id"]

    while username_invalid:
        print("Elige otro username")
        nueva_peticion = socket_sign_up()
        mensaje_cuerpo = nueva_peticion["message"]
        print(mensaje_cuerpo)
        if mensaje_cuerpo == "User registered successfully":
            username_invalid = False
            cookie = nueva_peticion["cookie_id"]

    #para este punto ya debe esta asignada la cookie 

    peticion_sign_in = socket_sign_in(cookie) #Hacemos la llamada para hacer sign in con la cookie.
    succesful_sign_in = peticion_sign_in["message"]
    print(succesful_sign_in)
    if succesful_sign_in == "Successful loggin":
        peticion_ai= socket_ahorcado_inicial()
        if peticion_ai["message"]=="Jugador 1":
            jugador1= peticion_ai["jugador1"]
            username1 = jugador1["username"]
            progreso1 = jugador1["progreso"]
            errores = jugador1["errores"]
            colgado = estados_error[errores]
            print("Hola Jugador 1: "+username1)
            print("Tu progreso actual es : "+ progreso1)
            print("Colgado actual"+colgado)
            socket_movimiento()

            



    

