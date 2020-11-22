import os

from PIL import Image

path = ''
file_dir = os.listdir(path)
parent_dir = path.split('\\')[-1]
try:
    ang = int(parent_dir)
except ValueError:  # todo what error
    print('error with dir ', path)
else:
    if ang != 0:
        for file in file_dir:
            file = os.path.join(path, file)
            img = Image.open(file)
            img = img.rotate(ang)
            img.save(file)
