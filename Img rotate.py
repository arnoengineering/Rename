import os

from PIL import Image

path = r'N:\P + V\Mom Split'
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.jpg'):
            parent_dir, ang_dir = root.split('\\')[-2:]  # dir for name and angle
            try:
                ang = int(ang_dir)
            except ValueError:  # todo what error
                print('error with dir ', root)
                break  # stops rerunning code for same albs if already checked
            else:
                if ang == 0:
                    break
                img = Image.open(os.path.join(root, file))
                img = img.rotate(ang)
                img.save(os.path.join(parent_dir, file))  # moves to original dir
