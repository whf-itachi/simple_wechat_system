from flask import Blueprint, request

index_blu = Blueprint('index', __name__, url_prefix='/')


@index_blu.before_request
def index_before_request():
    urla = request.url
    print(urla, ' is the url where now get!', end='/n')


from . import index
