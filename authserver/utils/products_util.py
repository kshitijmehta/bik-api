import os
import uuid
import functools
from PIL import Image
from authserver import app


def image_transpose_exif(im):
    """
    Apply Image.transpose to ensure 0th row of pixels is at the visual
    top of the image, and 0th column is the visual left-hand side.
    Return the original image if unable to determine the orientation.

    As per CIPA DC-008-2012, the orientation field contains an integer,
    1 through 8. Other values are reserved.

    Parameters
    ----------
    im: PIL.Image
       The image to be rotated.
    """

    exif_orientation_tag = 0x0112
    exif_transpose_sequences = [                   # Val  0th row  0th col
        [],                                        #  0    (reserved)
        [],                                        #  1   top      left
        [Image.FLIP_LEFT_RIGHT],                   #  2   top      right
        [Image.ROTATE_180],                        #  3   bottom   right
        [Image.FLIP_TOP_BOTTOM],                   #  4   bottom   left
        [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],  #  5   left     top
        [Image.ROTATE_270],                        #  6   right    top
        [Image.FLIP_TOP_BOTTOM, Image.ROTATE_90],  #  7   right    bottom
        [Image.ROTATE_90],                         #  8   left     bottom
    ]

    try:
        seq = exif_transpose_sequences[im._getexif()[exif_orientation_tag]]
    except Exception:
        return im
    else:
        return functools.reduce(type(im).transpose, seq, im)


def save_image(args, *images):
    try:
        uuids = {}
        for image in images:
            image_file = args[image]
            if image_file is not None:
                image_uuid = str(uuid.uuid4())
                image_extension = os.path.splitext(image_file.filename)[1]
                ## Saving original size image
                image_file.save(os.path.join('authserver/unscaledImages', image_uuid + image_extension))
                ## Saving reduced size image
                img = Image.open(os.path.join('authserver/unscaledImages', image_uuid + image_extension))
                img = image_transpose_exif(img)
                basewidth = 800
                wpercent = (basewidth / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                # Rotating image is the width > height
                # if basewidth > hsize:
                #     img = img.rotate(90, expand=True)
                img.save(os.path.join('authserver/scaledImages', image_uuid + image_extension), optimize=True, quality=95)

                uuids[image_file.filename] = image_uuid + image_extension
        return uuids

    except Exception as e:
        print('error in save image')
        app.logger.debug(e)
        return 'error'


def delete_image(images):
    try:
        for key, value in images.items():
            print(os.path.join('authserver/scaledImages', value))
            os.remove(os.path.join('authserver/scaledImages', value))
            os.remove(os.path.join('authserver/unscaledImages', value))

    except Exception as e:
        app.logger.debug(e)
        return 'error'


def delete_image_while_update(images):
    try:
        for value in images:
            os.remove(os.path.join('authserver/scaledImages', value))
            os.remove(os.path.join('authserver/unscaledImages', value))

    except Exception as e:
        app.logger.debug(e)
        return 'error'


def create_image_query(images):
    try:
        image_query = ' '
        index = 0
        for key, value in images.items():
            index = index + 1
            image_query += '_name' + str(index) + '=>%(' + key + ')s, _img' + str(index) + 'path=>%(' + value + ')s,'

        return image_query[:-1] + ')'

    except Exception as e:
        app.logger.debug(e)
        return 'error'


def update_arg_for_image(data):
    try:
        args = {}
        for key, value in data.items():
            args[key] = key
            args[value] = value
        return args
    except Exception as e:
        app.logger.debug(e)
        return 'error'


def create_tuple_for_product_details(combo_data, product_id, inr_price, usd_price):
    try:
        product_details = ''
        product_id_inr_usd_string = str(product_id) + ', ' + str(inr_price) + ',' + str(usd_price) + ', '
        for combo in combo_data:
            if 'productDetailId' in combo and combo['productDetailId'] == '0':
                product_details = product_details + '(' + product_id_inr_usd_string
                for key, value in combo.items():
                    if key != 'productDetailId':
                        product_details = product_details + str(value) + ','
                product_details = product_details[:-1]
                product_details = product_details + '),'
        product_details = product_details[:-1]
        return product_details
    except Exception as e:
        app.logger.debug(e)
        return e
