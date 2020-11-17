# add description to image
import piexif
import os
from PIL import Image
# edits tags
import mutagen
from mutagen.easyid3 import EasyID3
from logging import exception


def image_disc(img_path, n_disc):
    had_disc = True
    img = Image.open(img_path)  # loads image
    try:
        ex_dict = piexif.load(img.info['exif'])  # gets metadata
        # description at 0th, 270. Type: bytes so string to see if one already
        disc = ex_dict['0th'][270].decode('utf-8')
        if len(disc.replace(' ', '')) == 0:
            ex_bytes = piexif.dump({'0th': {270: n_disc}})  # changes disc
            piexif.insert(ex_bytes, img_path)  # adds to photo
            had_disc = False
    except:
        print('error with image ' + img_path.split('/')[-1])  # prints image
    return had_disc


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
