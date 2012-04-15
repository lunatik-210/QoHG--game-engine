import Image
import sys

if len(sys.argv) != 2:
    print 'Enter file name'

file_name = sys.argv[1]

img = Image.open(file_name)

new_file_name = file_name[:file_name.find('.')]

sizes = [64, 48, 32]
images = []

for size in sizes:
    new_img = img.resize((size,size))
    new_img.save(new_file_name + "__%d" % size + ".png")



