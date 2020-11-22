import RenameMod
from ExRead import mp3  # todo eval

path = input("path: ")  # 'P:/Music/Adventures in Odyssey'

def last_ep():
    last_num = int(input("Last Episode #: "))

    RenameMod.rename_pre_num(last_num, path)


# add prefix or remove text
def partial_text():
    remove = input('Remove: ')  # remove what from file
    prefix = input('Prefix: ')

    RenameMod.rename_text(path, remove, prefix)


# removes series name
def series_rem():
    series = input('Series ')  # what directory to edit
    RenameMod.rename_text(path, remove=series)


# renames all files in sub-dirs
def multi_dir():
    file_list = RenameMod.rename_walk(path)  # list of all sub dir and files
    RenameMod.rename_pre_num(file_list)


# renames based on names in file
def file_ren():
    file = input('Path to File with Names')

    RenameMod.rename_file(path, file)


def list_ren():
    names = []  # list of ep names
    RenameMod.rename_ep_num(path, names)


def rename_movies():
    rep_dir = {'+': ' ', '-720': '', 'SD': '', 'HD': ''}  # dict of what to replace
    RenameMod.remove_dict(path, rep_dir)


def great_course():
    names = []
    num = 0
    with open('P:/DVD Rips/GC OC.txt', 'r') as f:  # open File
        for line in f:
            if '<div class="lecture-title">' in line:  # checks for x in line the splits by tex in tile
                line = line.split('<div class="lecture-title">')
                line = line[1]
                line = line.split('</div>')
                line = line[0]
                names.append(str(num) + ' ' + line)
    RenameMod.rename_ep_num(path, names)  # to rename


def get_mp3():
    pa = 'P:/Music/Adventures in Odyssey'
    to_ed = RenameMod.rename_walk(pa)
    for fi, di in to_ed.items():  # adds mp3 tags to all files and alb
        mp3(fi, di)


eval(input('What function to run'))  # to accesses correct function
