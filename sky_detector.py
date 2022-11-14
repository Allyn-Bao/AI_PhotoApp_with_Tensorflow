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

    def __init__(self, model_path):
        super().__init__(model_path=model_path)


if __name__ == "__main__":
    # plt test
    black_img = np.asarray([[[0 for _ in range(100)] for _ in range(100)] for _ in range(3)])
    plt.imshow(tf.transpose(black_img.astype("uint8")))
    plt.show()
    print(tf.transpose(black_img.astype("uint8")))
