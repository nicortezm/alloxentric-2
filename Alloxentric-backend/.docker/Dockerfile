FROM python:3.8-slim-buster

WORKDIR /opt/alloxentric

COPY ./requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
EXPOSE 5050

COPY . .

CMD ["python3", "app.py"]
#CMD ["gunicorn", "wsgi:app", "-w", "1", "--worker-class", "eventlet", "-b", "0.0.0.0:5050", "--timeout", "60", "--log-config", "log.conf"]  