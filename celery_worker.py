import glob
import os
import psycopg2

from PIL import Image
from celery import Celery

BROKER = 'pyamqp://guest@localhost//'

app = Celery('celery_worker', broker=BROKER)


def update_file_status(filename):
    con = psycopg2.connect(
        database='dr_service_db', user='postgres',
        password='example', host='localhost', port=5432
    )
    cursor = con.cursor()
    cursor.execute(f"""UPDATE task_queue SET status='Done' 
                    where filename='{filename}'""")
    con.commit()
    con.close()


@app.task
def do_image_512(path):
    height = 512
    width = 512
    for infile in glob.glob(path):
        file, ext = os.path.splitext(infile)
        with Image.open(infile) as im:
            new_img = im.resize((height, width), Image.ANTIALIAS)
            im.mode = 'RGB'
            new_img.save(file + "_MINI.jpeg", "JPEG")
            update_file_status(f'{file}.jpeg')
    return 'Successfully'
