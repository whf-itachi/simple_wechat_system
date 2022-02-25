from flask import Blueprint

dynamic_blu = Blueprint('dynamic', __name__, url_prefix='/dynamic/')


from . import views
