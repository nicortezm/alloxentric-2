# obtenemos la clase del recurso que tenemos en el archivo example.py para utilizarlo en un endpoint
#from v1.resources.example.example import Role

from src.resources.api.silence_api import Endpoint_final_silence, Endpoint_wait_time, Endpoint_total_silence
from src.resources.api.noise_api import Endpoint_noise
from src.resources.api.prediction_api import Endpoint_Trainingtags, Endpoint_Prediction


def initialize_routes(api):
    '''
    En el endpoint le indicamos el recurso keycloak a utilizar
    con el formato "auth:nombrerecurso:explicacion_corta"
    '''
    # Solo se puede ocupar un auth:recurso por endpoint

    api.add_resource(Endpoint_wait_time, '/wait_time', endpoint='auth:inicial',
                     methods=['GET', 'POST', 'DELETE'])
    api.add_resource(Endpoint_final_silence, '/final_silence',
                     endpoint='auth:final', methods=['GET', 'POST', 'DELETE'])
    api.add_resource(Endpoint_total_silence, '/total_silence',
                     endpoint='auth:total', methods=['GET', 'POST', 'DELETE'])
    api.add_resource(Endpoint_noise, '/noise',
                     endpoint='auth:noise', methods=['GET', 'POST', 'DELETE'])
    api.add_resource(Endpoint_Trainingtags, '/training_tag',
                     endpoint='auth:training_tag', methods=['GET', 'POST', 'DELETE'])
    api.add_resource(Endpoint_Prediction, '/prediction',
                     endpoint='auth:prediction', methods=['GET', 'POST', 'DELETE'])
