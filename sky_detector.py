import tensorflow as tf
from tensorflow.python.keras.utils.data_utils import get_file
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

import detector


class Sky_Detector(detector.Detector):
    IMAGE_SIZE = 244
    LABELS = ['sunset', 'sky', 'no_sky']
    MODEL_PATH = os.path.join('models', 'sky_recognition_basic_v2.h5')
    CLASS_NAME = ['no_sky', 'sky', 'sunset']

    def __init__(self):
        super().__init__(model_path=self.MODEL_PATH)

    def predict_image(self, image_path):
        # import image
        self.show_img_with_path(image_path)
        image = plt.imread(image_path)
        # resizing
        resized_image = tf.image.resize(
            images=image,
            size=[self.IMAGE_SIZE, self.IMAGE_SIZE],
            method=tf.image.ResizeMethod.BILINEAR,
            preserve_aspect_ratio=False,
        )
        self.show_img(np.asarray(resized_image))

        # rescaling and normalizing image
        image_array = np.asarray(resized_image) / 255

        # prediction
        image_tensor = tf.convert_to_tensor(np.expand_dims(image_array, axis=0))
        print(np.shape(image_tensor))
        predictions = self.model.predict(image_tensor)
        prediction = Sky_Detector.get_prediction(predictions, self.CLASS_NAME)
        print(prediction)
        return prediction

    def predict_images(self, image_paths):
        predictions = {}
        for image_path in image_paths:
            predition = self.predict_image(image_path)
            predictions[image_path] = predition
        return predictions

    @staticmethod
    def get_prediction(prediction, class_names):
        one_hot_array = prediction[0]
        max_confidence = max(one_hot_array)
        if max_confidence < 0.5:
            return 'unsure'
        else:
            return {class_names[one_hot_array.argmax()]: [max_confidence]}


if __name__ == "__main__":
    sky_detector = Sky_Detector()
    sky_detector.predict_image(os.path.join('sample_images', 'sky_testing', 'images', 'ottawa_sunset_1.jpg'))
