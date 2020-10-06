import os
import uuid


def save_image(args, *images):
    try:
        uuids = {}
        for image in images:
            image_file = args[image]
            if image_file is not None:
                image_uuid = str(uuid.uuid4())
                image_extension = os.path.splitext(image_file.filename)[1]
                image_file.save(os.path.join('authserver/images', image_uuid + image_extension))
                uuids[image_file.filename] = image_uuid + image_extension
        return uuids

    except Exception as e:
        print('error in save image')
        print(e)
        return 'error'


def delete_image(images):
    try:
        for key, value in images.items():
            os.remove(os.path.join('authserver/images', value))

    except Exception as e:
        print(e)
        return 'error'


def create_image_query(images):
    try:
        image_query = ' '
        index = 0
        for key, value in images.items():
            index = index + 1
            image_query += '_name'+str(index)+'=>%('+key+')s, _img'+str(index)+'path=>%('+value+')s,'

        return image_query[:-1] + ')'

    except Exception as e:
        print(e)
        return 'error'


def update_arg_for_image(data):
    try:
        args = {}
        for key, value in data.items():
            args[key] = key
            args[value] = value
        return args
    except Exception as e:
        print(e)
        return 'error'
