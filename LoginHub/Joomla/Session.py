import base64
import re


class JoomlaSession:
    def __init__(self, session: str = None, session_id: str = None, debug: bool = False):
        self._debug = debug
        self.session_id = session_id
        self.raw = self._parse_session(session)
        self.data = self._parse_dict(self.raw)

    def _parse_session(self, session: str = None):
        sess_name, sess_type, sess_len, session = re.search(r'^(.*)\|(.):([0-9]*):"(.*)";$', session).groups()
        session = str(base64.b64decode(session).decode('utf-8'))
        session = session.replace('"', "'")
        session = '"' + session + '"'
        session = "{" + session.replace('{', '":{"').replace('}', '"},"').replace(',""', '').replace('\x00', '') + "}"
        session = session.replace('"}', '":""}').replace('\\', '/')
        session = dict(eval(session))
        if self._debug:
            print(session)
        return session

    def _parse_dict(self, data: dict = None):
        output = {}
        _data = data
        data = {}
        for key in _data.keys():
            if len(key) != 0:
                data[key] = _data[key]
        for key in data.keys():
            key_type = self._get_object_type(key)
            if key_type == 'single':
                if isinstance(data[key], dict):
                    output[self._parse_key(key)] = self._parse_dict(data[key])
                else:
                    if self._debug:
                        print(data)
                    else:
                        raise AttributeError()
            elif key_type == 'multi':
                if isinstance(data[key], dict):
                    output[self._parse_key(key)] = self._parse_dict(data[key])
                else:
                    if self._debug:
                        print(data)
                    else:
                        raise AttributeError()
            elif key_type == 'pair':
                if isinstance(key, str):
                    for k, v in self._parse_pair(key).items():
                        output[k] = v
            else:
                if self._debug:
                    print(data)
                else:
                    raise AttributeError()
        return output

    def _parse_pair(self, pair: str = None):
        pair = list(filter(None, pair.split(';')))
        pair_len = len(pair)
        loop_count = 0
        output = {}
        while loop_count < pair_len:
            key = pair[loop_count].replace("'", '').split(':')[-1]
            value = pair[loop_count + 1].replace("'", '').split(':')
            if value[0].lower() == 'i':
                value = int(value[-1])
            elif value[0].lower() == 's':
                value = str(value[-1])
            elif value[0].lower() == 'b':
                value = int(value[-1])
                if value == 1:
                    value = True
                else:
                    value = False
            else:
                value = value[-1]
            loop_count += 2
            output[key] = value
        return output

    @staticmethod
    def _parse_key(key: str = None):
        key = key.replace("'", '').replace(';', ':').split(':')
        return key[2]

    @staticmethod
    def _get_object_type(obj: str = None):
        obj = list(filter(None, obj.split(';')))
        if len(obj) > 1:
            if str(obj[-1]).split(':')[0].lower() in ['o', 'a']:
                return 'multi'
            else:
                return 'pair'
        else:
            return 'single'

    def __getattr__(self, item):
        return self.data.get(item, None)

    def __str__(self):
        return "<Joomla Session ID: " + str(self.session_id) + ">"
