"""Web views for the server
"""

from flask import render_template, send_from_directory, send_file


def init_flask(app, path_dir_imgs, path_file_out):

    @app.route('/')
    def main():
        return render_template('main.html')

    @app.route('/get_annotations')
    def send_annotations():
        return send_file(path_file_out)

    @app.route('/img/<path:filename>')
    def send_img(filename):
        return send_from_directory(path_dir_imgs, filename)
