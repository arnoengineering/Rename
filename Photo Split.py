import os
from ExRead import dir_date
from PIL import Image, UnidentifiedImageError

path = input('Path to edit: ')
new_dir = r'N:\P + V\Mom Split'
ren_in = input('Rename files? (n for split): ')
th_in = input('In thirds? (n for quarter)')
three = False  # third or quarter

if ren_in.lower() == 'y' or ren_in.lower() == 'yes':
    rename = True  # rename or split
else:  # only needs to work if not rename
    rename = False
    if th_in.lower() == 'y' or th_in.lower() == 'yes':
        three = True

size = (200, 400)  # x, y pix
third_val = {(15, 620): (0, 900), (630, 1240): (0, 900), (125, 1020): (910, 1500)}  # if split by 3
norm_val = [[(15, 540), (560, 1100)], [(0, 750), (760, 1500)]]  # if quartered

total = 0
error = 0
dir_list = []


# third if photo to be split by 3
def split_files(file_path, third=False):
    global error
    split_rec = []
    num = 0  # what sub
    if file_path.endswith('.NEF') or file_path.lower().endswith('.jpg'):
        try:
            img = Image.open(file_path)
            # gets img name and basename
            img_name, ext = os.path.splitext(os.path.basename(file_path))
            parent_dir = os.path.dirname(file_path).split('\\')[-1]

            if third:  # splits image into 3
                for x_tup, y_tup in third_val.items():
                    x, x_max = x_tup
                    y, y_max = y_tup
                    sub_rec = (x, y, x_max, y_max)
                    split_rec.append(sub_rec)

            else:  # loops through x and y values in 2x2 grid
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
                sub_img.save(os.path.join(save_dir, new_name + ext))  # names in new dir

        except UnidentifiedImageError:
            error += 1
            print('error with image ', file_path)
    return num


for root, dirs, files in os.walk(path):
    if rename:  # loops through all dir tor rename
        for di in dirs:
            dir_list.append(os.path.join(root, di))

    else:
        for file in files:  # slits files by 3 or 4
            file = os.path.join(root, file)
            num_r = split_files(file, three)
            total += num_r

if rename:
    er = dir_date(dir_list)
    if er:  # if error in image date error is added, same format for print
        error += 1
    else:
        total += 1

print('finished editing {} images, with {} errors'.format(total, error))
