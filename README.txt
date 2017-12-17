ImageOrganizer (ImageOrganizer.py)

ImageOrganizer recursively scans a target folder for images, and

1) renaming pictures with the creation date and time from the exif data
2) moves pictures based on their file name into new folders (20010101-012342.jpg is moved into a folder named '2001')
3) moves duplicate pictures into a folder named 'Duplicates' in the root of the target folder.

ImageOrganizer is written for Python3.7

Usage: ./ImageOrganizer.py [target path]

