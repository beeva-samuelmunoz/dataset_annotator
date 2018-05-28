"""
"""

import argparse

from flask import Flask

from DS_annotator.annotations import Annotations
from DS_annotator.server.flask import init_flask
from DS_annotator.server.jsonrpc import init_jsonrpc


if __name__ == '__main__':
    #TODO import argparse
    # User input
    # path_dir_imgs = sys.argv[1]
    # path_file_out = sys.argv[2]
    path_dir_imgs = "/home/samuelmunoz/beeva/dataset_annotator/data"
    path_file_out = "/home/samuelmunoz/beeva/dataset_annotator/data/test1.csv"

    annotations = Annotations(path_dir_imgs, path_file_out)

    # set the project root directory as the static folder, you can set others.
    app = Flask(__name__, static_url_path='')
    init_flask(app, path_dir_imgs, path_file_out)
    init_jsonrpc(app, annotations)


    app.run(host='0.0.0.0', debug=True)
