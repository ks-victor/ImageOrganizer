import hashlib
import os
import shutil

root_path = '/Volumes/Small/Pictures/jpg'

#root_path = '/Users/lallepot/Desktop/testing'

dubdir = root_path+"/dub"

dict = {}
file = ""

dubs = 0
total = 0

if not os.path.isdir(dubdir):
    os.mkdir(dubdir)

for root, dirs, filenames in os.walk(root_path):
    # folder level
    for filename in filenames:
        # file level
        if root == dubdir:
            continue
        if filename[:1] == '.':
            continue
        file = os.path.join(root, filename)
        hash = hashlib.md5(open(file, 'rb').read()).hexdigest()
        print file
        for x in dict:
            if x == file:
                break
            else:
                if dict[x] == hash:
                    shutil.move(file, dubdir+'/'+filename)
                    dubs = dubs + 1
                    break
        dict.update({file: hash})
        total = total + 1

print "Checked Files: ", total,"\n", "Number of Duplicates:", dubs
