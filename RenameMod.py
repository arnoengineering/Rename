# module to loop and rename
import os


def rename_text(path, remove='', prefix=''):
    file_dir = os.listdir(path)
    num = 0
    for f in file_dir:
        file, f_type = os.path.splitext(f)  # split to file type
        if len(prefix) != 0:  # if no pre, skip
            name = prefix + str(num)
        else:
            name = file.replace(remove, '')  # what to remove. if nothing, it will do nothing
        if name != file:
            name += f_type
            rename(f, name, path)


def rename_ep(path, num=0):
    file_dir = os.listdir(path)
    for file in file_dir:
        num += 1
        file.replace('(Cont.)', '')

        new_name = str(num) + " " + file
        rename(file, new_name, path)


def remove_dict(path, rep_dic):
    num = 0  # number renamed
    err = 0  # number of errors
    file_dir = os.listdir(path)
    for f in file_dir:
        file, f_type = os.path.splitext(f)

        n_file = file.split(')', 1)  # removes first bracket
        for i, x in rep_dic.items():
            n_file = n_file.replace(i, x)  # replaces dict keys, by values

        if n_file == f:
            err += 1
        else:
            num += 1
            n_file += f_type
            rename(f, n_file, path)

    print('finished renaming: {} files'.format(num))
    print('Error Renaming: {} files'.format(err))


def rename_pre_num(file_dir, last_n=0, path=''):
    ep_num = 0  # prevents premature reference if dir is empty
    for file in file_dir:
        if len(path) == 0 and last_n == 0:
            file, path = path_split(file)

            try:  # finds last num of disk
                last_n = 9 * (int(path[-1]) - 1)  # if od is left out
            except ValueError:
                last_n = 0

        num, no_num = file.split(' ', 1)  # origin num rem
        ep_num = num + last_n

        if '(Cont.)' in no_num:
            no_num.replace('(Cont.)', '')

        new_name = str(ep_num) + " " + no_num
        rename(file, new_name, path)
    return ep_num


def rename_file(path, name_f):
    names = []  # names of shows

    f = open(name_f, 'r')  # open file
    fi = f.read()
    fi.replace(":", "-")
    ep = fi.split('"')
    for i in range(1, len(ep)):
        if i % 2 != 0:
            names.append(ep[i])
    rename_ep_num(path, names)


def rename_ep_num(path, names):
    names = [x.replace(':', '') for x in names]  # replace extra in names
    names = [x.replace('?', '') for x in names]

    file_dir = os.listdir(path)

    for file in file_dir:
        n_file = file.replace("Ep", "")

        num, name = n_file.split(' ', 1)
        num = num.split('-')
        num1 = int(num[0])

        ep_name = ''  # empty string
        if len(num) > 1:  # thus 2 ep
            num2 = int(num[1])
            name_str = "Ep {}-{}".format(num1, num2)
        else:
            num2 = num1  # for loop
            name_str = "Ep " + str(num1)
        for i in range(num, num2):
            ep_name += names[i - 1]
            if i < num2 - 1:
                ep_name += ", "

        new_name = name_str + ep_name

        # renames files keeping same extension
        rename(file, new_name, path)


# sole rename
def rename(file, n_file, path):
    f_path = os.path.join(path, file)
    n_path = os.path.join(path, n_file)
    # renames files keeping same extension
    try:
        os.rename(f_path, n_path)
    except (FileExistsError, FileNotFoundError) as e:
        print("error {} with image {}".format(e, f_path))


def path_split(file_path):
    file = os.path.basename(file_path)
    path2_file = os.path.dirname(file_path)
    return file, path2_file


def rename_walk(path):
    file_list = {}  # list of files with dir
    for root, di, file in os.walk(path):
        for f in file:
            alb = root.split('\\')[-1]  # last alb
            file_path = os.path.join(root, f)
            file_list[file_path] = alb  # dir list
    print(file_list)
    return file_list


def walk_ren(path):
    for root, di, files in os.walk(path):
        alb = root.split('\\')[-1]  # last alb
        for num, file in enumerate(files):
            ext = os.path.splitext(file)[1]
            n_name = str(alb) + " " + str(num + 1)
            n_file = n_name + ext
            rename(file, n_file, root)


def ren_file_lines(file):
    f = open(file)
    lines = f.readlines()
    lines = [li.strip().split('  ', 1)[1] for li in lines if '  ' in li.strip()]
    lines = list(dict.fromkeys(lines))
    lines.sort()
    f.close()
    f = open(file, 'w')
    f.writelines(lines)


def mom_pics(f):
    p = r'J:\HPSCANS'
    with open(f) as fi:
        line = fi.readlines()
    for li in line:
        dir_n = os.path.join(p, li.strip())
        os.mkdir(dir_n)


# mom_pics(r'C:\Users\parno\Documents\mom_pics.txt')

p = r'J:\HPSCANS'
for root, dirs, f in os.walk(p):
    dir_range = {os.path.join(root, d): d.split('PIC')[1].replace(' ', '').split('-') for d in dirs}
    for fil in f:
        fi, ext = os.path.splitext(fil)
        try:
            f_num = int(fi.replace('PIC', ''))
            for d in dir_range.keys():
                if int(dir_range[d][0]) <= f_num <= int(dir_range[d][1]):
                    f_name = os.path.join(d, fil)
                    os.rename(os.path.join(root, fil), f_name)
        except (ValueError, FileExistsError):
            print("error", fil)
