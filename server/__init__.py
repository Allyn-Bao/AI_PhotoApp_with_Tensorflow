from flask import Flask
from flask import jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_marshmallow import Marshmallow
from image_filter import Image_Filter
import os
# from server.extensions import db
from server.views import *


def create_app():
    app = Flask(__name__)

    # database
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
    # init db
    db.init_app(app)

    # image filter
    app.image_filter = Image_Filter()
    # load saved content
    saved_content = unpack_json_dicts(get_from_file(save_path))
    if saved_content is not None:
        app.image_filter.image_path_to_labels_dict, \
        app.image_filter.album_to_image_paths_dict, \
        app.image_filter.keyword_to_image_paths_dict = unpack_json_dicts(get_from_file(save_path))

    # blueprint
    from server.views import main
    app.register_blueprint(main)

    return app


if __name__ == "__main__":
    # run server
    app = create_app()
    app.run(debug=True, use_reloader=False)
