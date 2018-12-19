# Dataset Annotator

## Description
This tool allows to annotate images with bboxes from the web server in order to generate a dataset to train an object detection system.


## Features
* Web interface.
* Multiuser, enslave your coworkers in parallel!
* Resume work if server fails/closes.
* Draw several boxes in the same image.
* Delete images from dataset.
* Skip current image.
* Output file is in CSV format.


### TODO
*  Implement a visualization page to see annotations.
*  Implement something for classification.


## First steps

### Requirements

* make
* python3 (tested  with version 3.5)
* virtualenv

### Installation
```bash
git clone https://github.com/beeva-samuelmunoz/dataset_annotator
cd dataset_annotator
make install
```

*Note: if you want to use other python version rather than 3.5, type:*
```bash
make install PYTHON_VERSION=<version>
```

### First run
Once in the project folder `dataset_annotator`.
* To get some help type:
```bash
make
```
* Example, annotate images of *red cars* from the dataset created with the [image_downloader](https://github.com/beeva-samuelmunoz/image_downloader.git) and use the port 5000.
```bash
make make run-webserver path_imgs="/home/user/image_downloader/data/computer mouse-google" port=5000
```
  * *Note: you should use the path that fits your case, where the images are.*
  * Go to http://localhost:5000 and start tagging.
  * Once you are done, the resulting CSV file should be in `/home/user/image_downloader/data/computer mouse-google/annotations.csv`
