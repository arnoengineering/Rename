import os
from PIL import Image, UnidentifiedImageError

# variables to count format and output
file_com = 0
file_err = 0
dir_err = 0
dir_list = []

path = input('Path to dir: ')


for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.jpg'):
            parent_dir, ang_dir = root.rsplit('\\', 1)  # dir for name and angle splits from right

            try:  # only runs on albums with images and have direction
                ang = int(ang_dir)
            except ValueError:
                print('error with dir ', root)
                dir_err += 1
                break  # stops rerunning code for same albs if already checked
            else:
                if parent_dir not in dir_list:  # so output of number of dirs done
                    dir_list.append(parent_dir)
                    print(parent_dir)
                # breaks if alb is zero
                if ang == 0:
                    break

                try:
                    img = Image.open(os.path.join(root, file))
                    out = img.rotate(ang, expand=True)  # expand to get original dimensions
                    out.save(os.path.join(parent_dir, file))  # moves to original dir
                    file_com += 1
                except UnidentifiedImageError:
                    print('error with file ', file)
                    file_err += 1

print('{} files completed with {} errors'.format(file_com, file_err))
print('{} dirs completed with {} errors'.format(len(dir_list), file_err))
