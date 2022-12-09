from flask import Flask, request, jsonify, Blueprint, current_app
from .extensions import db
from .model import Model
import json


main = Blueprint('main', __name__)


@main.route('/')
def root():
    return jsonify({"images": current_app.image_filter.image_path_to_labels_dict})


@main.route('/add_images', methods=['POST'])
def add_images():
    data = request.get_json()
    # add image to image filter object
    for image_url in data["images"]:
        current_app.image_filter.add_image(image_url)
    print(current_app.image_filter.image_path_to_labels_dict)
    # save
    # ...
    # return updated image list according to the filters
    album = data["album"]
    keywords = data["keywords"]
    list_of_images = current_app.image_filter.get_images_filtered(album, keywords)
    return jsonify({"condition": "image(s) added", "updated_images": list_of_images}), 201


@main.route('/delete_images', methods=['POST'])
def delete_images():
    data = request.get_json()
    # delete images
    for image_url in data["images"]:
        current_app.image_filter.remove_image(image_url)
    print(current_app.image_filter.image_path_to_labels_dict)
    # save
    # ....
    # return updated image list according to the filters
    album = data["album"]
    keywords = data["keywords"]
    list_of_images = current_app.image_filter.get_images_filtered(album, keywords)
    return jsonify({"condition": "image(s) deleted", "updated_images": list_of_images}), 201


@main.route('/images', methods=['POST'])
def get_images():
    data = request.get_json()
    album = data["album"]
    keywords = data["keywords"]
    list_of_images = current_app.image_filter.get_images_filtered(album, keywords)
    return jsonify({"condition": "image filtered", "updated_images": list_of_images}), 201


def save_to_database(images_to_labels, albums_to_images, keywords_to_images):
    column_names = ['images_to_labels', 'albums_to_images', 'keywords_to_images']
    column_dicts = [images_to_labels, albums_to_images, keywords_to_images]
    # clear old data
    db.session.query(Model).delete()
    db.session.commit()
    # add new data
    for i in range(len(column_names)):
        dictionary = Model(name=column_names[i], dict=column_dicts[i])
        db.session.add(dictionary)
    db.session.commit()


def get_dicts_from_database():
    pass


