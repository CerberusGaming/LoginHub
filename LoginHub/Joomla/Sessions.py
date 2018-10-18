import redis
from LoginHub.Joomla.Session import JoomlaSession


class JoomlaSessions:
    def __init__(self, host: str = None, port: int = 6379, db: int = 0, password: str = None):
        self.__redis__ = redis.StrictRedis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=True,
            retry_on_timeout=True
        )
        self.__session_header__ = 'PHPREDIS_SESSION'

    def _get_session_key(self, session_id: str = None):
        return self.__session_header__ + ":" + session_id

    def get_session(self, session_id):
        sessions = self.__redis__.get(self._get_session_key(session_id))
        return JoomlaSession(sessions, session_id)
