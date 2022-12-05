"""
superclass of all detectors
"""
import tensorflow as tf
from tensorflow.python.keras.utils.data_utils import get_file
import json
import os
import numpy as np
import matplotlib.pyplot as plt


class Detector:

    model_name = None
    model = None
    IMAGE_SIZE = None

    def __init__(self, class_names=None, model_url=None, model_path=None, image_size=244):
        self.IMAGE_SIZE = image_size
        self.CLASS_NAMES = class_names
        # downloaded models from model zoo
        if model_url is not None and model_path is None:
            self.download_model(model_url)
            model_path = os.path.join('..', 'Detectors', 'models', 'checkpoints', self.model_name, 'saved_model')
            self.load_downloaded_model(model_path)
        # saved keras models
        elif model_url is None and model_path is not None and os.path.splitext(model_path)[1] == ".h5":
            self.model_name = os.path.basename(model_path)
            self.load_saved_model(model_path)

    @staticmethod
    def get_labels_from_json(json_file_path):
        """
        import json file as dictionary
        input: str, jason file path
        output: dictionary
        """
        with open(json_file_path, 'r') as json_file:
            labels = json.load(json_file)
            return labels

    def download_model(self, model_url):
        """
        download a pre-trained model from url, if it does not exit in the models folder
        """
        file_name = os.path.basename(model_url)
        self.model_name = file_name[:file_name.index(".")]
        download_dir = os.path.join('..', 'Detectors', 'models')
        get_file(fname=file_name,
                 origin=model_url,
                 cache_dir=download_dir,
                 cache_subdir="checkpoints",
                 extract=True)

    def load_downloaded_model(self, model_path):
        """
        load the local pretrained model downloaded from model zoo in the models folder
        """
        print("Model Loading:", self.model_name)
        tf.keras.backend.clear_session()
        self.model = tf.saved_model.load(model_path)
        print("model load successfully")

    def load_saved_model(self, model_path):
        """
        load saved keras model created locally in .h5 format
        """
        print("Model Loading", self.model_name)
        tf.keras.backend.clear_session()
        self.model = tf.keras.models.load_model(model_path)
        print("model load successfully")

    def predict_image(self, image):
        """
        Predict image
         - resize / rescale
         - prediction with model

        """
        # resizing
        resized_image = tf.image.resize(
            images=image,
            size=[self.IMAGE_SIZE, self.IMAGE_SIZE],
            method=tf.image.ResizeMethod.BILINEAR,
            preserve_aspect_ratio=False,
        )
        # prediction
        image_tensor = tf.convert_to_tensor(np.expand_dims(resized_image, axis=0))
        predictions = self.model.predict(image_tensor)
        prediction = self.get_prediction(predictions)
        return prediction

    def predict_images(self, images):
        """
                input: list of image-np-arrays
                output: list of predictions
                """
        list_predictions = []
        for image in images:
            list_predictions.append(self.predict_image(image))
        return list_predictions

    def predict_images_by_path(self, image_paths):
        predictions = {}
        for image_path in image_paths:
            prediction = self.predict_image(Detector.import_image_from_path(image_path))
            predictions[image_path] = prediction
        return predictions

    def predict_images_by_dir_path(self, dir_path):
        return self.predict_images_by_path(Detector.get_image_list(dir_path))

    def get_prediction(self, prediction):
        one_hot_array = prediction[0]
        max_confidence = max(one_hot_array)
        if max_confidence < 0.5:
            return 'unsure'
        else:
            return {self.CLASS_NAMES[one_hot_array.argmax()]: [max_confidence]}

    @staticmethod
    def show_img_with_path(image_path):
        """
        show numpy array as image with pyplot
        """
        image = plt.imread(image_path)
        Detector.show_img(image)

    @staticmethod
    def show_img(image, label=None):
        plt.imshow(np.array(image, dtype=int))
        plt.title(label)
        plt.show()
        plt.close()

    @staticmethod
    def get_image_list(dir_path):
        """
        directory path => list of image paths
        """
        format_list = [".jpg", ".jpeg", ".JPG"]
        img_list = list(map(lambda name: os.path.join(dir_path, name), os.listdir(dir_path)))
        img_list = list(filter(lambda path: os.path.splitext(os.path.basename(path))[1] in format_list, img_list))
        return img_list

    @staticmethod
    def import_image_from_path(image_path):
        """
        image path -> image np array
        """
        return plt.imread(image_path)

    @ staticmethod
    def import_images_from_dir(dir_path):
        """
        directory path -> list of image np arrays
        """
        images_path = Detector.get_image_list(dir_path)
        image_list = []
        for image_path in images_path:
            image_list.append(Detector.import_image_from_path(image_path))
        return image_list


if __name__ == "__main__":
    detector = Detector()
    sample_dir_path = os.path.join("sample_images", "classifier testing")
    print(detector.get_image_list(sample_dir_path))



