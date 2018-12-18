# -*- coding: utf-8 -*-


import argparse
# See: https://docs.python.org/3/library/argparse.html#the-add-argument-method


def get_args():
     # Argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path_imgs",
        type=str,
        help="images folder"
    )
    parser.add_argument(
        "--csv",
        type=str,
        action="store",
        help="csv file to store the annotations"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        action="store",
        help="server port"
    )
    return parser.parse_args()
