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
#parser.add_argument('root_path', type=str, action="store", help="Path to folder to scan")
parser.add_argument('-t', '--test', dest='testing', action='store_true', help="Testing Mode")
parser.add_argument('-vvv', action="store_const", dest="verbose", const='INFO')
parser.set_defaults(testing=True)

#parser.set_defaults(root_path="/Users/lallepot/Desktop/testing/test/")
parser.set_defaults(root_path="/Users/lallepot/Desktop/Pictures/")

parser.set_defaults(verbose="")


args = parser.parse_args()

dubdir = args.root_path + "Duplicates/"
filelist = []
exifData = ""
verbose = ""
hashlist = []
hashtable = {}
filetable = []



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
        if verbose:
            print(index, file)
        try:
            f = open(file, 'rb')
        except Exception as e:
            print(e, index, file)

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
        if os.path.isfile(newname):  # file already exists?
            newname = path+tag+"_1."+extension
        try:
            os.rename(file, newname)
        except Exception as e:
            print(e)
        filelist[index] = newname
    print("")



def sort():  # sort renamed pictures into 'year' folders
    print("Start 'Sorting'")
    for index, file in enumerate(filelist):
        print("\rSorting File %d of %d" % (index + 1, len(filelist)), end="");
        if verbose:
            print(file)
        x = file.rsplit("/", 1)[1][:4]
#        print(x)
        if not str.isdigit(x):
#            print("no match")
            continue
        x = int(x)
        if 2000 <= x <= datetime.datetime.now().year:
            y = str(file.rsplit("/", 1)[1])
            try:
                dst = args.root_path+str(x)+"/"+y
            except Exception as e:
                print(e)
            movefile(file, dst, index)
    print("")


def hashit():
    temp = []
    count = 0
    global verbose
    if verbose:
        print("Start 'Picture Hashing'")
    for index, file in enumerate(filelist):
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
        #if verbose:
        #    print(index, pichash)
        if not hashtable.pop(pichash, 0):
            hashtable.update({pichash: file})
        else:
            dst = dubdir + file.rsplit("/", 1)[1]
            movefile(file, dst, index)



# move files
# check if dir exists before, and creates dir if not
def movefile(src, dst, index):
    if verbose:
        print("Moving:", index, src)
    if not os.path.isdir(dst.rsplit("/", 1)[0]):
        os.makedirs(dst.rsplit("/", 1)[0])
        if verbose:
            print("+++ Making Dir:", dst.rsplit("/", 1)[0])
    if src == dst:
        return
    if os.path.isfile(dst):
        path = dst.rsplit("/", 1)[0]
        temp = dst.rsplit("/", 1)[1]
        name = temp.rsplit(".", 1)[0]
        extension = temp.rsplit(".", 1)[1]
        dst = path + "/" + name + "_1." + extension
        if os.path.isfile(dst):
            dst = path + "/" + name + "_1_random_" + str(randint(1000,9999)) + "." + extension
            if os.path.isfile(dst):
                print("true")
                dst = dst.rsplit(".", 1)[0] + str(randint(1000,9999)) + "." + extension
    try:
        shutil.move(src, dst)
    except Exception as e:
        if verbose:
            print(" ... Cannot move file: %s" % dst)
    if verbose:
        print("... %s moved" % dst.rsplit("/", 1)[1])
    filelist[index] = dst




def main():  # starts everything up
    print("Starting Cleaning up Your Pictures\nLooking in %s" % args.root_path)
    filewalk(args.root_path)
    rename()
    sort()
    hashit()


def check_paths():
    print()

if __name__ == "__main__":
    if args.verbose == "INFO":
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    elif args.verbose == "WARNING":
        logging.basicConfig(format='%(message)s', level=logging.WARNING)
    else:
        logging.basicConfig(format='%(message)s', level=logging.CRITICAL)

    if args.testing:
        args.root_path = "/Users/lallepot/Desktop/testing/test/"

    # Ensure that paths end with /
    if not args.root_path[len(args.root_path)-1:] == "/":
        args.root_path = args.root_path+"/"
    if not dubdir[len(dubdir)-1:] == "/":
        dubdir = dubdir + "/"



starttime = time()
main()
endtime = time()
print('Completed in %f secs' % (endtime - starttime))

