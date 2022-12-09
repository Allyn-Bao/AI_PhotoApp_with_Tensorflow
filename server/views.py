from flask import Flask, request, jsonify, Blueprint


main = Blueprint('main', __name__)


@main.route('/add_image', methods=['POST'])
def add_image():
    data = request.get_json()

    return 'Image Added', 201


@main.route('/delete_image', methods=['POST'])
def delete_image():
    data = request.get_json()

    return 'Image Deleted', 201


@main.route('/images')
def get_images():
    return jsonify([])
