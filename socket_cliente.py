from socket import *
import json

serverName = 'localhost' # 127.0.0.1 (referencia a mi misma maquina)
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM) # SOCK_DGRAM para decir que vamos a usar UDP
print("hello")

# Función para realizar la comunicación hacia el servidor enviando un mensaje para empezar con un registro de la sesión.
def socket_sign_up():
    username = input('Introduce tu username: ')
    password = input('Introduce tu contraseña: ')
    dictmensaje = dict(username=username,password=password,tipo=0)
    mensajejson = json.dumps(dictmensaje)
    clientSocket.sendto(mensajejson.encode(),(serverName, serverPort)) # encode para pasarlo a una secuencia de bytes
    respuesta, serverAddress = clientSocket.recvfrom(2048)
    mensaje_respuesta = json.loads(respuesta) #Debe responde algo de tipo {"message": ... , "cookie":...}
    return mensaje_respuesta 

# Función para realizar la comunicación hacia el servidor enviando la cookie para comenzar la sesión.
def socket_sign_in(cookie):
    dictmensaje = dict(cookie= cookie,tipo=1)
    mensajejson = json.dumps(dictmensaje)
    clientSocket.sendto(mensajejson.encode(),(serverName, serverPort)) # encode para pasarlo a una secuencia de bytes
    respuesta, serverAddress = clientSocket.recvfrom(2048)
    mensaje_respuesta = json.loads(respuesta) #Debe responde algo de tipo {"message": ... }
    return mensaje_respuesta 

# Función para realizar la comunicación hacia el servidor enviando un mensaje para probar
# si la letra introducida está incluida en la palabra que debe ser adivinada.
def socket_letra():
    letra = input('Dame una letra: ')
    dictmensaje = dict(letra= letra,tipo=2)
    mensajejson = json.dumps(dictmensaje)
    clientSocket.sendto(mensajejson.encode(),(serverName, serverPort)) # encode para pasarlo a una secuencia de bytes
    respuesta, serverAddress = clientSocket.recvfrom(2048)
    mensaje_respuesta = json.loads(respuesta) #Debe responde algo de tipo {"message": ... , "jugador1":...,"jugador2":..., siguiente_jugador:}
    if mensaje_respuesta["message"]=="Finalizado":
        clientSocket.close()
    return mensaje_respuesta 


if __name__== '__main__':
    # Lista de posibles estados del ahorcado, dependiendo de la cantidad de
    # errores que haya tenido el jugador al momento.
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
    if mensaje_cuerpo == "User already exists":
        print(mensaje_cuerpo)
        username_invalid = True
    else:
        username_invalid = False
        cookie = peticion_sign_up["cookie"]

    while username_invalid:
        print("Elige otro username")
        nueva_peticion = socket_sign_up(cookie)
        mensaje_cuerpo = nueva_peticion["message"]
        print(mensaje_cuerpo)
        if mensaje_cuerpo == "User registered successfully":
            username_invalid = False
            cookie = nueva_peticion["cookie"]

    #para este punto ya debe esta asignada la cookie 

    peticion_sign_in = socket_sign_in(cookie) #Hacemos la llamada para hacer sign in con la cookie.
    succesful_sign_in = peticion_sign_in["message"]
    print(succesful_sign_in)
    if succesful_sign_in == "Successful login":
        peticion_a = socket_letra()
        if peticion_a["message"] == "No suficientes usuarios :( ":
            no_suficientes_usuarios = True
            while no_suficientes_usuarios:
                peticion_a = socket_letra()
                if peticion_a["message"]=="Continua":
                    no_suficientes_usuarios = False
        continua = True
        while continua:
            if peticion_a["message"]!="Continua":
                print(peticion_a["message"])
                continua=False
            else:
                if peticion_a["message"]=="Jugador 1":
                    jugador1= peticion_a["jugador1"]
                    username1 = jugador1["username"]
                    progreso1 = jugador1["progreso"]
                    errores1 = jugador1["errores"]
                    colgado1 = estados_error[errores1]
                    print("Hola Jugador 1: "+username1)
                    print("Tu progreso actual es : "+ progreso1)
                    print("Colgado actual"+colgado1)
                else:
                    jugador2= peticion_a["jugador2"]
                    username2 = jugador2["username"]
                    progreso2 = jugador2["progreso"]
                    errores2 = jugador2["errores"]
                    colgado2 = estados_error[errores2]
                    print("Hola Jugador 2: "+username2)
                    print("Tu progreso actual es : "+ progreso2)
                    print("Colgado actual"+colgado2)

    


            



    

