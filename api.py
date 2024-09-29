from fastapi import FastAPI
import secrets
from servidor import Servidor

app = FastAPI()

users = {} #almacena los usuarios, quien sabe si lo ocupemos.
cookie_jar = []
@app.get("/")
async def root():
    return {"message": "Bienvenido a Ahorcado multijugador!"}

@app.post("/sign_up")
async def sign_up(username, password): #Primero registrate para que pueda crear la cookie
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

@app.post("/sign_in")
async def sign_in(cookie): #Una vez registrado ya solo necesitamos la cookie para saber quien es y validarlo
    
    user = ""
    for galletita in cookie_jar:
        if cookie == galletita["cookie_id"]:
            username = galletita["username"]
            Servidor.agrega_jugador(username)
            return{"message": "Successful loggin"}
    
    
    return {"message": "Not Found User"}


