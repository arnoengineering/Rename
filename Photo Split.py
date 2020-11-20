import os
from PIL import Image, UnidentifiedImageError

path = r'C:\Users\parno\Desktop\La Pas'
new_dir = r'C:\Users\parno\Desktop\LA S'
size = (200, 400)  # x, y pix
third_val = {(15, 620): (0, 900), (630, 1240): (0, 900), (125, 1020): (910, 1500)}
norm_val = [[(15, 540), (560, 1100)], [(0, 750), (760, 1500)]]
total = 0
error = 0


# third if photo to be split by 3
def split_files(file_path, third=False):
    global error
    split_rec = []
    if file_path.endswith('.NEF') or file_path.lower().endswith('.jpg'):
        num = 0  # what sub
        try:
            img = Image.open(file_path)
            # gets img name and basename
            img_name = os.path.basename(file_path)
            parent_dir = os.path.dirname(file_path).split('\\')[-1]

            if third:
                for x_tup, y_tup in third_val.items():
                    x, x_max = x_tup
                    y, y_max = y_tup
                    sub_rec = (x, y, x_max, y_max)
                    split_rec.append(sub_rec)
            else:
                # loops through x and y values in 2x2 grid
                for x, x_max in norm_val[0]:
                    for y, y_max in norm_val[1]:
                        sub_rec = (x, y, x_max, y_max)
                        split_rec.append(sub_rec)

            for rec in split_rec:
                num += 1
                new_name = img_name + ' ' + str(num)
                sub_img = img.crop(rec)  # put in loop
                save_dir = os.path.join(new_dir, parent_dir)
                # makes dir if not present
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                sub_img.save(os.path.join(new_dir, new_name))  # names in new dir

        except UnidentifiedImageError:
            error += 1
            print('error with image ', file)
        return num


for root, dirs, files in os.walk(path):
    for file in files:
        file = os.path.join(root, file)
        nu = split_files(file)
        total += nu

print('finished editing {} images, with {} errors'.format(total, error))
