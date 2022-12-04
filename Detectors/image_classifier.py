import tensorflow as tf
import os

# detector classes
from detector import Detector
from Object_detector import Object_Detector
from sky_detector import Sky_Detector
from mountain_detector import Mountain_Detector


class Image_classifier(Detector):

    COCO_LABEL_PATH = os.path.join('Detectors', 'COCO_datasets', 'coco_categories.json')
    COCO_SUPER_LABEL_PATH = os.path.join('Detectors', 'COCO_datasets', 'coco_super_categories.json')
    OD_MODEL_URL = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/mask_rcnn_inception_resnet_v2_1024x1024_coco17_gpu-8.tar.gz'

    ALBUM_TAGS = ['Portrait', 'Pet', 'Sunset', 'Nature', 'Urban', 'Night']

    def __init__(self):
        super().__init__()
        # initialize detectors
        self.ob_detector = Object_Detector(labels_path=self.COCO_LABEL_PATH,
                                           super_label_path=self.COCO_SUPER_LABEL_PATH,
                                           model_url=self.OD_MODEL_URL)
        self.sky_detector = Sky_Detector()
        self.mountain_detector = Mountain_Detector()

    def tag_image(self, image):
        pass



