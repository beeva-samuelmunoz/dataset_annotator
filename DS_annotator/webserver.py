"""Webserver
"""

import os
import sys
from threading import Timer

from flask import Flask

from DS_annotator import utils
from DS_annotator.annotations import Annotations
from DS_annotator.server.flask import init_flask
from DS_annotator.server.jsonrpc import init_jsonrpc


def repeater(seconds, func):
    print("Save annotations")
    func()
    Timer(seconds, repeater, args=(seconds, func) ).start()


if __name__ == '__main__':
    # Parse arguments
    args = utils.get_args()
    # Dataset musts exist
    if not os.path.isdir(args.path_imgs):
        print("ERROR: cannot find {}".format(args.path_imgs))
        exit(0)
    args.path_imgs = os.path.abspath(args.path_imgs)
    # Default CSV file
    if not args.csv:
        args.csv = os.path.join(args.path_imgs,"annotations.csv")
    args.csv = os.path.abspath(args.csv)

    # Server info
    print("Server info")
    print("\tData directory: {}".format(args.path_imgs))
    print("\tAnnotations CSV file: {}".format(args.csv))
    print("\tServer Port: {}".format(args.port))

    annotations = Annotations(args.path_imgs, args.csv)

    # Save the CSV every 3 minutes.
    repeater(3*60, annotations.save)

    # set the project root directory as the static folder, you can set others.
    app = Flask(__name__, static_url_path='')
    init_flask(app, args.path_imgs, args.csv)
    init_jsonrpc(app, annotations)

    app.run(host='0.0.0.0', port=args.port, debug=True)
