"""
This object detector uses a pre-trained tensorflow model (trained on COCO dataset) from model zoo

"""
import tensorflow as tf
from tensorflow.python.keras.utils.data_utils import get_file
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

import detector


COCO_LABEL_PATH = os.path.join('COCO_datasets', 'coco_categories.json')
COCO_SUPER_LABEL_PATH = os.path.join('COCO_datasets', 'coco_super_categories.json')
MODEL_URL = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/mask_rcnn_inception_resnet_v2_1024x1024_coco17_gpu-8.tar.gz'


class Object_Detector(detector.Detector):
    SCORE_THRESHOLD = 0.5
    IMAGE_AREA = 1024 * 1024

    def __init__(self, labels_path, super_label_path, model_url):
        # load model
        super().__init__(model_url=model_url)
        self.dict_labels = Object_Detector.get_labels_from_json(labels_path)
        # import COCO labels
        self.dict_label_name_by_index = dict((v, k) for k, v in self.dict_labels.items())
        self.dict_super_labels = Object_Detector.get_labels_from_json(super_label_path)

    # @staticmethod
    # def get_labels_from_json(json_file_path):
    #     """
    #     import json file as dictionary
    #     input: str, jason file path
    #     output: dictionary
    #     """
    #     with open(json_file_path, 'r') as json_file:
    #         labels = json.load(json_file)
    #         return labels

    # def download_model(self, model_url):
    #     """
    #     download a pre-trained model from url, if does not exit in the models folder
    #     """
    #     file_name = os.path.basename(model_url)
    #     self.model_name = file_name[:file_name.index(".")]
    #     download_dir = os.path.join('models')
    #     get_file(fname=file_name,
    #              origin=model_url,
    #              cache_dir=download_dir,
    #              cache_subdir="checkpoints",
    #              extract=True)

    # def load_model(self):
    #     """
    #     load the local pretrained model in the models folder
    #     """
    #     print("Model Loading:", self.model_name)
    #     tf.keras.backend.clear_session()
    #     self.model = tf.saved_model.load(os.path.join('models', 'checkpoints', self.model_name, 'saved_model'))
    #     print("model load successfully")

    def detect_image(self, image_path):
        """
        detect objects in an image given an image path,
        including confidence sore for each object and ratio of covered area that object's bounding box covers
        objects name come from the coco2017 dataset, which the model was trained on.
        input: str, image path
        output: dictionary, each key<str> is the object class name, value<list> contains [ confidence_score, area_ratio]
        """
        # import image
        self.show_img_with_path(image_path)
        image = plt.imread(image_path)
        # resizing
        resized_image = tf.image.resize(
            images=image,
            size=[1024, 1024],
            method=tf.image.ResizeMethod.BILINEAR,
            preserve_aspect_ratio=False,
            antialias=False
        )
        self.show_img(np.asarray(resized_image))

        # processing
        image_array = np.asarray(resized_image)
        int_array = image_array.astype(int) - 1

        # detection
        detections = self.model([tf.convert_to_tensor(np.array(int_array))])
        # all classes detection
        class_array = np.asarray(detections['detection_classes'][0]).astype(int)
        # class confidence score
        class_score = np.asarray(detections['detection_scores'][0])
        # bounding boxes
        class_bbox = np.asarray(detections['detection_boxes'][0])
        # list of all detected classes
        class_detected = {}
        print("Detection for image:", os.path.basename(image_path))
        for i in range(0, min(5, len(class_array))):
            if class_score[i] >= self.SCORE_THRESHOLD:
                # extract class name
                class_name = self.dict_label_name_by_index[class_array[i]]
                # objects of same class already found: save the max sore & area
                if class_name not in class_detected:
                    score = class_score[i]
                    area = Object_Detector.cal_bbox_area_ratio(class_bbox[i])

                else:
                    score = max(class_score[i], class_detected[class_name][0])
                    area = max(Object_Detector.cal_bbox_area_ratio(class_bbox[i]), class_detected[class_name][1])
                class_detected[class_name] = [score, area]
        print("object detected:", class_detected)
        return class_detected

    def detect_images(self, image_paths):
        """
        Detect objects in an array of images
        input: list<string>,  list of images paths
        output: list of dict, list of results for each image,
                                each dict elements in the list contains object info for one image
                format: example for a single image: [ {class_name: [score, area_ratio]}, ... ]
        """
        return list(map(self.detect_image, image_paths))

    # @staticmethod
    # def show_img(image_path):
    #     """
    #     show numpy array as image with pyplot
    #     """
    #     image = plt.imread(image_path)
    #     plt.imshow(np.array(image, dtype=int))
    #     plt.show()
    #     plt.close()

    @staticmethod
    def cal_bbox_area_ratio(bbox_array):
        """
        input: takes raw output of the model, bbox co-ordinates [x1, y1, x2, y2] between 0 and 1
        output the ratio of the boxed area over the total area
        """
        x1, y1, x2, y2 = bbox_array
        area = (x2 - x1) * (y2 - y1)
        return area


if __name__ == "__main__":
    sample_images_names = os.listdir(os.path.join('sample_images'))
    clean_sample_images_names = list(filter(lambda name: os.path.splitext(name)[1] == '.jpg', sample_images_names))
    sample_images_paths = list(map(lambda name: os.path.join('sample_images', name), clean_sample_images_names))
    print(sample_images_paths)
    od = Object_Detector(labels_path=COCO_LABEL_PATH, super_label_path=COCO_SUPER_LABEL_PATH, model_url=MODEL_URL)
    prediction = od.detect_images(sample_images_paths)
    print(prediction)
