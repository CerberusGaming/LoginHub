import base64
import re
import phpserialize


class JoomlaSession:
    def __init__(self, session: str = None, session_id: str = None):
        # Parse the session data
        sess_name, sess_type, sess_len, session = re.search(r'^(.*)\|(.):([0-9]*):"(.*)";$', session).groups()
        session = str(base64.b64decode(session).decode('utf-8'))
        session = session.replace('"', "'")
        session = '"' + session + '"'
        session = "{" + session.replace('{', '":{"').replace('}', '"},"').replace(',""', '').replace('\x00', '') + "}"
        session = session.replace('"}', '":""}').replace('\\', '/')
        session = dict(eval(session))
        print(session)
        print(self._parse_dict(session))

    def _parse_dict(self, data: dict = None):
        for k, v in data.items():
            k = self._parse_key(k)
            if k[1] != 'dict':
                for sk, sv in v.items():
                    if len(sv) == 0:
                        v = sk
                v = list(filter(None, v.split(';')))
                v_pass = 0
                v_len = len(v)
                v_dict = {}
                while v_pass != v_len:
                    v_dict[v[v_pass]] = v[v_pass + 1]
                    v_pass += 2
                v = v_dict
                v_dict = {}
                for vk, vv in v.items():
                    vk = vk.split(':')[-1].replace("'", '')
                    vv = vv.split(':')[-1].replace("'", '')
                    v_dict[vk] = vv
                v = v_dict
                return {k[0]: v}
            else:
                print('dicks')
                multi_v = {}
                for vk, vv in v.items():
                    vk = vk.replace("'", '').replace(";", ':').split(':')[2]
                    print(vk)
                    if isinstance(vk, dict):
                        multi_v[vk] = self._parse_dict(vv)
                    else:
                        multi_v[vk] = vv
                return {k[0]: multi_v}

    @staticmethod
    def _parse_pair(pair):
        pass

    @staticmethod
    def _parse_key(key):
        key = key.replace("'", '').replace(';', ':').split(':')
        if key[0] == 'O':
            return key[2], 'dict'
        elif key[0] == 's':
            if len(key) >= 4:
                if key[3] == 'O':
                    return key[2], 'dict'
                else:
                    return key[2], 'string'
        else:
            pass
