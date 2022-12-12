from flask import Flask, request, jsonify, Blueprint, current_app
from server.extensions import db
# from server.model import Images_Db
import json
import os

main = Blueprint('main', __name__)

save_path = os.path.join("./data.json")


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
    contents = jsonify_dicts(current_app.image_filter.image_path_to_labels_dict,
                             current_app.image_filter.album_to_image_paths_dict,
                             current_app.image_filter.keyword_to_image_paths_dict)
    save_to_file(contents, save_path)
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
    data = request.get_json()
    album = data["album"]
    keywords = data["keywords"]
    list_of_images = current_app.image_filter.get_images_filtered(album, keywords)
    return jsonify({"condition": "image filtered", "updated_images": list_of_images}), 201


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
