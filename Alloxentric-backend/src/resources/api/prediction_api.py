
import logging
#import terceros
from flask import session, request, jsonify
from flask_restful import Resource
from mongoengine.context_managers import switch_db
# Import del sistema
from src.resources.auth.authorization import Auth
from src.resources.auth.dbDecorator import dbAccess

# Imports propios
from src.models.api_models import M_Training_Tags, M_Prediction

logger = logging.getLogger(__name__)


class Endpoint_Trainingtags(Resource):  # Clase para crear recursos REST
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def post(self):
        # Audio request
        req_audio = request.files['files']

        if req_audio.filename.endswith("mp3") or req_audio.filename.endswith("wav"):
            # hacer algo
            print("TODO: algo")
        else:
            return {'msg': 'Formato no compatible, Pruebe con .mp3 y .wav'}

        gender = request.form.get("gender")
        age = request.form.get("age_range")
        try:
            with switch_db(M_Training_Tags, session["dbMongoEngine"]) as my_collection:
                my_model = my_collection(audio_name=req_audio.filename, gender=gender,
                                         age_range=age)
                my_model.save()
        except Exception as err:
            logger.error(err)
        return my_model.to_json()

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def get(self):

        with switch_db(M_Training_Tags, session["dbMongoEngine"]):
            my_model = M_Training_Tags.objects().order_by('-id')[:5]
            context = []
            for m in my_model:
                context.append(m.to_json())
            if my_model:
                return context, 200
        return {"msg": "No se han encontrado registros"}, 404

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def delete(self):
        data = request.form.get("id")
        obj = ""
        with switch_db(M_Training_Tags, session["dbMongoEngine"]) as my_model:
            my_obj = my_model.objects(id=data).first()
            if not my_obj:
                return jsonify({'msg': 'Objeto no encontrado'})
            obj = my_obj.to_json()
            my_obj.delete()
        return obj, 200


class Endpoint_Prediction(Resource):  # Clase para crear recursos REST
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def post(self):
        # Audio request
        req_audio = request.files['files']

        if req_audio.filename.endswith("mp3") or req_audio.filename.endswith("wav"):
            # hacer algo
            print("TODO: algo")
        else:
            return {'msg': 'Formato no compatible, Pruebe con .mp3 y .wav'}

        gender = "MALE 95%"
        age = ">45 85%"
        try:
            with switch_db(M_Prediction, session["dbMongoEngine"]) as my_collection:
                my_model = my_collection(audio_name=req_audio.filename, gender=gender,
                                         age_range=age)
                my_model.save()
        except Exception as err:
            logger.error(err)
        return my_model.to_json()

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def get(self):

        with switch_db(M_Prediction, session["dbMongoEngine"]):
            my_model = M_Prediction.objects().all().order_by('-id')[:5]
            context = []
            for m in my_model:
                context.append(m.to_json())
            if my_model:
                return context, 200
        return {"msg": "No se han encontrado registros"}, 404

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def delete(self):
        data = request.form.get("id")
        obj = ""
        with switch_db(M_Prediction, session["dbMongoEngine"]) as my_model:
            my_obj = my_model.objects(id=data).first()
            if not my_obj:
                return jsonify({'msg': 'Objeto no encontrado'})
            obj = my_obj.to_json()
            my_obj.delete()
        return obj, 200
