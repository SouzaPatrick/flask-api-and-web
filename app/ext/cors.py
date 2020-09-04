from flask_cors import CORS

cors = CORS()

def init_app(app):
    cors.init_app(app, resources={r"/v1/*": {"origins": "*"}})