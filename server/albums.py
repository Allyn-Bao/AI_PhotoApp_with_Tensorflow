class Albums:

    def __init__(self, album_label_to_images_dict):
        self.album_label_to_cover_dict = {}
        self.update_album_covers(album_label_to_images_dict)

    def update_album_covers(self, album_label_to_images_dict: dict):
        if album_label_to_images_dict == {}:
            return
        for label, images in album_label_to_images_dict.items():
            # skip "all" album
            if label == "all":
                continue
            # if label already exist in album covers dict
            if label in self.album_label_to_cover_dict.keys():
                # check if cover image is not deleted
                cover_image = self.album_label_to_cover_dict[label]
                if cover_image not in images:
                    # update cover image
                    self.album_label_to_cover_dict[label] = images[0]
            else:
                # add new album and cover
                if images: # check if non-empty
                    self.album_label_to_cover_dict[label] = images[0]
        # check for deleted albums
        for album in self.album_label_to_cover_dict.keys():
            if album not in album_label_to_images_dict.keys():
                del self.album_label_to_cover_dict[album]


    def get_album_labels(self):
        return list(self.album_label_to_cover_dict.keys())

    def get_album_covers(self):
        return list(self.album_label_to_cover_dict.values())

