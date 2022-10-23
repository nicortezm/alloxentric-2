
import logging
#import terceros
from flask import session, request, jsonify
from flask_restful import Resource, reqparse
from mongoengine.context_managers import switch_db
from pydub import AudioSegment, silence
# Import del sistema
from src.resources.auth.authorization import Auth
from src.resources.auth.dbDecorator import dbAccess


# Imports propios
from src.models.api_models import M_Noise

logger = logging.getLogger(__name__)


class Endpoint_noise(Resource):  # Clase para crear recursos REST
    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def post(self):
        # Audio request
        req_audio = request.files['files']
        extension = req_audio.filename.split(".")[-1]

        if extension == "mp3" or extension == "wav":
            audio = AudioSegment.from_file(req_audio, extension)
        else:
            return {'msg': 'Formato no compatible, Pruebe con .mp3 y .wav',
                    "extension": extension}

        detect = silence.detect_nonsilent(
            audio, min_silence_len=700, silence_thresh=audio.dBFS-1, seek_step=1)

        audio_duration = float('%.3f' % audio.duration_seconds)
        if detect:
            # Detectar silencio en segundos, para esto puedes dividir por 1000 para convertir de ms a s
            ranges = [((start / 1000), (stop / 1000))
                      for start, stop in detect]
            # Retorna tuplas con rangos de silencios detectados (start, stop)
            total = 0
            for tuple in ranges:
                # Obtener el silencio en segundos (stop - start)
                seconds = tuple[1]-tuple[0]
                # Sumar el silencio en segundos
                total += seconds
            precentage = float('%.3f' % (total * 100 / audio_duration))
        else:
            return {"msg": "Error al procesar audio, porfavor comunicar a un administrador"}
        try:
            with switch_db(M_Noise, session["dbMongoEngine"]) as my_collection:
                my_model = my_collection(audio_name=req_audio.filename, value=float('%.3f' % total),
                                         percentage=precentage, audio_duration=audio_duration)
                my_model.save()
        except Exception as err:
            logger.error(err)
            return {"msg": "Error al guardar en la base de datos porfavor contactar a un administrador"}
        return my_model.to_json()

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def get(self):

        with switch_db(M_Noise, session["dbMongoEngine"]):
            my_model = M_Noise.objects().all().order_by('-id')[:5]
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
        with switch_db(M_Noise, session["dbMongoEngine"]) as my_model:
            my_obj = my_model.objects(id=data).first()
            if not my_obj:
                return jsonify({'msg': 'Objeto no encontrado'})
            obj = my_obj.to_json()
            my_obj.delete()
        return obj, 200
