from flask import Flask, jsonify, request
from flask_cors import CORS
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
cors = CORS(app, resources={r"/api/v1/*": {"origins": "127.0.0.1"}})


@app.errorhandler(404)
def not_found(error):
    """ Handles 404 error"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5050
    app.run(host=host, port=port, debug=True, threaded=True)
