from panorama import Stitcher
import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", required=True,
    help="path to first image")
ap.add_argument("-s", "--second", required=True,
help="path to second image")
args = vars(ap.parse_args())

# load the two images and resize them with
# same width 
width = 400
imageA = cv2.imread(args["first"])
imageB = cv2.imread(args["second"])
imageA  = imutils.resize(imageA, width=width)
imageB = imutils.resize(imageB, width=width)

# stitch the images together to create panorama
stitcher = Stitcher()
(result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)

# show the image
cv2.imshow("Image A", imageA)
cv2.imshow("Image B", imageB)
cv2.imshow("Mathces", vis)
cv2.imshow("panorama", result)
cv2.waitKey(0)

cv2.destroyAllWindows()