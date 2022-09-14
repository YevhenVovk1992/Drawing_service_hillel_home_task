from os.path import join, dirname, realpath
from flask import Flask, flash, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from flask_migrate import Migrate

from celery_worker import do_image_512
from models import db, TaskQueue

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'uploads')
SECRET_KEY = "super_secret_key"
DB_CONNECT = 'postgresql://postgres:example@localhost:5432/dr_service_db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECT
db.init_app(app)
migrate = Migrate(app, db)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = 5242880
app.secret_key = SECRET_KEY


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_status_db(filename):
    task = TaskQueue(filename=f'{filename}')
    try:
        db.session.add(task)
        db.session.commit()
    except AssertionError:
        return 'Connecting error'


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
            return render_template(
                'file_error.html', title="Error", error_messange='No file part'
            )
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return render_template(
                'file_error.html', title="Error", error_messange='No selected file'
            )
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path_file = join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path_file)
            try:
                do_image_512.apply_async(args=[path_file])
            except:
                return 'Something went wrong'
            else:
                add_status_db(filename)
            return render_template('get_image_success.html', title="Download file")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
