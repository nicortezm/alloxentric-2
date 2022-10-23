# FLASK_API

Plantilla creada para programar un API flask con los parametros de Alloxentric.

## FLASK_API - Entorno

Se recomienda instalar un entorno virtual de python [(info)](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/):

```python3
pip3 install virtualenv
```

Para crear un entorno virtual:

```python3
mkdir VENV
python3 -m venv VENV
source VENV/bin/activate
```

Una vez dentro podemos instalar las librerias necesarias:

```python3
pip3 install -r requirements.txt
```

## Para iniciar el servidor flask

 ```python3
python3 app.py
```

## En la carpeta V1 se encuentran 3 carpetas

- models: Van las clases, métodos, funciones que se utilizaran en los recursos.
- errors: Van los errores personalizados de los recursos.
- resources: Se agregan todos los recursos de la API y se definen los endpoints

## En la ruta principal se encuentran los archivos

- app.py: Aplicacion principal, donde se define la ip/port del servidor flask, se configura el JWB, etc.
- db.py: Conexion para mongo y sus colecciones.
- errors.py: Definicion de errores.

## Documentación Auth

<https://github.com/alloxentric/KeycloakAuth>

## Iniciar con Ambiente virtual

### Ejecutar los siguientes comandos en el directorio dodne se encuentra el archivo docker-compose.yml

### Cómo construir y ejecutar en primer plano

docker-compose up --build

### Contruir y ejecutar en segundo plano

docker-compose up --build -d

### Verificar estado de contenedores

docker-compose ps

### Detener contenedor

docker-compose down

### Verifique su aplicación en el puerto 9090 en el servidor host donde vive el contenedor si es remoto

<http://172.0.0.67:9090>    <- Ip de servidor

### O localhost si es desarrollo local

<http://localhost:9090> o
<http://127.0.0.1:9090>
