import glob
import os

from PIL import Image
from celery import Celery

app = Celery('celery_worker', broker='pyamqp://guest@localhost//')


@app.task
def do_image_512(path):
    size = 512, 512
    for infile in glob.glob(path):
        file, ext = os.path.splitext(infile)
        with Image.open(infile) as im:
            im.thumbnail(size)
            im.save(file + "MINI.jpg", "JPEG")
    return 'Successfully'


