from os.path import join, dirname, realpath
from flask import Flask, flash, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from celery_worker import do_image_512


ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')
SECRET_KEY = "super_secret_key"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 5242880
app.secret_key = SECRET_KEY


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return redirect(url_for('get_image'))


@app.route('/get_image', methods=['GET', 'POST'])
def get_image():
    if request.method == 'GET':
        return render_template('index.html', title="Get Image")
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'file not in request.files'
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(join(app.config['UPLOAD_FOLDER'], filename))
            return 'OK'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
