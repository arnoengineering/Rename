import os
from PIL import Image

path = ''
new_dir = ''
size = (200, 400)  # x, y pix
for root, dirs, files in os.walk(path):
    for d in dirs:
        pass


def split_files(file_path, img_size):
    num = 0  # what sub
    img = Image.open(file_path)
    # gets img name and basename
    img_name = os.path.basename(file_path)
    parent_dir = os.path.dirname(file_path).split('\\')[-1]

    # loops through x and y valuse in 2x2 grid
    for x in range(1):
        for y in range(1):
            num += 1
            sub_rec = (x * img_size[0] // 2, y * img_size[1] // 2,
                       (x + 1) * img_size[0] // 2, (y + 1) * img_size[1] // 2)  # min max by floor
            sub_img = img.crop(sub_rec)  # put in loop
            save_dir = os.path.join(new_dir, parent_dir)
            # makes dir if not present
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            sub_img.save(os.path.join(new_dir, img_name))  # names in new dir


