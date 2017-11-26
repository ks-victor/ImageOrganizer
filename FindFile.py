import hashlib
import os
import shutil
import sys

#root_path = '/Volumes/Small/Audio/'
root_path = '/Volumes/Small/Documents/'
#root_path = '/Users/lallepot/Desktop/testing'

dubdir = root_path+"/dub"

dict = {}
file = ""

dubs = 0
total = 0
workload = 0

print root_path

for root, dirs, filenames in os.walk(root_path):
    for filename in filenames:
        if root == dubdir:
            continue
        if filename[:1] == '.':
            continue
        workload = workload + 1
        print "\rCalculating Workload:", workload,
print ""

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
        #print "\r", file,
        for x in dict:
            if x == file:
                break
            else:
                if dict[x] == hash:
                    if not os.path.isdir(dubdir):
                        os.mkdir(dubdir)
                    shutil.move(file, dubdir+'/'+filename)
                    dubs = dubs + 1
                    break
        dict.update({file: hash})
        total = total + 1
        print "\rProgress:", total , "/", workload, "(Duplicates:", str(dubs)+")",
print ""

print "Checked Files: ", total,"\n", "Number of Duplicates:", dubs
