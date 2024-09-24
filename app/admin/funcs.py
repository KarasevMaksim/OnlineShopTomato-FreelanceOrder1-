import os
import shutil
import secrets

from flask import current_app, url_for
from werkzeug.utils import secure_filename
from PIL import Image
from urllib.parse import unquote


def save_product_img(picture_name, sections_id):
    _, _ext = os.path.splitext(secure_filename(picture_name))
    new_picture_name = f"{secrets.token_hex(10)}{_ext}"
    
    full_path = os.path.join(
        current_app.root_path,
        'static',
        'img',
        'products',
        sections_id
    )
    
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        
    path_to_db = os.path.join('img', 'products', sections_id, new_picture_name).replace('\\', '/')
    path_to_save = os.path.join(full_path, new_picture_name)
    return path_to_save, path_to_db


def resized_image(file_obj, x=800, y=800):
    img = Image.open(file_obj)
    img.thumbnail((x, y))
    return img


def delete_product_img(img_path):
    try:
        full_path = current_app.root_path.replace('\\', '/') + img_path
        os.remove(unquote(full_path))
    except Exception as err:
        print(err)
        
        
def delete_paths_to_img(paths):
    for path in paths:
        try:
            full_path = current_app.root_path.replace('\\', '/') + path
            shutil.rmtree(unquote(full_path))
        except OSError as err:
            print(err)
