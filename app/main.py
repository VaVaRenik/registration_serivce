from flask import Flask
from api.booking import booking_router
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(booking_router)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
