import os.path
import shutil
import exifread
from ExRead import image_disc

# Path for sorted files to be stored
# If it doesn't exist, creates a new one
dirs_path = r"N:\P + V\PH Sorted"
if not os.path.exists(dirs_path):
    os.mkdir(dirs_path)

# Where images to be organized are located
images_path = r"N:\P + V\Photos"

fail_count = 0
success_count = 0
start_num = 0

# files to get double dir
sub_dir = ['Edits', 'Weird', 'Notes', 'Alaska', 'Baltic', 'Greece', 'Mediterranean', 'New England', 'Norway']
# Recursively walk through all subdirectories and store the path + name of the jpg images
images = []
pic_rename = []
nef_pics = []


for root, dirs, files in os.walk(images_path):
    for f in files:
        # I'm only interested in pictures
        image_p = os.path.join(root, f)
        if f.lower().endswith(".jpg") or f.endswith('.NEF'):
            images.append(image_p)


# Extracts the date an image was taken and moves it to a folder with the format YYYY.MM
# If the image doesn't have EXIF tags or has description, sends it to a different folder
for img_path in images:
    fold = os.path.dirname(img_path)  # dir to file
    img = os.path.basename(img_path)  # filename

    parent_dir = fold.split('\\')[-1]  # last dir
    if parent_dir in sub_dir:  # two up description
        parent_dir = ', '.join(fold.split('\\')[-2:])
    had_dir, er_load = image_disc(img_path, parent_dir)  # to grab disc

    if had_dir:  # add to description files
        date_path = parent_dir + "Had Description"
        fail_count += 1
    elif er_load:
        date_path = parent_dir + " Exif error"
        fail_count += 1

    else:
        with open(img_path, "rb") as file:
            tags = exifread.process_file(file, details=False, stop_tag="DateTimeOriginal")

            try:
                date_path = str(tags["EXIF DateTimeOriginal"]).replace(":", ".")[:7]

                # check if posible
                try:
                    int(date_path[0])
                except ValueError:
                    print('Using datetime')
                    date_path = str(tags["Image DateTime"]).replace(":", ".")[:7]
                success_count += 1

            except KeyError:
                print(str(img_path) + " does not have EXIF tags.")
                fail_count += 1
                date_path = "No Date"
    if success_count >= 0 and success_count % 100 == 0:
        print('working')  # so you know its running
    new_path = os.path.join(dirs_path, date_path)
    if not os.path.exists(new_path):
        os.mkdir(new_path)

    try:
        shutil.move(img_path, new_path + "\\" + img)  # moves to correct dir
    except FileExistsError:
        shutil.move(img_path, new_path + "\\" + img + '-exits')  # moves to correct dir

print("Sorted " + str(success_count) + " files.")  # Images properly sorted by date taken
print("Failed to sort " + str(fail_count) + " files.")  # Images sent to 0000
