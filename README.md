# RANDOM_DATA_WHATSAPP_WEB

Desarrollado en python y qt.

Implementación en MySQL utilizando la libreria pymysql para python.

## Dependencias

Primero instalamos python y pip.

Dependiendo el sistema operativo en el que nos encontremos podemos seguir éste [tutorial](https://tecnonucleous.com/2018/01/28/como-instalar-pip-para-python-en-windows-mac-y-linux/).

Una vez instaldo python junto a pip, instalamos las dependencias del proyecto:

```pip install -r requirements.txt```

## Credenciales

Cambiamos el nombre del archivo .env_example por .env y modificamos los valores correspondientes.

## Ejecutable

Podemos generar un ejecutable tanto del programa principal,

```pyinstaller src/main.py --onefile```

cómo de la automatización de mensajes.

```pyinstaller src/run_thread.py --onefile```