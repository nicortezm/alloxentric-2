import json
import logging
import os

from functools import wraps
from flask import request, g, session

import requests

from config import AuthConfig

logger = logging.getLogger(__name__)

class Auth():
    Path = os.path.dirname(os.path.realpath(__file__))
    with open(Path+'/scopes.json', encoding='utf-8') as file:
        Scopes = json.load(file)

    @staticmethod
    def authenticate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            method = request.method.upper()
            scope = Auth().Scopes[method]

            #obtenemos el nombre del recurso a utilizar desde la url
            if "auth:" in request.endpoint:
                resource = request.endpoint.split(":")[1]
            else:
                resource = str(request.url_rule)
                if resource.startswith("/"):
                    resource = resource[1:]
                resource = resource.split('/', maxsplit=1)[0]

            #se obtienen las credenciales de keycloak desde el archivo de Configuracion
            grant_type = "password"
            client_id = AuthConfig["ClientID"]
            client_secret = AuthConfig["ClientSecret"]

            # El token siempre debiera venir en el request para este tipo de APIs
            if "Authorization" in request.headers and request.headers["Authorization"].startswith("Bearer "):
                token = request.headers["Authorization"].replace("Bearer ","")


            # En el caso de obtener autentificacion basica de parte del usuario se obtiene el token
            elif request.authorization is not None:
                username = request.authorization.username
                password = request.authorization.password
                res = Auth().get_token(username, password, grant_type, client_id, client_secret)
                if res is not True:
                    #si no se obtiene el token se retorna un codigo de error 401 (unauthorized)
                    return res, 401
                token = g.auth_data["access_token"]

            else:
                # En el caso de no existir un toquen ni una autentificacion basica se envia un
                # mensaje indicando que el usuario no tiene permiso
                response = {'message':'unauthorized'}
                return response, 401
            session["token"] = token
            #se verifica el acceso del usuario al recurso
            res = Auth().get_access(token, client_id, resource, scope)
            if res is True:
                #en el caso de tener permiso se obtiene obtiene la informacion del usuario
                if "user" not in session or not session["user"]:
                    res = Auth().get_info(token) #se obtiene la informacion del usuario
                    if res is not True:
                        return res
                session["resource"] = resource
                res = func(*args, **kwargs)
                return res

            return res
        return wrapper

    @staticmethod
    def get_token(username, password, grant_type, client_id, client_secret):
        '''
        Este método obtiene el token. No se utiliza ya que siempre debería venir.
        '''
        try:
            url = AuthConfig["UrlToken"]
            payload= \
                f'username={username}&password={password}&grant_type={grant_type}' \
                f'&client_id={client_id}&client_secret={client_secret}'
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 200:
                g.auth_data = response.json()
                return True
            logger.warning("Credenciales del usuario invalidas")
        except Exception as ex:
            logger.error("Se ha producido un error al obtener el token: %s", ex)
        return False

    @staticmethod
    def get_info(token):
        # Método para obtener informacion del usuario y guardarla en session
        url = AuthConfig["UrlInfo"]
        payload = {}
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            session["user"] = response.json()
            return True

        logging.warning("Se ha producido un error al obtener la informacion del usuario")
        return response.json()

    @staticmethod
    def get_access(token, client_id, resource, scope):
        #metodo para verificar el acceso del usuario a un recurso
        logger.debug("%s, %s, %s", client_id, resource, scope)
        url = AuthConfig["UrlToken"]
        payload = \
            f'grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Auma-ticket&audience='\
            f'{client_id}&permission={resource}&scope={scope}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            return True

        logger.warning("El usuario no tiene acceso al recurso")
        return response.json()

    @staticmethod
    def test_user(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session["user2"] = {
                "name": "test_user",
                "preferred_username": "system",
                "given_name": "Test",
                "family_name": "Xentric",
                "email": "test@alloxentric.com",
                "groups": ["xentric", ],
                "bdName": "test_db",
                "bdUser": "test_db_user"
            }
            session["token"] = "Dummy_Token"

            if "auth:" in request.endpoint:
                resource = request.endpoint.split(":")[1]
            else:
                resource = str(request.url_rule)
                if resource.startswith("/"):
                    resource = resource[1:]
                resource = resource.split('/', maxsplit=1)[0]
            session["resource"] = resource
            rtn = func(*args, **kwargs)
            session.clear()
            return rtn
        return wrapper
