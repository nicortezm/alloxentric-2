from mongoengine import Document
from mongoengine import StringField, FloatField

# Clase Modelo tiempo espera


class M_Wait_time(Document):
    audio_name = StringField()
    value = FloatField()
    percentage = FloatField()
    audio_duration = FloatField()

    def to_json(self):
        return {
            "_id": str(self.pk),
            "audio_name": self.audio_name,
            "value": self.value,
            "percentage": self.percentage,
            "audio_duration": self.audio_duration
        }

# Clase Modelo silencio final


class M_Final_silence(Document):
    audio_name = StringField()
    value = FloatField()
    percentage = FloatField()
    audio_duration = FloatField()

    def to_json(self):
        return {
            "_id": str(self.pk),
            "audio_name": self.audio_name,
            "value": self.value,
            "percentage": self.percentage,
            "audio_duration": self.audio_duration
        }

# Clase Modelo silencio total


class M_Total_silence(Document):
    audio_name = StringField()
    value = FloatField()
    percentage = FloatField()
    audio_duration = FloatField()

    def to_json(self):
        return {
            "_id": str(self.pk),
            "audio_name": self.audio_name,
            "value": self.value,
            "percentage": self.percentage,
            "audio_duration": self.audio_duration
        }

# Clase Modelo ruido


class M_Noise(Document):
    audio_name = StringField()
    value = FloatField()
    percentage = FloatField()
    audio_duration = FloatField()

    def to_json(self):
        return {
            "_id": str(self.pk),
            "audio_name": self.audio_name,
            "value": self.value,
            "percentage": self.percentage,
            "audio_duration": self.audio_duration
        }

# Clase Modelo predicciones


class M_Training_Tags(Document):
    audio_name = StringField()
    gender = StringField()
    age_range = StringField()

    def to_json(self):
        return {
            "_id": str(self.pk),
            "audio_name": self.audio_name,
            "gender": self.gender,
            "age_range": self.age_range,
        }


class M_Prediction(Document):
    audio_name = StringField()
    gender = StringField()
    age_range = StringField()

    def to_json(self):
        return {
            "_id": str(self.pk),
            "audio_name": self.audio_name,
            "gender": self.p_gender,
            "age_range": self.p_age_range,
        }
