#import os
import threading
import logging

from datetime import datetime
from functools import wraps

import requests
from flask import request, session, g
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

#from .encript import decrypt
from config import AuthConfig, DbConfig


try:
    mongo_uri = f'mongodb://{DbConfig["user"]}:{DbConfig["pass"]}@{DbConfig["host"]}:{DbConfig["port"]}'
    myclient = MongoClient(mongo_uri)
except ConnectionFailure:
    logging.error("Error de conección a Mongo: %s", mongo_uri)

def pymongo_access(func):
    '''
    session["dbPyMongo"] -> Base de datos del cliente (objeto)
    session["user"]["bdName"] -> Nombre de la base de datos del cliente (str)
    session["user"]["bdUser"]
    session["token"] -> Token del usuario entregado por Keycloak

    db["xentric_db"] -> base de datos general de Xentric para todos los clientes
    db["xentric_db"]["clients"] -> Todos los clientes
    db["xentric_db"]["user"] -> Todos los usuarios
    db["xentric_db"]["info"] ?
    db["xentric_db"]["registers"] -> Logs con los accesos a bd
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug(session)
        if "dbPyMongo" not in session or not session["dbPyMongo"]:
            # Si no hay bd asignada a esta sesión, seguir el flujo.
            # Se comienza revisando si el usuario existe en la bd
            user = session["user"]
            group = str(user["bdName"])
            mydb = myclient["xentric_db"]
            qry = {
                "$and": [
                    {"client": group[0]},
                    {"user": user["preferred_username"]}
                ]
            }
            if mydb["user"].count_documents(qry, limit = 1) == 0:
                # Si el usario no existe, se inserta en la colección "user"
                add_user(session["user"], session["token"])

                if mydb["clients"].count_documents({"client": group}, limit = 1) == 0:
                    # Si el cliente no existe, se inserta en la colección "clients"
                    dbUser = user["bdUser"]
                    data = {"client": group, "user": dbUser, "bdName": group}
                    mydb["clients"].insert_one(data)

                    # Se crea registro de quien creó la bd y cuándo
                    mydb = myclient[group]
                    data2 = {
                        "client": group,
                        "creation_date": datetime.now(),
                        "created_by": user["preferred_username"]
                        }
                    mydb["info"].insert_one(data2)

            #session["dbPyMongo"] = myclient[user["bdName"]]
            g.db = myclient[user["bdName"]]

        # Se crea registro de acceso en bd (logs)
        if "auth:" in request.endpoint:
            resource = request.endpoint.replace("auth:", "")
        else:
            resource = str(request.url_rule)
            if resource.startswith("/"):
                resource = resource[1:]
            resource = resource.split('/')
            resource = resource[0]
        ip_address = request.remote_addr
        thr = threading.Thread(target=add_register, args=(session["user"], resource, ip_address,))
        thr.start()

        res = func(*args, **kwargs)

        #session.clear()                  # The required endpoint function is executed.
        return res                       # Returns the value of the function.

    return wrapper


def get_permission(token):
    #FIXME No debería haber ninguna pregunta a Keycloak aquí. Tiene que ser independiente
    url = AuthConfig["UrlToken"]
    audience = AuthConfig["ClientID"]
    payload = \
        f'grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Auma-ticket' \
        f'&audience={audience}&response_mode=permissions'
    headers = {
        'Authorization':'Bearer '+str(token),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        data=response.json()
        return data
    return []


def add_user(user, token):
    '''
    Agrega el usuario a la base de datos si es que no existe
    @param user: Información de usuario
    @param token: token para obtener los permisos del usuario
    '''
    mydb = myclient["xentric_db"]
    group = user["groups"]
    qry = {
        "$and": [
            {"client": group[0]},
            {"user": user["preferred_username"]}
        ]
    }
    if mydb["user"].count_documents(qry, limit = 1) == 0:
        user_name = ""
        user_last_name = ""
        email = ""
        if "given_name" in user:
            user_name = user["given_name"]
        if "family_name" in user:
            user_last_name = user["family_name"]
        if "email" in user:
            email = user["email"]
        data = {
            "client": group[0],
            "user": user["preferred_username"],
            "name": user_name,
            "last_name": user_last_name,
            "email": email,
            "permission": get_permission(token)
        }
        mydb["user"].insert_one(data)

def add_register(user, resource, ip_address):
    '''
    Crea un registro en la bd registers con el
    registro del acceso.
    '''
    mydb = myclient["xentric_db"]
    group = user["groups"]
    data = {
        "client": group[0],
        "user": user["preferred_username"],
        "resource": resource,
        "date": datetime.now(),
        "ip_request": ip_address
    }
    mydb["registers"].insert_one(data)
