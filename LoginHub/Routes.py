import redis
from flask import redirect, request, session, make_response, render_template
from flask_session import Session

from LoginHub.App import AppConfig, Flask
from LoginHub.Joomla import Joomla

_redis_pass = AppConfig.get('REDIS_PASSWORD', None)
if _redis_pass == '':
    _redis_pass = None
flask_redis = redis.Redis(
    host=AppConfig.get('REDIS_HOST', '127.0.0.1'),
    port=AppConfig.getint('REDIS_PORT', 6379),
    db=AppConfig.getint('REDIS_DB', 0),
    password=_redis_pass
)

Flask.config['SECRET_KEY'] = AppConfig.get('APP_SECRET', 'abcd12345')
Flask.config['SESSION_TYPE'] = 'redis'
Flask.config['session_cookie_name'] = 'loginhub'
Flask.config['SESSION_REDIS'] = flask_redis

Session(Flask)


@Flask.route('/')
def index():
    cookies = request.cookies
    sessions = []
    if 'joomla_user_state' in cookies:
        if cookies['joomla_user_state'] == 'logged_in':
            for key, value in cookies.items():
                if key == 'joomla_user_state':
                    pass
                else:
                    sessions.append(Joomla.get_session(value))
            sessions = list(filter(None, sessions))
            sessions = sessions[0]
            session['jsession'] = sessions.data
            return redirect('/validate')
    else:
        return redirect(AppConfig.get('APP_HOMEPAGE', '/404'))


@Flask.route("/validate")
def validate():
    jsession = session.get('jsession')
    if 'X-Forwarded-For' in request.headers:
        client_ip = request.headers['X-Forwarded-For']
    else:
        client_ip = request.remote_addr
    js_ip = jsession['Joomla/Registry/Registry']['*data']['__default']['session']['client']['forwarded']
    if js_ip != client_ip:
        response = make_response(redirect(AppConfig.get('APP_LOGOUT', '/log-out')))
        for k, v in request.cookies.items():
            response.set_cookie(k, '', expires=0)
        session.clear()
        return response
    else:
        return redirect('/main')


@Flask.route("/main")
def main():
    if 'jsession' not in session.keys():
        return redirect(AppConfig.get('APP_LOGOUT', '/log-out'))
    jsession = session.get('jsession')
    client_id = jsession['Joomla/Registry/Registry']['*data']['__default']['user']['id']
    discord_url = AppConfig.get('URL_DISCORD', '/')

    return render_template('main.html', client_id=client_id, discord_url=discord_url)


@Flask.route('/discord/token')
def discord_token():
    print(request.args)
    pass
