import os

from PIL import Image

path = ''
file_dir = os.listdir(path)
ang = int(input('angle CCW: '))  # angle from dir

for file in file_dir:
    file = os.path.join(path, file)
    img = Image.open(file)
    img = img.rotate(ang)
    img.save(file)
