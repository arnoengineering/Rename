import os
from PIL import Image

path = ''
new_dir = ''
sie = (200, 400)  # x, y pix
for root, dirs, files in os.walk(path):
    for file in files:
        pass


def split_files(file_path, img_size):
    num = 0  # what sub
    img = Image.open(file_path)
    img_name = os.path.basename(file_path)
    for x in range(1):
        for y in range(1):
            num += 1
            sub_rec = (x * img_size[0] // 2, y * img_size[1] // 2,
                       (x + 1) * img_size[0] // 2, (y + 1) * img_size[1] // 2)
            sub_img = img.crop(sub_rec)  # put in loop
            sub_img.save(os.path.join(new_dir, img_name))  # naves in new dir  # todo where to save


