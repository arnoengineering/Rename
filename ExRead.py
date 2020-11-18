# add description to image
import exifread
import piexif
import os
from PIL import Image

import mutagen
from mutagen.easyid3 import EasyID3


def grab_dict(ex_dict):  # same for both
    has_disc = True
    if 270 not in ex_dict.keys():  # if not in, add to remove error
        ex_dict[270] = b''

    disc = ex_dict[270].decode('utf-8')
    if len(disc.replace(' ', '')) == 0:
        has_disc = False
    return has_disc  # if empty


def image_disc(img_path, n_disc):
    # if img_path.endswith('.NEF'): # change type
    had_disc = True
    load_error = False
    with Image.open(img_path) as img:  # loads image
        try:
            if img_path.endswith('.NEF'):
                ex_dict = img.tag  # nef tag
                had_disc = grab_dict(ex_dict)
                if not had_disc:
                    img.tag[270] = n_disc
            elif img_path.lower().endswith('.jpg'):
                ex_dict = piexif.load(img.info['exif'])  # gets metadata
                # description at 0th, 270. Type: bytes so string to see if one already
                ex_0 = ex_dict['0th']  # 0th key
                had_disc = grab_dict(ex_0)   # zeroth key is update

                if not had_disc:
                    ex_dict['0th'] = ex_0  # since zeroth key is updated, we can dump all back
                    ex_bytes = piexif.dump(ex_dict)  # changes disc
                    piexif.insert(ex_bytes, img_path)  # adds to photo

        except:
            print('error with image {}'.format(img_path.split('/')[-1]))  # prints image
            load_error = True
    return had_disc, load_error


def nef_data(img_path):
    f = open(img_path, 'rb')
    tags = exifread.process_file(f, details=False, stop_tag="DateTimeOriginal")
    print(tags)
    f.close()


def mp3(file, alb, artist='Adventures in Odyssey'):  # use for mp3, but default odyssey
    if file.endswith('.mp3'):  # todo maybe switch to mutagen, and add alb art # img_path = 'C:/A Images'
        try:
            tag = EasyID3(file)

        except:
            tag = mutagen.File(file, easy=True)
            tag.add_tags()

        num, name = os.path.basename(file).split(' ', 1)  # base file, then num and name
        name = name.replace('.mp3', '')  # removes end
        print(tag)
        tag['artist'] = artist
        tag['title'] = name
        tag['album'] = alb
        tag['tracknumber'] = num
        try:
            tag.save()
        except:
            print('error with {} in {}'.format(name, alb))
