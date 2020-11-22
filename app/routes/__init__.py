from flask import Blueprint

bp = Blueprint('main', __name__)
admin_bp = Blueprint('admin', __name__)

from app.routes import administartion
from app.routes import api
from app.routes import index
from app.routes import selector
from app.routes import qr
