import os

import exifread
from RenameMod import rename

# variables
dirs_left = []

# edit options
path_main = r'C:\Users\parno\Desktop\La Pas'  # 'N:\\P + V\\Photos'  # input('Path: ')  # what directory to edit

# if has special name
dict_to_edit = {}
# dir_to_edit = [# 'GradParents\\The Gir', 'Hobbies\\Awana''s Rally 2011', 'Sleeping']


class PicLoop:
    def __init__(self, pa, re_name):
        self.to_ren = ("DSC", 'Chr', 'IMG', 'Snow Nov', re_name[:3])  # tuple, always grabs short

        # self assigned variables
        self.re_name = re_name
        self.path = pa

        # lists
        self.left_list = []
        self.file_list = {}
        self.fail_pic = {}
        self.fail_exif = []  # list of pics failed in EXIF
        self.pic_list = []  # list of all pics with possibility to edit

        # variables
        self.num = 0
        self.start_num = 0
        self.success_rename = 0
        self.fail_rename = 0
        self.first_run = True
        self.un_ed = 0

    # finds EXIF Dates on pics
    def exif_pic(self, dir_pics):
        for f in dir_pics:  # loops through all files in list to edit
            f_full = os.path.join(path, f)
            # opens full file-path to grab Metadata
            with open(f_full, "rb") as file:
                tags = exifread.process_file(file, details=False, stop_tag="DateTimeOriginal")
                try:
                    date_path = str(tags["EXIF DateTimeOriginal"]).replace(":", ".")
                    self.file_list[date_path] = f
                except:  # todo exception
                    print(str(f) + " does not have EXIF tags.")
                    self.fail_exif.append(f)  # list to run at end

    # loops through pics in list or dir, sorts and renames files
    def loop_pic(self, num, f_dir):  # list or dir of files
        f_list = []  # variable as to not edit the original list

        if type(f_dir) is dict:  # sorts and changes dict to list
            for x in sorted(f_dir.keys()):
                f_list.append(f_dir[x])
        else:
            f_list = f_dir

        for file in f_list:
            f_name, f_type = os.path.splitext(file)
            num += 1  # num to name files.

            if self.first_run:  # renames files and modifies list of files to edit
                new_name = f_name + '-edit'  # adds to file to avoid 'filer already exists error'
                f_dir[num - 1] = new_name + f_type  # adds new name to dict: thus exif_pic can find new name
            else:
                new_name = self.re_name + ' ' + str(num)  # renames file in order with prefix and num

            new_file = new_name + f_type  # adds extension
            if new_file != file:
                try:
                    rename(file, new_file, path)
                    if not self.first_run:  # to avoid duel count since first run is not a success
                        self.success_rename += 1
                except (FileNotFoundError, FileExistsError) as e:
                    self.fail_pic[file] = new_file  # keeps order and dir
                    print(e)
                    print('error: {} with file:{}'.format(e, new_file))
        self.num = num  # saves last num
        self.first_run = False  # resets val for second run

    def main(self):
        try:
            pic_dir = os.listdir(self.path)
        except FileNotFoundError:
            print('error with dir ' + self.path)
            dirs_left.append(self.path)
        else:
            for fi in pic_dir:  # loops to find files to edit
                if fi.endswith('.db'):  # removes thumbs
                    pic_dir.remove(fi)
                    self.un_ed -= 1  # leaves u unedited
                if fi.startswith(self.to_ren):
                    if fi.endswith('.NEF') or fi.lower().endswith('.jpg'):  # allows for JPG
                        self.pic_list.append(fi)
                    else:
                        self.left_list.append(fi)
                else:
                    self.un_ed += 1
            print("editing {} files".format(len(self.pic_list)))
            self.loop_pic(self.start_num, self.pic_list)  # first_run to add suffix and update edit list

            self.exif_pic(self.pic_list)  # grabs exif data and
            # renames for real and returns last_num, for pics_sans_date
            self.loop_pic(self.start_num, self.file_list)
            self.loop_pic(self.num, self.fail_exif)

            for o_file, n_file in self.fail_pic.items():  # tries a second rename in case first fails
                try:
                    rename(o_file, n_file, path)
                    self.success_rename += 1
                except (FileNotFoundError, FileExistsError) as e:
                    print('Second error {} at num: {}'.format(e, n_file))
                    self.fail_rename += 1

            print('{} files unedited of {}'.format(self.un_ed, len(pic_dir)))  # todo add fail num cor, and for each alb
            print("Finished with {} success, and {} failures".format(len(self.file_list), len(self.fail_exif)))
            print('edit {} successes, and {} failures'.format(self.success_rename, self.fail_rename))
            if len(self.left_list) > 0:
                print('Not images: ')
                print(self.left_list)


for root, dirs, files in os.walk(path_main):  # loops through all and sees if to name
    for alb in dirs:
        if alb in dict_to_edit.keys():  # checks for name
            name = dict_to_edit[alb]  # sets name to my name, use dor double dirs
        else:
            name = alb  # name = alb name
        try:
            path = os.path.join(root, alb)
        except FileNotFoundError:  # adds to list of errors
            print('unable to edit ' + alb)
            dirs_left.append(alb)
        else:
            print('editing ', alb)
            edit_dir = PicLoop(path, name)  # initialises class
            edit_dir.main()  # starts main class exclusion


print(dirs_left)
