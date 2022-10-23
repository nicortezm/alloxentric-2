# pylint: disable=invalid-name
import logging
import os
from datetime import datetime
from functools import wraps
import threading

from flask import request, session
from mongoengine import connect
from pymongo import MongoClient
import requests

from config import app
from src.resources.auth.encript import decrypt


Path = os.path.dirname(os.path.realpath(__file__))
Config = app.config["DbConfig"]
Username = Config["user"]
Password = Config["pass"]
EncriptWord = Config["EncriptWord"]
Host = str(Config["host"]+":"+Config["port"])
MyClient = MongoClient('mongodb://%s:%s@%s' % (Username, Password, Host))

logger = logging.getLogger(__name__)


class dbAccess():
    @staticmethod
    def mongoEngineAccess(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            User = session["user"]
            Group = str(User["bdName"])
            MyDb = MyClient["xentric_db"]
            MyCol = MyDb["clients"]
            Reg = MyCol.find_one({"client": Group})

            if Reg is None:
                DbUser = User["bdUser"]
                data = {"client": Group, "user": DbUser, "bdName": Group}
                MyCol.insert_one(data)
                UserName = ""
                UserLastName = ""
                Email = ""
                if "given_name" in User:
                    UserName = User["given_name"]
                if "family_name" in User:
                    UserLastName = User["family_name"]
                if "email" in User:
                    Email = User["email"]
                MyCol = MyDb["user"]
                Permissions = getPermission(session["token"])

                data = {
                    "client": Group,
                    "user": User["preferred_username"],
                    "name": UserName,
                    "last_name": UserLastName,
                    "email": Email,
                    "permission": Permissions
                }
                MyCol.insert_one(data)
                Pw = decrypt(User["bdPass"], EncriptWord)
                try:
                    MyDb = MyClient[Group]
                    MyCol = MyDb["info"]
                    Data2 = {"client": Group, "creation_date": datetime.now(
                    ), "created_by": User["preferred_username"]}
                    MyCol.insert_one(Data2)
                    MyDb.add_user(DbUser, Pw)
                    resp = connectMongoEngine(Host, Group, DbUser, Pw)
                    session["dbMongoEngine"] = resp
                except Exception as ex:
                    logging.error("error: "+str(ex))
            else:
                dbUser = User["bdUser"]
                Pw = decrypt(User["bdPass"], EncriptWord)
                resp = connectMongoEngine(Host, Group, dbUser, Pw)
                User = session["user"]
                session["dbMongoEngine"] = resp
                User = session["user"]
                Process = threading.Thread(
                    target=addUser, args=(User, session["token"],))
                Process.start()
                Resource = session["resource"]
                IpAddress = request.remote_addr
                Process = threading.Thread(
                    target=addRegister, args=(User, Resource, IpAddress,))
                Process.start()
            res = f(*args, **kwargs)
            return res

        return wrapper


def connectMongoEngine(host, Db, User, Passw):
    User = Username
    Passw = Password

    try:
        logger.debug("%s, %s, %s, %s", host, Db, User, Passw)
        connect(host="mongodb://"+Username+":"+Password +
                "@"+host+"/xentric_db?authSource=admin")
        # connect(alias=f"conne_{Db}",host=f"mongodb://{User}:{Passw}@{host}/{Db}?authSource={Db}")
        connect(
            alias=f"conne_{Db}", host=f"mongodb://{User}:{Passw}@{host}/{Db}?authSource=admin")
        return f"conne_{Db}"
    except Exception as ex:
        logging.error(
            "Se produjo un error al conectar a la base de datos: %s", ex)
        return ""


def getPermission(token):
    url = app.config["AuthConfig"]["UrlToken"]
    payload = 'grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Auma-ticket&audience=flask_api&response_mode=Permissions'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    Response = requests.request("POST", url, headers=headers, data=payload)
    if Response.status_code == 200:
        data = Response.json()
        return data
    return []


def addUser(User, token):
    MyDb = MyClient["xentric_db"]
    MyCol = MyDb["user"]
    group = User["groups"]
    Reg = MyCol.find_one(
        {"$and": [{"client": group[0]}, {"user": User["preferred_username"]}]})
    if Reg is None:
        UserName = ""
        UserLastname = ""
        Email = ""
        if "given_name" in User:
            UserName = User["given_name"]
        if "family_name" in User:
            UserLastname = User["family_name"]
        if "email" in User:
            Email = User["email"]
        Permissions = getPermission(token)
        data = {
            "client": group[0],
            "user": User["preferred_username"],
            "name": UserName,
            "last_name": UserLastname,
            "email": Email,
            "permission": Permissions
        }
        MyCol.insert_one(data)


def addRegister(user, resource, ip):
    MyDb = MyClient["xentric_db"]
    mycol = MyDb["registers"]
    group = user["groups"]
    data = {
        "client": group[0],
        "user": user["preferred_username"],
        "resource": resource,
        "date": datetime.now(),
        "ip_request": ip
    }
    mycol.insert_one(data)
