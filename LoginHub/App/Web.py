import os
from flask import Flask
from flask_bootstrap import Bootstrap

_templates = os.path.normpath(os.getcwd() + "/templates")
_static = os.path.normpath(os.getcwd() + "/static")

Flask = Flask(__name__, template_folder=_templates, static_folder=_static)
Bootstrap(Flask)
