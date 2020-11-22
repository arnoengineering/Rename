import os

from PIL import Image

path = r'N:\P + V\Mom Split'
for root, dirs, files in path:
    for file in files:
        parent_dir, ang_dir = root.split('\\')[-2:]
        try:
            ang = int(ang_dir)
        except ValueError:  # todo what error
            print('error with dir ', root)
            break
        else:
            if ang != 0:
                img = Image.open(os.path.join(root, file))
                img = img.rotate(ang)
                img.save(os.path.join(parent_dir, file))
