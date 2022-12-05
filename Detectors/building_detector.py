import os
import detector


class Building_Detector(detector.Detector):
    IMAGE_SIZE = 244
    MODEL_PATH = os.path.join('models', 'building_recognition_transf_v1.h5')
    CLASS_NAME = ['building', 'not building']

    def __init__(self):
        super().__init__(model_path=self.MODEL_PATH,
                         class_names=self.CLASS_NAME,
                         image_size=self.IMAGE_SIZE)


if __name__ == "__main__":
    sample_images_path = os.path.join("sample_images", "building testing")
    building_detector = Building_Detector()
    print(building_detector.predict_images_by_dir_path(sample_images_path))
