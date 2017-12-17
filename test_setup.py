import shutil
import os

path = "/Users/lallepot/Desktop/testing/"
file = ""
dir_list = []
count = 0

def setup():

    src_path = path+"day0/"
    dst_path = path+"test/"

    # Clear out the TEST directory
    if os.path.isdir(dst_path):
        try:
            shutil.rmtree(dst_path)
        except Exception as e:
            print(e)
            exit(9)

    # Get list of DIRS
    for root, dirs, filenames in os.walk(src_path):
        for x in root.splitlines():
            dir_list.append(x)

    # Creates DIR in TEST
    for x in dir_list:
        x = x.replace("day0", "test")
        #logging x, os.path.isdir(x)
        if not os.path.isdir(x):
            os.makedirs(x)

    for root, dirs, filenames in os.walk(src_path):
        for filename in filenames:
            if filename[:1] == '.':
                continue
            src = os.path.join(root, filename)
            dst = src.replace("day0", "test")
            #print src, dst
            shutil.copy(src, dst)

    print("Enviroment Setup Done")
    print("*********************")


setup()
