import base64
import imghdr
import io

from flask import Flask, request, jsonify, Blueprint, current_app
from server.extensions import db
# from server.model import Images_Db
import json
import os
from flask_cors import cross_origin

main = Blueprint('main', __name__)

save_path = os.path.join("./data.json")
images_dir_path = os.path.join(".", "images")


@main.route('/')
def root():
    return jsonify({"images": current_app.image_filter.image_path_to_labels_dict})


@main.route('/add_images', methods=['POST'])
def add_images():
    image_urls = request.json["imageURLs"]
    album = request.json["album"]
    keywords = request.json["keywords"]
    for i, url in enumerate(image_urls):
        if url.startswith('data:image/jpeg;'):
            current_app.image_filter.add_image(url)
    print(current_app.image_filter.image_path_to_labels_dict)
    # save
    contents = jsonify_dicts(current_app.image_filter.image_path_to_labels_dict,
                             current_app.image_filter.album_to_image_paths_dict,
                             current_app.image_filter.keyword_to_image_paths_dict)
    save_to_file(contents, save_path)
    # return updated image list according to the filters
    list_of_images = current_app.image_filter.get_images_filtered(album, keywords)
    return jsonify({"condition": "image(s) added", "updated_images": list_of_images}), 201


@main.route('/add_images_check', methods=['POST'])
@cross_origin()
def add_images_check():
    # get image urls:
    image_urls = request.json["imageURLs"]
    for i, url in enumerate(image_urls):
        if url.startswith('data:image/jpeg;'):
            with open(os.path.join(images_dir_path, f"image{i}.jpeg"), "wb") as f:
                f.write(base64.b64decode(url.split(',')[1]))
            current_app.image_filter.add_image(url)
    print(current_app.image_filter.image_path_to_labels_dict)
    return jsonify({"condition": "image received"})


@main.route('/delete_images', methods=['POST'])
def delete_images():
    data = request.get_json()
    # delete images
    for image_url in data["images"]:
        current_app.image_filter.remove_image(image_url)
    print(current_app.image_filter.image_path_to_labels_dict)
    # save
    contents = jsonify_dicts(current_app.image_filter.image_path_to_labels_dict,
                             current_app.image_filter.album_to_image_paths_dict,
                             current_app.image_filter.keyword_to_image_paths_dict)
    save_to_file(contents, save_path)
    # return updated image list according to the filters
    album = data["album"]
    keywords = data["keywords"]
    list_of_images = current_app.image_filter.get_images_filtered(album, keywords)
    return jsonify({"condition": "image(s) deleted", "updated_images": list_of_images}), 201


@main.route('/images', methods=['POST'])
def get_images():
    album = request.json["album"]
    keywords = request.json["keywords"]
    list_of_images = current_app.image_filter.get_images_filtered(album, keywords)
    return jsonify({"condition": "image filtered", "images": list_of_images}), 201


def save_to_database():
    pass


def get_dicts_from_database():
    pass


def save_to_file(content, file_path):
    """
    save json to file
    content: json
    file_path: string
    """
    if not os.path.exists(file_path):
        open(file_path, "a")
    with open(file_path, "w") as f:
        json.dump(content, f)
    return 0


def get_from_file(file_path):
    """
    get json from file
    file_path: string
    return: json, None if file doesn't exist
    """
    if not os.path.exists(file_path):
        print(f"file {file_path} doesn't exist")
        return None
    else:
        with open(file_path, "r") as f:
            return json.loads(f.read())


def jsonify_dicts(image_to_label, album_to_image, keyword_to_image):
    return {"image_to_label": image_to_label,
            "album_to_image": album_to_image,
            "keyword_to_image": keyword_to_image}


def unpack_json_dicts(json_content):
    if json_content is not None:
        return (json_content["image_to_label"],
                json_content["album_to_image"],
                json_content["keyword_to_image"])
    return None


def save_image_data_to_directory(image_data, image_name, dir_path):
    image_path = os.path.join(dir_path, image_name)
    with open(image_path, "wb") as f:
        f.write(image_data)

