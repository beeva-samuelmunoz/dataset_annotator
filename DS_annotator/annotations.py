import csv
import os
import random


class Annotations:

    EXTENSIONS = ('.jpg', 'jpeg', '.png')

    def __init__(self, imgs_dir, csv_path):
        # Attributes
        self.imgs_dir = imgs_dir
        self.csv_path = csv_path  # Path to the csv file
        self.imgs_ids = set()  # Image paths under directory (relative)
        self.bboxes = []  # Annotations for the images. [ {path, x, y, width, height}, ... ]
        imgs_ids_candidate = set()  # Not annotated images (pending)

        # Get imgs under path
        for (path, subdirs, files) in os.walk(imgs_dir):
                if files:
                    for f in files:
                        if f.lower().endswith( self.EXTENSIONS ):
                            self.imgs_ids.add(
                                os.path.relpath(
                                    os.path.join(path,f),
                                    imgs_dir
                                )
                            )
        # Load CSV to resume tagging
        if os.path.isfile(csv_path):
            print("File {} seems to exist, resuming...".format(csv_path))
            with open(csv_path) as csvfile:
                self.bboxes = [row for row in csv.DictReader(csvfile)]
        self.imgs_ids_candidate = self.imgs_ids - set(x['path'] for x in self.bboxes) # Don't show already tagged imgs


    def save(self):
        """Save annotations into the csv_path file
        """
        if self.bboxes:
            with open(self.csv_path, "w+") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.bboxes[0].keys())
                writer.writeheader()
                for bbox in self.bboxes:
                    writer.writerow(bbox)


    def add_annotation(self, img_id, x, y, width, height):
        """Add an annotation
        """
        self.bboxes.append({
            'path': img_id,
            'x': x,
            'y': y,
            'width': width,
            'height': height,
        })


    def get_annotations(self, img_id):
        """Return ([annotations])
        """
        return [x for x in self.bboxes if x['path']==img_id]


    def get_not_annotated_image(self):
        """ Return the img_id of a non-annotated image
        """
        img_id = None
        if self.imgs_ids_candidate:
            img_id = random.sample(self.imgs_ids_candidate, 1).pop()
        return img_id


    def is_annotated(self, img_id):
        """Has an image already been anotated?
        """
        return img_id not in self.imgs_ids_candidate


    def set_annotated(self, img_id):
        """Do not annotate an image twice.
        """
        try:
            self.imgs_ids_candidate.remove(img_id)
        except:
            pass


    def remove_image(self, img_id):
        """Remove image from dataset & delete file.
        """
        try:
            os.remove(os.path.join(self.imgs_dir, img_id))
            self.set_annotated(img_id)
        except Exception as e:
            print(e)
            pass
