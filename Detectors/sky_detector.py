import os
import detector


class Sky_Detector(detector.Detector):
    IMAGE_SIZE = 244
    MODEL_PATH = os.path.join('models', 'sky_recognition_basic_v2.h5')
    CLASS_NAMES = ['not sky', 'sky', 'sunset']

    def __init__(self):
        super().__init__(model_path=self.MODEL_PATH,
                         image_size=self.IMAGE_SIZE,
                         class_names=self.CLASS_NAMES)


if __name__ == "__main__":
    sample_dir_path = os.path.join("sample_images", "sky_testing")
    sky_detector = Sky_Detector()
    print(sky_detector.predict_images_by_dir_path(sample_dir_path))
