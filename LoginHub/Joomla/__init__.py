from LoginHub.App import AppConfig
from LoginHub.Joomla.Sessions import JoomlaSessions

Joomla = JoomlaSessions(
    host=AppConfig.get('REDIS_HOST', '127.0.0.1'),
    port=AppConfig.getint('REDIS_PORT', 6379),
    db=AppConfig.getint('REDIS_DB', 0),
    password=AppConfig.get('REDIS_PASSWORD', None)
)
