import os
import detector


class Forest_Detector(detector.Detector):
    IMAGE_SIZE = 244
    MODEL_PATH = os.path.join('models', 'forest_recognition_basic_v1.h5')
    CLASS_NAME = ['forest', 'not forest']

    def __init__(self):
        super().__init__(model_path=self.MODEL_PATH,
                         class_names=self.CLASS_NAME,
                         image_size=self.IMAGE_SIZE)


if __name__ == "__main__":
    sample_images_path = os.path.join("sample_images", "forest testing")
    forest_detector = Forest_Detector()
    print(forest_detector.predict_images_by_dir_path(sample_images_path))
