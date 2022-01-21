# dependencies
# requires python3.x
# pip install pillow
#
# this script looks at all the images in the jekyll/assets/img folder and
# collects the resolution and file size of all images.
# it then spits out a images.csv file that can be uploaded to google drive.

import os
import glob
from pathlib import Path
from PIL import Image # run `pip install pillow` to get this lib.
import enum
import csv


img_path = "../jekyll/assets/img/**/*"
imgs = glob.glob(img_path)
Images = []
failed_images = []

## -- utils for converting size type

# Enum for size units
class SIZE_UNIT(enum.Enum):
   BYTES = 1
   KB = 2
   MB = 3
   GB = 4

def convert_unit(size_in_bytes, unit):
   """ Convert the size from bytes to other units like KB, MB or GB"""
   if unit == SIZE_UNIT.KB:
       return size_in_bytes/1024
   elif unit == SIZE_UNIT.MB:
       return size_in_bytes/(1024*1024)
   elif unit == SIZE_UNIT.GB:
       return size_in_bytes/(1024*1024*1024)
   else:
       return size_in_bytes

# --

def make_img_dict(imgPath, Img):
    f = {
        "path": imgPath,
        "width": Img.width,
        "height": Img.height,
        "PIL_Image": Img,
        "size":   os.stat(imgPath).st_size
    }
    return f

def get_img_data():
    for img in imgs:
        isFile = os.path.isfile(img)
        isImg = img.endswith(".jpg") or img.endswith(".png")
        if isFile and isImg :
            try:
                x = Image.open(img)
                img_dict = make_img_dict(img, x)
                Images.append(img_dict)
            except:
                failed_images.append(img)


def print_report():
    print("\nThe following images from ../jekyll/assets/img/ are soted by size.\n")
    print ("{:<60} | {:<7} | {:<7} | {:<7}".format('File', 'width', 'height', "size"))
    print ("-----------------------------------------------------------------------------------------------------------------")

    Images.sort(key = lambda i: (i['width']))
    Images.reverse()
    for idx, img in enumerate(Images):
        path = img["path"].split("../jekyll/assets/img/")[1]
        imgSize = convert_unit(img["size"], SIZE_UNIT.MB)
        print ("{:<60} | {:<7} | {:<7} | {:<7}".format(path,  img["width"], img["height"], imgSize))


def resize_image():
   """If image is larger than img_size, resize it to img_size"""
   for idx, img in enumerate(Images):
      # If you want to resize images and keep their aspect ratios, then you
      # should instead use the thumbnail() function to resize them. This also
      # takes a two-integer tuple argument representing the maximum width and
      # maximum height of the thumbnail.
      if img["width"] > 1920 or img["height"] > 1920:
         img["PIL_Image"].thumbnail((1920, 1920))
         # if it's a png, use compress_level,
         # print(img["path"])
         # os.system(f"convert {img['path']} -resize 1920 {img['path']}")
         # img["PIL_Image"].save(img["path"], optimize=True)
         # otherwise, if it's jpeg, set quality to ...n?

def write_csv():
    keys = Images[0].keys()
    with open('images.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(Images)


get_img_data()
# print_report()
# write_csv()
resize_image()
