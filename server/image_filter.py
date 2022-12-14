import base64
import io

from Detectors.image_classifier import Image_classifier
from vocab_dictionary import Vocab_Dictionary
import os
import requests
from PIL import Image
from io import BytesIO
import numpy as np


class Image_Filter:

    def __init__(self):
        self.image_classifier = Image_classifier()
        # image paths -> [ list of albums, list of keywords ]
        self.image_path_to_labels_dict = dict()
        # Albums -> list of images
        self.album_to_image_paths_dict = dict(zip(
            self.image_classifier.ALBUMS + ["all"],
            [[] for _ in range(len(self.image_classifier.ALBUMS) + 1)]
        ))
        # Keywords -> list of images
        self.keyword_to_image_paths_dict = dict()
        # vocab dictionary
        self.vd = Vocab_Dictionary()

    def add_image(self, image, is_path=False):
        """
        add image path to system
        """
        if image in self.image_path_to_labels_dict.keys():
            print(f"image: {image} already in dict")
            return 0
        # get labels
        albums, keywords = self.get_label_for_image(image, is_path=is_path)
        # image - labels:
        self.image_path_to_labels_dict[image] = [albums + ["all"], keywords]
        # albums:
        for album in albums:
            self.add_image_to_list_of_values_in_dict("all", image, self.album_to_image_paths_dict)
            self.add_image_to_list_of_values_in_dict(album, image, self.album_to_image_paths_dict)
        # keywords:
        for keyword in keywords:
            self.add_image_to_list_of_values_in_dict(keyword, image, self.keyword_to_image_paths_dict)
        return 0

    def add_images(self, images: list, is_path):
        """
        add list of image path to system
        """
        for image in images:
            self.add_image(image, is_path=is_path)

    def remove_image(self, image):
        """
        remove image path from system
        """
        print(f"log - delete image: total images before: {len(self.image_path_to_labels_dict)}")
        if image not in self.image_path_to_labels_dict.keys():
            print(f"remove failed: image not exist {image}")
            return 1
        # image - labels
        labels = self.image_path_to_labels_dict[image]
        albums = labels[0]
        keywords = labels[1]
        # remove from albums dict
        for album in albums:
            self.remove_image_to_list_of_values_in_dict(album, image, self.album_to_image_paths_dict)
        # remove from keyword dict
        for keyword in keywords:
            self.remove_image_to_list_of_values_in_dict(keyword, image, self.keyword_to_image_paths_dict)
        # remove from label list
        self.image_path_to_labels_dict.pop(image)
        print(f"log - image deleted: total images after {len(self.image_path_to_labels_dict)}")
        return 0

    def get_images_from_album(self, album):
        """
        album -> list of image path
        """
        if album in self.album_to_image_paths_dict.keys():
            return self.album_to_image_paths_dict[album]
        else:
            print(f"Album {album} does not exist")
            return []

    def get_images_from_keyword(self, keyword):
        """
        keyword -> list of image paths
        """
        image_list = set()
        # check keyword in the existing list of keywords
        for exist_keyword, images in list(self.keyword_to_image_paths_dict.items()):
            if self.vd.is_related(keyword, exist_keyword):
                image_list.update(set(images))
        # check if keyword is in preset keyword synonym list:
        similar_keyword = self.vd.word_in_keywords_related_words(keyword)
        if similar_keyword is not None and similar_keyword in list(self.keyword_to_image_paths_dict.keys()):
            image_list.update(set(self.keyword_to_image_paths_dict[similar_keyword]))
        # check if keyword is album name
        print(f"log - checking for keyword: {keyword}: list of albums: {self.album_to_image_paths_dict.keys()}")
        if keyword in self.album_to_image_paths_dict.keys():
            print(f"log - found album: {keyword} matches current keyword")
            image_list.update(set(self.album_to_image_paths_dict[keyword]))
        # check if keyword is synonym to album name:
        album_name_similar_to_keyword = self.vd.word_in_album_related_words(keyword)
        if (album_name_similar_to_keyword is not None
                and album_name_similar_to_keyword in self.album_to_image_paths_dict.keys()):
            image_list.update(set(self.album_to_image_paths_dict[album_name_similar_to_keyword]))
        return list(image_list)

    def get_images_from_keywords(self, keywords: list):
        """
        list of keywords -> list of image paths
        """
        image_list = set()
        for keyword in keywords:
            image_list.update(set(self.get_images_from_keyword(keyword)))
            # get album with keywords - when keyword input is also album
            if keyword in self.album_to_image_paths_dict.keys():
                image_list.update(set(self.get_images_from_album(keyword)))
        return list(image_list)

    def get_images_filtered(self, album=None, keywords=[]):
        """
        specified album + keywords -> list of qualified images
        """
        images_in_album = images_from_keywords = self.image_path_to_labels_dict.keys()
        # get image from album
        if album is not None:
            images_in_album = self.get_images_from_album(album)
        # get image with keywords
        if len(keywords) != 0:
            images_from_keywords = self.get_images_from_keywords(keywords)
        return list(set(images_in_album) & set(images_from_keywords))

    def get_label_for_image(self, image, is_path=False):
        """
        get labels with Image Classifier
        """
        if is_path:
            return self.image_classifier.label_image(self.image_classifier.import_image_from_path(image))
        else:
            # # is public web url
            # response = requests.get(image)
            # image_array = np.array(Image.open(BytesIO(response.content)))
            # is encoded url
            image_data = base64.b64decode(image.split(',')[1])
            image_data = Image.open(io.BytesIO(image_data))
            image_array = np.array(image_data)
            return self.image_classifier.label_image(image_array)

    @staticmethod
    def add_image_to_list_of_values_in_dict(key, image_path, dictionary: dict):
        """
        dictionary: { key: [images] }
        add image path to [images] under dictionary[key]
        """
        if key in dictionary.keys():
            dictionary[key].append(image_path)
        else:
            dictionary[key] = [image_path]
        return dictionary

    @staticmethod
    def remove_image_to_list_of_values_in_dict(key, image_path, dictionary: dict):
        """
        dictionary: { key: [images] }
        add image path to [images] under dictionary[key]
        """
        if key in dictionary.keys():
            if image_path in dictionary[key]:
                dictionary[key].remove(image_path)
            else:
                print(f"image not found in {key}: {image_path}")
        else:
            print(f"key: {key} doesn't exist in dictionary: {dictionary}")

    def is_image(self, image_path):
        """
        return True if file is image (file extension in IMAGE_EXTENSIONS)
        """
        return os.path.splitext(os.path.basename(image_path))[1] in [".jpg", ".JPG", ".JPEG", ".jpeg"]

    def get_all_image_path_from_dir(self, dir_path):
        """
        dir path -> all images paths under dir
        """
        images_paths = list(map(lambda image_name: os.path.join(dir_path, image_name), list(os.listdir(dir_path))))
        return list(filter(lambda image_path: self.is_image(image_path), images_paths))


if __name__ == "__main__":
    # image_classifier = Image_classifier()
    image_filter = Image_Filter()

    # local_image_path_list = image_classifier.

    dir_path = os.path.join("..", "images")
    images_list = image_filter.get_all_image_path_from_dir(dir_path)
    image_filter.add_images(images_list, is_path=True)
    print(len(image_filter.image_path_to_labels_dict))
    image_filter.remove_image(images_list[0])
    print(len(image_filter.image_path_to_labels_dict))


