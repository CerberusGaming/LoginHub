import pprint
import re
import phpserialize
from LoginHub.Joomla.Session import JoomlaSession


def print(*args, **kwargs):
    pprint.pprint(*args, **kwargs)


test_session = ''
kek = JoomlaSession(test_session)
