# ascii-picgen.py
# Generate ASCII picture from your own picture!

import cv2
import numpy as np
import argparse
import math

MAX_WIDTH = 500
#ASCII_CHOICE = '%&#$]/|;:,. '
ASCII_CHOICE = '%&$/:. '
OUTFILE = 'pic-gen.txt'

NO_OF_BINS = math.ceil(256/len(ASCII_CHOICE))
print('NO_OF_BINS: %d'%NO_OF_BINS)
print('ASCII_CHOICE: %s'%ASCII_CHOICE)

parser = argparse.ArgumentParser()
parser.add_argument("file", help='File to be converted.')

args = parser.parse_args()


img = cv2.imread(args.file)

if img is None:
    sys.exit("Invalid image.")

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(img.shape)

img2 = img.copy()
while True:
    img2= cv2.pyrDown(img2)
    if img2.shape[1] <= MAX_WIDTH/2:
        break

img2 = cv2.filter2D(img2, -1, np.array([
    [ 0, -1 , 0 ],
    [ -1, 5, -1 ],
    [ 0, -1, 0 ],
]))

with open(OUTFILE, 'w+') as f:
    for row in img2:
        for elem in row:
            elem = 256*pow(elem/256, 0.75)
            buf = ASCII_CHOICE[int(elem/NO_OF_BINS)]
            f.write(buf + buf)
        f.write('\n')

f.close()

cv2.imshow("Original", img)
cv2.imshow("Downsampled", img2)
k = cv2.waitKey(0)



