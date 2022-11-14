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

    def __init__(self, model_url=None, model_path=None):
        if model_url is not None and model_path is None:
            self.download_model(model_url)
            model_path = os.path.join('models', 'checkpoints', self.model_name, 'saved_model')
        self.load_model(model_path)

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
        download a pre-trained model from url, if does not exit in the models folder
        """
        file_name = os.path.basename(model_url)
        self.model_name = file_name[:file_name.index(".")]
        download_dir = os.path.join('models')
        get_file(fname=file_name,
                 origin=model_url,
                 cache_dir=download_dir,
                 cache_subdir="checkpoints",
                 extract=True)

    def load_model(self, model_path):
        """
        load the local pretrained model in the models folder
        """
        print("Model Loading:", self.model_name)
        tf.keras.backend.clear_session()
        self.model = tf.saved_model.load(model_path)
        print("model load successfully")

    @staticmethod
    def show_img_with_path(image_path):
        """
        show numpy array as image with pyplot
        """
        image = plt.imread(image_path)
        Detector.show_img(image)

    @staticmethod
    def show_img(image):
        plt.imshow(np.array(image, dtype=int))
        plt.show()
        plt.close()
