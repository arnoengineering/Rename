import piexif
import os
from PIL import Image, UnidentifiedImageError

import mutagen
from mutagen.easyid3 import EasyID3


# grabs description from exif dict
def grab_disc(ex_dict):  # same for both
    has_disc = True
    if 270 not in ex_dict.keys():  # if no tag, one is added so  for key assignment
        ex_dict[270] = b''
    # Type: bytes so string to see if one already
    disc = ex_dict[270].decode('utf-8')
    if len(disc.replace(' ', '')) == 0:  # if no description returns false so I can add one
        has_disc = False
    return has_disc  # if empty


# changes description in exif data
def image_disc(img_path, n_disc):
    had_disc = True
    load_error = False
    try:  # avoid opening error
        with Image.open(img_path) as img:  # loads image
            if img_path.endswith('.NEF'):
                ex_dict = img.tag  # nef tag
                had_disc = grab_disc(ex_dict)
                if not had_disc:
                    img.tag[270] = n_disc
            elif img_path.lower().endswith('.jpg'):
                ex_dict = piexif.load(img.info['exif'])  # gets metadata
                # description at 0th, 270.
                ex_0 = ex_dict['0th']  # 0th key
                had_disc = grab_disc(ex_0)   # zeroth key is update

                if not had_disc:
                    ex_dict['0th'] = ex_0  # since zeroth key is updated, we can dump all back
                    ex_bytes = piexif.dump(ex_dict)  # changes disc
                    piexif.insert(ex_bytes, img_path)  # adds to photo

    except (KeyError, UnidentifiedImageError) as e:
        print('error {} with image {}'.format(e, img_path.split('/')[-1]))  # prints image
        load_error = True
    return had_disc, load_error


def img_date(image, year, mon, day):
    exif_dict = piexif.load(image)
    new_date = '{}:{}:{} 12:00:00'.format(year, mon, day) # default time
    exif_dict['0th'][piexif.ImageIFD.DateTime] = new_date
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = new_date
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = new_date
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image)


def mp3(file, alb, artist='Adventures in Odyssey'):  # use for mp3, but default odyssey
    if file.endswith('.mp3'):  # so only works with mp3
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
