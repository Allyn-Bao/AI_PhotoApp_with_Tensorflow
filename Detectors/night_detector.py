import os
from Detectors.detector import Detector


class Night_Detector(Detector):
    IMAGE_SIZE = 244
    MODEL_PATH = os.path.join('..', 'Detectors', 'models', 'night_recognition_basic_v1.h5')
    CLASS_NAME = ['day', 'night']

    def __init__(self):
        super().__init__(model_path=self.MODEL_PATH,
                         class_names=self.CLASS_NAME,
                         image_size=self.IMAGE_SIZE)


if __name__ == "__main__":
    sample_images_path = os.path.join("sample_images", "night testing")
    night_detector = Night_Detector()
    print(night_detector.predict_images_by_dir_path(sample_images_path))
