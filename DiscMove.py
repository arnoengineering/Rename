import os.path
import shutil
import exifread
from ExRead import image_disc

# Path for sorted files to be stored
# If it doesn't exist, creates a new one
dirs_path = "D:\\Sorted\\"
if not os.path.exists(dirs_path):
    os.mkdir(dirs_path)

# Where images to be organized are located
images_path = "C:\\Users\\parno\\Desktop\\La Pas"

fail_count = 0
success_count = 0
start_num = 0


# Recursively walk through all subdirectories and store the path + name of the jpg images
images = []
pic_rename = []


for root, dirs, files in os.walk(images_path):
    for f in files:
        # I'm only interested in pictures
        if f.endswith(".jpg") or f.endswith(".NEF"):
            images.append(f)


# Extracts the date an image was taken and moves it to a folder with the format YYYY.MM
# If the image doesn't have EXIF tags or has description, sends it to a different folder
for img_path in images:
    fold = os.path.dirname(img_path)  # dir to file
    img = os.path.basename(img_path)  # filename
    parent_dir = fold.split('\\')[-1]  # last dir
    had_dir = image_disc(img_path, parent_dir)  # to grab disc

    with open(img_path, "rb") as file:
        if had_dir:  # add to description files
            date_path = "Had Description"
            fail_count += 1

        else:
            tags = exifread.process_file(file, details=False, stop_tag="DateTimeOriginal")

            try:
                date_path = str(tags["EXIF DateTimeOriginal"]).replace(":", ".")[:7]
                success_count += 1

            except:
                print(str(img_path) + " does not have EXIF tags.")
                fail_count += 1
                date_path = "No Date"
        if not os.path.exists(dirs_path + date_path):
            os.mkdir(dirs_path + date_path)

    shutil.move(img_path, dirs_path + date_path + "\\" + img)  # moves to correct dir


print("Sorted " + str(success_count) + " files.")  # Images properly sorted by date taken
print("Failed to sort " + str(fail_count) + " files.")  # Images sent to 0000
