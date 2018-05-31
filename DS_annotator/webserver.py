"""Webserver
"""

import os
import sys
from threading import Timer

from flask import Flask

from DS_annotator.annotations import Annotations
from DS_annotator.server.flask import init_flask
from DS_annotator.server.jsonrpc import init_jsonrpc


def repeater(seconds, func):
    print("Save annotations")
    func()
    Timer(seconds, repeater, args=(seconds, func) ).start()


if __name__ == '__main__':

    if len(sys.argv) != 3:  # Number of arguments correct
        print("Usage: {} <path dataset> <path annotations CSV file>".format(sys.argv[0]))
        exit(0)
    path_dir_imgs = sys.argv[1]
    path_file_out = sys.argv[2]

    # Dataset exists
    if not os.path.isdir(path_dir_imgs):
        print("ERROR: cannot find {}".format(path_dir_imgs))
        exit(0)

    print("Data directory: {}".format(os.path.abspath(path_dir_imgs)))
    print("Annotations file: {}".format(os.path.abspath(path_file_out)))



    annotations = Annotations(path_dir_imgs, path_file_out)

    # Save the CSV every 3 minutes.
    repeater(3*60, annotations.save)

    # set the project root directory as the static folder, you can set others.
    app = Flask(__name__, static_url_path='')
    init_flask(app, path_dir_imgs, path_file_out)
    init_jsonrpc(app, annotations)


    app.run(host='0.0.0.0', debug=True)
