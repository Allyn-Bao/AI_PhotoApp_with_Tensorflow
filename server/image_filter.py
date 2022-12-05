from Detectors.image_classifier import Image_classifier
import os


class Image_Filter:
    IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".JPG"]

    def __init__(self, image_path_list: list):
        self.image_classifier = Image_classifier()
        # image paths -> [ list of albums, list of keywords ]
        self.image_path_to_labels_dict = dict()
        # Albums -> list of images
        self.album_to_image_paths_dict = dict(zip(
            self.image_classifier.ALBUMS + ["all"],
            [[] for _ in range(len(self.image_classifier.ALBUMS) + 1)]
        ))
        # Keywords -> list of images
        self.keyword_to_image_paths_dict = dict()

    def add_image_path(self, image_path):
        """
        add image path to system
        """
        if self.is_image(image_path):
            # get labels
            albums, keywords = self.get_label_for_image(image_path)
            # image - labels:
            self.image_path_to_labels_dict[image_path] = [albums + ["all"], keywords]
            # albums:
            for album in albums:
                self.add_image_path_to_list_of_values_in_dict("all", image_path, self.album_to_image_paths_dict)
                self.add_image_path_to_list_of_values_in_dict(album, image_path, self.album_to_image_paths_dict)
            # keywords:
            for keyword in keywords:
                self.add_image_path_to_list_of_values_in_dict(keyword, image_path, self.keyword_to_image_paths_dict)
            return 0
        else:
            print("Error: not image: ", image_path)
            return 1

    def add_images_paths(self, images_paths: list):
        """
        add list of image path to system
        """
        for image_path in images_paths:
            self.add_image_path(image_path)

    def remove_image_path(self, image_path):
        """
        remove image path from system
        """
        try:
            # image - labels
            labels = self.image_path_to_labels_dict[image_path]
            albums = labels[0]
            keywords = labels[1]
            # remove from albums dict
            for album in albums:
                self.remove_image_path_to_list_of_values_in_dict(album, image_path, self.album_to_image_paths_dict)
            # remove from keyword dict
            for keyword in keywords:
                self.remove_image_path_to_list_of_values_in_dict(keyword, image_path, self.keyword_to_image_paths_dict)
            return 0
        except Exception as e:
            print(e)
            return 1

    def get_images_paths_from_album(self, album):
        """
        album -> list of image path
        """
        if album in self.album_to_image_paths_dict.keys():
            return self.album_to_image_paths_dict[album]
        else:
            print(f"Album {album} does not exist")
            return 1

    def get_images_paths_from_keyword(self, keyword):
        """
        keyword -> list of image paths
        """
        if keyword in self.keyword_to_image_paths_dict.keys():
            return self.keyword_to_image_paths_dict[keyword]
        else:
            print(f"Keyword {keyword} does not exist")
            return 1

    def get_images_paths_from_keywords(self, keywords: list):
        """
        list of keywords -> list of image paths
        """
        image_list = set()
        for keyword in keywords:
            image_list.add(self.get_images_paths_from_keyword(keyword))
        return list(image_list)

    def get_label_for_image(self, image_path):
        """
        get labels with Image Classifier
        """
        return self.image_classifier.label_image(self.image_classifier.import_image_from_path(image_path))


    @staticmethod
    def add_image_path_to_list_of_values_in_dict(key, image_path, dictionary: dict):
        """
        dictionary: { key: [images] }
        add image path to [images] under dictionary[key]
        """
        if key in dictionary.keys():
            dictionary[key].append(image_path)
        else:
            dictionary[key] = [image_path]
        return dictionary

    @staticmethod
    def remove_image_path_to_list_of_values_in_dict(key, image_path, dictionary: dict):
        """
        dictionary: { key: [images] }
        add image path to [images] under dictionary[key]
        """
        if key in dictionary.keys():
            if image_path in dictionary[key]:
                dictionary[key].remove(image_path)
            else:
                print(f"image not found in {key}: {image_path}")
        else:
            print(f"key: {key} doesn't exist in dictionary: {dictionary}")

    def is_image(self, image_path):
        """
        return True if file is image (file extension in IMAGE_EXTENSIONS)
        """
        return os.path.splitext(os.path.basename(image_path))[1] in self.IMAGE_EXTENSIONS

    def get_all_image_path_from_dir(self, dir_path):
        """
        dir path -> all images paths under dir
        """
        images_paths = list(map(lambda image_name: os.path.join(dir_path, image_name), list(os.listdir(dir_path))))
        return list(filter(lambda image_path: self.is_image(image_path), images_paths))


if __name__ == "__main__":
    # image_classifier = Image_classifier()
    image_filter = Image_Filter([])

    # local_image_path_list = image_classifier.

    dir_path = os.path.join("..", "images")
    images_list = image_filter.get_all_image_path_from_dir(dir_path)
    image_filter.add_images_paths(images_list)
    print(image_filter.get_images_paths_from_keywords(["building"]))


