from os import getenv
from dotenv import load_dotenv
from flask import Flask  # importamos la libreria flask


load_dotenv(".env.local")

#=====================Configuraciones keycloak=====================#

################################Recordatorio#############################################
#   las configuraciones que puedan variar de ambiente en ambiente deben                 #
#   ser declaradas con variables de entorno.                                            #
#   Ejemplo:                                                                            #
#          import os                                                                    #
#          BdName = os.getenv('NombreVariableEntorno', 'valor_por_defecto')             #
#                                                                                       #
#   Ademas de estos las configuraciones en este archivo deben ocupar las variables      #
#   de configuraciones de flask.                                                        #
#   Ejemplo:                                                                            #
#           app.config['NombreVariableConfiguracion'] = 'valor_de_configuracion'        #
#                                                                                       #
#########################################################################################


AuthConfig = {
    # cliente Keycloak que utilizara la aplicacion
    "ClientID": str(getenv("KEYCLOAK_CLIENTID")),
    "ClientSecret": str(getenv("KEYCLOAK_CLIENTSECRET")),
    # endpoint para obtener token
    "UrlToken": str(getenv("KEYCLOAK_URLTOKEN")),
    # endpoint para obtener informacion de usuario
    "UrlInfo": str(getenv("KEYCLOAK_URLINFO"))
}

DbConfig = {
    # ip de la base de datos principal de xentric
    "host": str(getenv("BD_HOST")),
    # puerto de la base de datos principal de xentric
    "port": str(getenv("BD_PORT")),
    # usuario de la base de datos principal de xentric
    "user": str(getenv("BD_USER")),
    # contraseña de la base de datos principal de xentric
    "pass": str(getenv("BD_PASS")),
    # palabra clave para encriptacion y desencriptacion
    "EncriptWord": str(getenv("ENCRIPTWORD"))
}

Parameters_app = {
    "SilenceDbfsLimit": int(getenv("SILENCE_LIMIT_DBFS")),
    "SilenceTimeDuration": int(getenv("SILENCE_TIME_DURATION")),
}

app = Flask(__name__)  # instanciamos la aplicacion
# le asignamos la clave secreta
app.secret_key = getenv('FLASK_SECRET_KEY', 'secret_key')
# asignamos la configuracion de keycloak a la aplicacion
app.config['AuthConfig'] = AuthConfig
# asignamos la configuracion de base de datos a la aplicacion
app.config['DbConfig'] = DbConfig
app.config['Parameters_app'] = Parameters_app
