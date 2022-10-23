
import logging
#import terceros
from flask import session, request, jsonify
from flask_restful import Resource
from mongoengine.context_managers import switch_db
from pydub import AudioSegment, silence
from src.resources.api.validations import final_silence, total_silence, wait_time
# Import del sistema
from src.resources.auth.authorization import Auth
from src.resources.auth.dbDecorator import dbAccess
from config import app
# Imports propios
from src.models.api_models import M_Wait_time, M_Final_silence, M_Total_silence, M_Noise

logger = logging.getLogger(__name__)
Config = app.config["Parameters_app"]
silence_limit = Config["SilenceDbfsLimit"]
silence_time_duration = Config["SilenceTimeDuration"]


class Endpoint_wait_time(Resource):  # Clase para crear recursos REST
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

        silence_detect = silence.detect_silence(
            audio, min_silence_len=silence_time_duration, silence_thresh=audio.dBFS - silence_limit)

        audio_duration = float('%.3f' % audio.duration_seconds)
        try:
            # Detectar silencio en segundos, para esto puedes dividir por 1000 para convertir de ms a s
            silence_ranges = [((start / 1000), (stop / 1000))
                              # Retorna tuplas con rangos de silencios detectados (start, stop)
                              for start, stop in silence_detect]

            # Tiempo de espera
            initial_silence, initial_percentage = wait_time(
                silence_ranges, audio_duration)

        except:
            initial_silence = initial_percentage = 0.0
        if initial_silence and initial_percentage and audio_duration:
            try:
                with switch_db(M_Wait_time, session["dbMongoEngine"]) as my_collection:
                    my_model = my_collection(audio_name=req_audio.filename,
                                             value=initial_silence, percentage=initial_percentage, audio_duration=audio_duration)
                    my_model.save()
            except Exception as err:
                logger.error(err)
            return my_model.to_json()

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def get(self):

        with switch_db(M_Wait_time, session["dbMongoEngine"]):
            my_model = M_Wait_time.objects().all().order_by('-id')[:5]
            context = []
            for m in my_model:
                context.append(m.to_json())
            if my_model:
                return context, 200
                # return Response(my_model, content_type='application/json')
        return {"msg": "No se han encontrado registros"}, 404

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def delete(self):
        data = request.form.get("id")
        obj = ""
        with switch_db(M_Wait_time, session["dbMongoEngine"]) as my_model:
            my_obj = my_model.objects(id=data).first()
            if not my_obj:
                return jsonify({'msg': 'Objeto no encontrado'})
            obj = my_obj.to_json()
            my_obj.delete()
        return obj, 200


# Arreglar Jorge
class Endpoint_final_silence(Resource):  # Clase para crear recursos REST
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

        silence_detect = silence.detect_silence(
            audio, min_silence_len=silence_time_duration, silence_thresh=audio.dBFS - silence_limit)

        audio_duration = float('%.3f' % audio.duration_seconds)
        try:
            # Detectar silencio en segundos, para esto puedes dividir por 1000 para convertir de ms a s
            silence_ranges = [((start / 1000), (stop / 1000))
                              # Retorna tuplas con rangos de silencios detectados (start, stop)
                              for start, stop in silence_detect]

            # Silencio Final
            silence_final, percentage_final = final_silence(
                silence_ranges, audio_duration)
        except:
            # Si el audio no tiene silencio, inicializa las variables en 0
            silence_final = percentage_final = 0

        try:
            with switch_db(M_Final_silence, session["dbMongoEngine"]) as my_collection:
                my_model = my_collection(audio_name=req_audio.filename,
                                         value=silence_final, percentage=percentage_final, audio_duration=audio_duration)
                my_model.save()
        except Exception as err:
            # logger.error(err)
            return {"msg": "error al guardar en la base de datos."}
        return my_model.to_json()

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def get(self):

        with switch_db(M_Final_silence, session["dbMongoEngine"]):
            my_model = M_Final_silence.objects().all().order_by('-id')[:5]
            context = []
            for m in my_model:
                context.append(m.to_json())
            if my_model:
                return context, 200
                # return Response(my_model, content_type='application/json')
        return {"msg": "No se han encontrado registros"}, 404

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def delete(self):
        data = request.form.get("id")
        obj = ""
        with switch_db(M_Final_silence, session["dbMongoEngine"]) as my_model:
            my_obj = my_model.objects(id=data).first()
            if not my_obj:
                return jsonify({'msg': 'Objeto no encontrado'})
            obj = my_obj.to_json()
            my_obj.delete()
        return obj, 200


class Endpoint_total_silence(Resource):  # Clase para crear recursos REST
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

        silence_detect = silence.detect_silence(
            audio, min_silence_len=silence_time_duration, silence_thresh=audio.dBFS - silence_limit)

        audio_duration = float('%.3f' % audio.duration_seconds)
        if silence_detect:
            # Detectar silencio en segundos, para esto puedes dividir por 1000 para convertir de ms a s
            silence_ranges = [((start / 1000), (stop / 1000))
                              # Retorna tuplas con rangos de silencios detectados (start, stop)
                              for start, stop in silence_detect]
            # Silencio Final
            try:
                silence_total, percentage_total = total_silence(
                    silence_ranges, audio_duration)
            except Exception as err:
                logger.error(err)
                return {"msg": "Error al procesar audio, porfavor comunicar a un administrador"}

        else:
            # Si el audio no tiene silencio, inicializa las variables en 0
            silence_total = percentage_total = 0

        if silence_total and percentage_total and audio_duration:
            try:
                with switch_db(M_Total_silence, session["dbMongoEngine"]) as my_collection:
                    my_model = my_collection(audio_name=req_audio.filename, value=silence_total,
                                             percentage=percentage_total, audio_duration=audio_duration)
                    my_model.save()
            except Exception as err:
                logger.error(err)
            return my_model.to_json()

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def get(self):

        with switch_db(M_Total_silence, session["dbMongoEngine"]):
            my_model = M_Total_silence.objects().all().order_by('-id')[:5]
            context = []
            for m in my_model:
                context.append(m.to_json())
            if my_model:
                return context, 200
                # return Response(my_model, content_type='application/json')
        return {"msg": "No se han encontrado registros"}, 404

    @Auth.authenticate
    @dbAccess.mongoEngineAccess
    def delete(self):
        data = request.form.get("id")
        obj = ""
        with switch_db(M_Total_silence, session["dbMongoEngine"]) as my_model:
            my_obj = my_model.objects(id=data).first()
            if not my_obj:
                return jsonify({'msg': 'Objeto no encontrado'})
            obj = my_obj.to_json()
            my_obj.delete()
        return obj, 200
