import os
from PIL import Image, UnidentifiedImageError

path = r'C:\Users\parno\Desktop\La Pas'
new_dir = r'C:\Users\parno\Desktop\LA S'
size = (200, 400)  # x, y pix


# third if photo to be split by 3
def split_files(file_path, third=False):
    if file_path.endswith('.NEF') or file_path.lower().endswith('.jpg'):
        num = 0  # what sub
        try:
            img = Image.open(file_path)
            # gets img name and basename
            img_name = os.path.basename(file_path)
            parent_dir = os.path.dirname(file_path).split('\\')[-1]

            if third:
                for x in [0, 1, 0.5]:
                    if x != 0.5:
                        y = 0
                    else:
                        y = 1
                    sub_rec = (x * size[0] // 2, y * size[1] // 2,
                               (x + 1) * size[0] // 2, (y + 1) * size[1] // 2)
                    sub_img = img.crop(sub_rec)  # put in loop  # todo make function
                    save_dir = os.path.join(new_dir, parent_dir)
                    # makes dir if not present
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)

                sub_img.save(os.path.join(new_dir, img_name))  # names in new dir
            else:
                # loops through x and y values in 2x2 grid
                for x in range(1):
                    for y in range(1):
                        num += 1
                        sub_rec = (x * size[0] // 2, y * size[1] // 2,
                                   (x + 1) * size[0] // 2, (y + 1) * size[1] // 2)  # min max by floor
                        sub_img = img.crop(sub_rec)  # put in loop
                        save_dir = os.path.join(new_dir, parent_dir)
                        # makes dir if not present
                        if not os.path.exists(save_dir):
                            os.makedirs(save_dir)

                        sub_img.save(os.path.join(new_dir, img_name))  # names in new dir
        except UnidentifiedImageError:
            print('error with image ', file)


for root, dirs, files in os.walk(path):
    for file in files:
        file = os.path.join(root, file)
        split_files(file)
