from LoginHub.App.Config import Config
from LoginHub.Routes import Flask

AppConfig = Config()


def run():
    Flask.run(
        host=AppConfig.get('APP_HOST', '127.0.0.1'),
        port=AppConfig.getint('APP_PORT', 5000),
        debug=AppConfig.getbool('APP_DEBUG', False),
    )
