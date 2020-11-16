import os

import exifread
from RenameMod import rename

# variables
start_num = 0
success_rename = 0
left_list = []
file_list = {}
fail_pic = {}
fail_exif = []  # list of pics failed in EXIF
pic_list = []  # list of all pics with possibility to edit
uned_dir = []

# edit options
path_main = 'N:\\P + V\\Photos'  # input('Path: ')  # what directory to edit
# alb_n = input('Name: ')  # what to call files

# run with all paths in, # todo 'Fun With Dad': 'Throwing Ice', 'GradParents\\Family Joshua':
# Ice Crac\\Frozen Lake; i,
dir_to_edit = ['GradParents\\Jannel', 'GradParents\\Ouma', 'GradParents\\Oupa',
               'GradParents\\The Gir', 'Hobbies\\Awana''s Rally 2011', 'Hobbies\\Guns', 'Hobbies\\Lego',
               'Hobbies\\Rockets', 'House', 'Ipad-GoPro\\Ipad Wierd', 'Ipad-GoPro\\Go Pro', 'La Pas', 'Nerf',
               'New House LLB', 'Phone', 'Portrates', 'Sleeping', 'Sobeys', 'Stanards', 'Summer',
               'Youth Banquet\\Youth']


# finds EXIF Dates on pics
def exif_pic(dir_pics):
    for f in dir_pics:  # loops through all files in list to edit
        f_full = os.path.join(path, f)
        # opens full file-path to grab Metadata
        with open(f_full, "rb") as file:
            tags = exifread.process_file(file, details=False, stop_tag="DateTimeOriginal")
            try:
                date_path = str(tags["EXIF DateTimeOriginal"]).replace(":", ".")
                file_list[date_path] = f
            except:  # todo exception
                print(str(f) + " does not have EXIF tags.")
                fail_exif.append(f)  # list to run at end


# loops through pics in list or dir, sorts and renames files
def loop_pic(num, f_dir, first_run=False):  # list or dir of files
    global success_rename
    f_list = []  # variable as to not edit the original list

    if type(f_dir) is dict:  # sorts and changes dict to list
        for x in sorted(f_dir.keys()):
            f_list.append(f_dir[x])
    else:
        f_list = f_dir

    for file in f_list:
        f_name, f_type = os.path.splitext(file)
        num += 1  # num to name files.

        if first_run:  # renames files and modifies list of files to edit
            new_name = f_name + '-edit'  # adds to file to avoid 'filer already exists error'
            f_dir[num - 1] = new_name + f_type  # adds new name to dict: thus exif_pic can find new name
        else:
            new_name = alb_n + ' ' + str(num)  # renames file in order with prefix and num

        new_file = new_name + f_type  # adds extension
        if new_file != file:
            try:
                rename(file, new_file, path)
                if not first_run:  # to avoid duel count since first run is not a success
                    success_rename += 1
            except (FileNotFoundError, FileExistsError) as e:
                fail_pic[file] = new_file  # keeps order and dir
                print(e)
                print('error: {} with file:{}'.format(e, new_file))

    return num  # num for files with no date


def main(ren_val):  # todo glob var and reset, maybe class
    global file_list, fail_pic, fail_exif, pic_list, success_rename, left_list
    left_list = []
    file_list = {}
    fail_pic = {}
    fail_exif = []  # list of pics failed in EXIF
    pic_list = []  # list of all pics with possibility to edit
    un_ed = 0
    fail_rename = 0
    try:
        pic_dir = os.listdir(path)
    except FileNotFoundError:
        print('error with dir ' + path)
        uned_dir.append(path)
    else:
        for fi in pic_dir:  # loops to find files to edit
            if fi.endswith('.db'):  # removes thumbs
                pic_dir.remove(fi)
                un_ed -= 1  # leaves u unedited
            if fi.startswith(ren_val):
                if fi.endswith('.NEF') or fi.lower().endswith('.jpg'):  # allows for JPG
                    pic_list.append(fi)
                else:
                    left_list.append(fi)
            else:
                un_ed += 1

        print("editing {} files".format(len(pic_list)))
        loop_pic(start_num, pic_list, True)  # first_run to add suffix and update edit list

        exif_pic(pic_list)  # grabs exif data and
        last_num = loop_pic(start_num, file_list)  # renames for real and returns last_num, for pics_sans_date
        loop_pic(last_num, fail_exif)

        for o_file, n_file in fail_pic.items():  # tries a second rename in case first fails
            try:
                rename(o_file, n_file, path)
                success_rename += 1
            except (FileNotFoundError, FileExistsError) as e:
                print('Second error {} at num: {}'.format(e, n_file))
                fail_rename += 1

        print('{} files unedited of {}'.format(un_ed, len(pic_dir)))
        print("Finished with {} success, and {} failures".format(len(file_list), len(fail_exif)))
        print('edit {} successes, and {} failures'.format(success_rename, fail_rename))
        if len(left_list) > 0:
            print('Not images: ')
            print(left_list)


if type(dir_to_edit) is dict:
    pass  # todo add his here
for alb in dir_to_edit:  # todo change if not dir
    try:
        path = os.path.join(path_main, alb)
    except:  # todo exception type
        print('unable to edit ' + alb)
    alb_n = alb.split('\\')[-1]  # last album
    if len(alb_n) >= 4:
        name_ren = alb_n[:3]
    else:
        name_ren = alb_n
    to_ren = ("DSC", 'Chr', 'IMG', 'Snow Nov', name_ren)
    main(to_ren)
print(uned_dir)
