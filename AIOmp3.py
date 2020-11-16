import os

path = 'P:/Music/Adventures in Odyssey'
img_path = 'C:/A Images'  # images
atv_dir = os.listdir(path)  # all albums


def file_ed(file):
    file_path = os.path.join(alb_path, file)  # path to file


for album in atv_dir:
    alb_path = os.path.join(path, album)
    file_dir = os.listdir(alb_path)  # all the files in the specified directory
    alb_num = album.split(' ', 1)[0]
    img_f = img_path + '/' + alb_num + 'front.jpg'
    for f in file_dir:
        if os.path.isfile(f):
            file_ed(f)
