#!/usr/local/bin/python3.7
import os\
    , exifread\
    , logging\
    , argparse\
    , shutil\
    , datetime\
    , dhash

from time import time
from PIL import Image
from random import randint

### import test_setup

parser = argparse.ArgumentParser(description="Find duplicate files and moves them other folder")
parser.add_argument('root_path', type=str, action="store", help="Path to folder to scan")
parser.add_argument('-t', '--test', dest='testing', action='store_true', help="Testing Mode")
parser.add_argument('-vvv', action="store_const", dest="verbose", const='INFO')
parser.set_defaults(testing=True)

#parser.set_defaults(root_path="/Users/lallepot/Projects/ImageCleanUp/testing")
#parser.set_defaults(root_path="/Users/lallepot/Desktop/Backup/")
#parser.set_defaults(root_path="/Users/lallepot/Desktop/Pictures/")

parser.set_defaults(verbose="")


args = parser.parse_args()


filelist = []
exifData = ""
verbose = ""
hashlist = []
hashtable = {}
filetable = []
templist = []
filelist2 = []

def filewalk(path):
    print("Start 'Scanning'")
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if filename.rsplit(".",1)[1] not in ["png", "jpg", "tiff", "jpeg", "tif"]:
                continue
            if root == dubdir:
                continue
            if filename[:1] == '.':
                continue
            file = os.path.join(root, filename)
            filelist.append(file)
        print(" ... %s" % root)


def rename():
    print("Start 'Renaming'")
    for index, file in enumerate(filelist):
        print("\rRenaming File %d of %d" % (index+1, len(filelist)), end="");
        #print("in  rename:", index, file)
        try:
            f = open(file, 'rb')
        except Exception as e:
            print(" ... ", e, index, file)
        try:
            tag = str((exifread.process_file(f)['EXIF DateTimeOriginal']))  # alternative try: ['Image DateTime']
        except Exception as e:
            if verbose:
                print(" ... NO EXIF DATA:", index, file)
            continue
        tag = tag.replace("/", ":").replace(":", "").replace(" ", "-")
        if verbose:
            print(" ... Tag:", tag, "File:", file, )
        if tag in file:  # is file names after exif?
            if verbose:
                print("File has EXIF as name", index, file)
            continue
        temp = file.rsplit("/", 1)
        path = temp[0]+"/"  #file path
        extension = temp[1].rsplit(".", 1)[1]  # file extension
        newname = path+tag+"."+extension  # new file name
        #print("out rename:", index, file, newname)
        movefile(file, newname, index)
    print("")



def sort():  # sort renamed pictures into 'year' folders
    print("Start 'Sorting'")
    for index, file in enumerate(filelist):
        print("\rSorting File %d of %d" % (index + 1, len(filelist)), end="");
        if verbose:
            print(file)
        x = file.rsplit("/", 1)[1][:4]
        if not str.isdigit(x):
            continue
        x = int(x)
        if 2000 <= x <= datetime.datetime.now().year:
            y = str(file.rsplit("/", 1)[1])
            try:
                dst = args.root_path+str(x)+"/"+y
            except Exception as e:
                print("sort error", e)
            movefile(file, dst, index)
    print("")


def hashit():
    count = 0
    print("Start 'Picture Hashing'")
    verbose = False
    for index, file in enumerate(filelist):
        print("\rHashing File %d of %d - %d" % (index + 1, len(filelist), len(hashtable)),end="");
        count = count + 1
        if verbose:
            print(file)
        try:
            image = Image.open(file)
        except Exception as e:
            if verbose:
                print(" ... Cannot open image: %s" % file)
            continue
        try:
            row, col = dhash.dhash_row_col(image)
        except Exception as e:
            if verbose:
                print(" ... Cannot open image: %s" % file)
            continue
        pichash = dhash.format_hex(row, col)
        if pichash in hashtable:
            dst = dubdir + file.rsplit("/", 1)[1]
            movefile(file, dst, index)
        else:
            hashtable.update({pichash: file})
    print("")


# move files
# check if dir exists before, and creates dir if not
def movefile(src, dst, index):
    #print("src, dst, ... ", src, dst, index)
    if verbose:
        print("Moving:", index, src)
    if not os.path.isdir(dst.rsplit("/", 1)[0]):
        os.makedirs(dst.rsplit("/", 1)[0])
        if verbose:
            print("+++ Making Dir:", dst.rsplit("/", 1)[0])
    if src == dst:
        return
    if os.path.isfile(dst):
        zearch = dst.rsplit("/", 1)[1]
        zearch = zearch.rsplit(".", 1)[0]
        path = dst.rsplit("/", 1)[0]
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                file = os.path.join(root, filename)
                filelist2.append(file)
        matching = [s for s in filelist2 if zearch in s]
        maxlength = max(len(s) for s in matching)
        longest_strings = [s for s in matching if len(s) == maxlength]
        for x in longest_strings:
            count = 0
            path2 = x.rsplit("/", 1)[0]
            file = x.rsplit("/", 1)[1]
            extension = "."+file.rsplit(".", 1)[1]
            file =  file.rsplit(".", 1)[0]
            try:
                str.isdigit(file.rsplit("_", 1)[1])
                count = file.rsplit("_", 1)[1]
            except Exception as e:
                pass
                count = 0
            templist.append(count)
        if len(templist) != 0:
            templist.sort(reverse=True)
            count = int(templist[0]) + 1
        else:
            count = 0
        try:
            dst = path2 + "/" + file.rsplit("_", 1)[0] + "_" + str(count) + extension
        except:
            dst = path2 + "/" + file + "_" + str(count) + extension
        del templist[:]
        del filelist2[:]
    try:
        shutil.move(src, dst)
    except Exception as e:
        if verbose:
            print(" ... Cannot move file: %s" % dst)
    #print("out move..:", index, src, dst)
    if verbose:
        print("... %s moved" % dst.rsplit("/", 1)[1])
    filelist[index] = dst




def main():  # starts everything up
    print("Starting Cleaning Up Your Pictures\nLooking in %s" % args.root_path)
    filewalk(args.root_path)
    rename()
    sort()
    hashit()


if __name__ == "__main__":
    if args.verbose == "INFO":
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    elif args.verbose == "WARNING":
        logging.basicConfig(format='%(message)s', level=logging.WARNING)
    else:
        logging.basicConfig(format='%(message)s', level=logging.CRITICAL)

    # Ensure that paths end with /
    if not args.root_path[len(args.root_path)-1:] == "/":
        args.root_path = args.root_path+"/"
    dubdir = args.root_path + "Duplicates/"
    if not dubdir[len(dubdir)-1:] == "/":
        dubdir = dubdir + "/"



starttime = time()
main()
endtime = time()
print('Completed in %f secs' % (endtime - starttime))



