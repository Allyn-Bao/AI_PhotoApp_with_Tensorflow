import os
from Detectors.detector import Detector


class Mountain_Detector(Detector):
    IMAGE_SIZE = 244
    MODEL_PATH = os.path.join('..', 'Detectors', 'models', 'mountain_recognition_basic_v1.h5')
    CLASS_NAME = ['mountain', 'not mountain']

    def __init__(self):
        super().__init__(model_path=self.MODEL_PATH,
                         class_names=self.CLASS_NAME,
                         image_size=self.IMAGE_SIZE)


if __name__ == "__main__":
    sample_dir_path = os.path.join("sample_images", "mountain testing")
    mountain_detector = Mountain_Detector()
    print(mountain_detector.predict_images_by_dir_path(sample_dir_path))

