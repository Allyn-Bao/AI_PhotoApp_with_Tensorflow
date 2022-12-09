from flask import Flask
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_marshmallow import Marshmallow
from image_filter import Image_Filter
import os
from .extensions import db


def create_app():
    app = Flask(__name__)

    # database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # init db
    db.init_app(app)

    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)

    app.image_filter = Image_Filter()

    from server.views import main
    app.register_blueprint(main)

    return app


if __name__ == "__main__":
    # run server
    app = create_app()
    app.run(debug=True, use_reloader=False)
