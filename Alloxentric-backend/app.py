'''
API de ejemplo
'''
from os import getenv

from dotenv import load_dotenv
from flask_restful import Api  # importamos la libreria para crear recursos REST
from flask_cors import CORS  # biblioteca para configurar cors
from config import app  # de aqui se obtienen configuraciones
# from v1.resources.routes import initialize_routes  # importamos las rutas
from src.resources.routes import initialize_routes

# Flask restful con errores personalizados
CORS(app)  # configuramos cors
api = Api(app)  # instanciamos el api

load_dotenv()

initialize_routes(api)  # inicializamos las rutas
if __name__ == '__main__':
    # inicializamos el servidor flask con el puerto 4043
    # (este puerto debe ser cambiado al momento de probar en maquina de desarrollo)
    app.run(host=getenv("APP_HOST"), port=getenv("APP_PORT"), debug=True)
