import os
from PIL import Image
from flask import url_for,current_app
from datetime import datetime


def add_image_pic(pic_upload):
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    suffix = datetime.now().strftime("%y%m%d_%H%M%S")
    storage_filename = str(suffix)+'.'+ext_type

    #ファイルのパス
    # filepath = os.path.join(current_app.root_path,'static/event_pics',storage_filename)
    #
    # output_size = (800,1200)
    # pic = Image.open(pic_upload)
    # pic.thumbnail(output_size)
    # pic.save(filepath)

    return storage_filename
