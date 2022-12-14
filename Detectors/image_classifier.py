import tensorflow as tf
import os

# detector classes
from Detectors.detector import Detector
from Detectors.object_detector import Object_Detector
from Detectors.sky_detector import Sky_Detector
from Detectors.mountain_detector import Mountain_Detector
from Detectors.forest_detector import Forest_Detector
from Detectors.building_detector import Building_Detector
from Detectors.night_detector import Night_Detector


class Image_classifier(Detector):

    # for object detection
    COCO_LABEL_PATH = os.path.join('..', 'Detectors', 'COCO_datasets', 'coco_categories.json')
    COCO_SUPER_LABEL_PATH = os.path.join('..', 'Detectors', 'COCO_datasets', 'coco_super_categories.json')
    OD_MODEL_URL = 'http://download.tensorflow.org/models/object_detection/tf2/20200711/mask_rcnn_inception_resnet_v2_1024x1024_coco17_gpu-8.tar.gz'

    # minimum confidence threshold on a prediction
    THRESHOLD = 0.7

    # albums
    ALBUMS = ["portraits", "pets", "cars", "interior",
              "food", "nature", "urban", "sunset", "night"]

    def __init__(self):
        super().__init__()
        # initialize detectors
        self.ob_detector = Object_Detector(labels_path=self.COCO_LABEL_PATH,
                                           super_label_path=self.COCO_SUPER_LABEL_PATH,
                                           model_url=self.OD_MODEL_URL)
        self.detectors = [
            Sky_Detector(),
            Mountain_Detector(),
            Forest_Detector(),
            Building_Detector(),
            Night_Detector()
        ]
        # COCO dataset
        self.coco_super_class_dict = Image_classifier.get_labels_from_json(self.COCO_SUPER_LABEL_PATH)
        self.coco_class_list = list(dict(Image_classifier.get_labels_from_json(self.COCO_LABEL_PATH)).keys())
        self.coco_super_class_list = list(dict(self.coco_super_class_dict).keys())

    def classify_image(self, image):
        """
        input: image np-array
        output: (labels, objects): <list>, <list>
                where labels contain string of all class names from self.detectors,
                and objects contain the result of object_detector detection, in the format of:
                    [ { str_coco_class_name: [float_confidence, float_occupied_area_percentage] } ]
        """
        labels = []
        objects = []
        # labels - class by environment
        for detector in self.detectors:
            prediction = detector.predict_image(image)
            if prediction != "unsure":
                labels += self.extract_label(prediction)
        # object detected
        objects.append(self.ob_detector.detect_image(image))
        return labels, objects

    def extract_label(self, predictions):
        """
        detector predict_image() -> [ class_names ]
        """
        list_labels = []
        for key, value in predictions.items():
            if value[0] >= self.THRESHOLD:
                list_labels.append(key)
        return list_labels

    def label_image(self, image):
        labels, objects = self.classify_image(image)
        # labels
        # filter out negating class names: eg. not ...
        labels = Image_classifier.filter_label_negation(labels)
        # toggle labels: labels assume until proven otherwise
        is_nature = "building" not in labels
        is_urban = not is_nature
        is_interior = False
        # album class
        album = set()
        for key, value in objects[0].items():
            super_class = self.get_coco_super_class(key)
            # portrait: includes "person" and occupied area larger than 0.2
            if key == "person" and value[1] > 0.25:
                album.add("portraits")
            # pets
            elif key == "dog" or key == "cat" and value[1] > 0.25:
                album.add("pets")
            # cars
            if key == "car" and value[1] > 0.3:
                album.add("cars")
            # interior
            if super_class == "furniture" or super_class == "appliance":
                is_interior = True
            # food
            if super_class == "food" or super_class == "kitchen":
                album.add("food")
        # nature
        if is_nature and ("forest" in labels or "mountain" in labels):
            album.add("nature")
        # urban
        if is_urban:
            album.add("urban")
        elif is_interior:
            album.add("interior")
        # sunset
        if "sunset" in labels:
            album.add("sunset")
        # night
        elif "night" in labels:
            album.add("night")
        # objects
        objects_list = list(objects[0].keys()) + labels
        return list(album), objects_list

    def label_images_by_paths(self, images_paths):
        detector_dict = {}
        for image_path in images_paths:
            image = Image_classifier.import_image_from_path(image_path)

            albums, objects = self.label_image(image)
            detector_dict[image_path] = [albums, objects]

            # log image
            self.show_img(image, "labels:" + ", ".join(albums) + "\nobjects" + ", ".join(objects))

        return detector_dict

    @staticmethod
    def filter_label_negation(labels):
        """
        remove str "not *" from list
        """
        return list(filter(lambda name: "not" not in name, labels))

    def get_coco_super_class(self, class_name):
        """
        str of COCO class_name -> str of COCO super class
        """
        return self.coco_super_class_dict[class_name]


if __name__ == "__main__":
    image_classifier = Image_classifier()
    sample_dir_path = os.path.join("sample_images", "classifier testing")
    list_images_path = Image_classifier.get_image_list(sample_dir_path)
    dict_result = image_classifier.label_images_by_paths(list_images_path)
    print("RESULT:", dict_result)
