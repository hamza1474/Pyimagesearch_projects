import cv2
import imutils

image = cv2.imread("jp.png")
(h, w, d) = image.shape
print("width={}, height={}, depth={}".format(w, h,  d))

cv2.imshow("Image", image)
cv2.waitKey(0)

(b, g ,r) = image[100, 50]
print("B {} G {} R {} ".format(b,g,r))

roi = image[25:110, 30:400]
cv2.imshow("ROI", roi)
cv2.waitKey(0)

resized = cv2.resize(image, (200, 200))
cv2.imshow("Fixed Resizing", resized)
cv2.waitKey(0)

dim = (int(w*1.5), int(h*1.5))
asp = cv2.resize(image, dim)
cv2.imshow("resized", asp)
cv2.waitKey(0)

imresize = imutils.resize(image, width=300)
cv2.imshow("imresize", imresize)
cv2.waitKey(0)

center = (w//2, h//2)
M = cv2.getRotationMatrix2D(center, -45, 1)
rotated = cv2.warpAffine(image, M, (w, h))
cv2.imshow("rotated", rotated)
cv2.waitKey(0)

rotated = imutils.rotate_bound(image, -80)  #rotate will clip, rotate_bound will display full
cv2.imshow("rotated", rotated)
cv2.waitKey(0)

blurred = cv2.GaussianBlur(image, (11, 11), -10)
cv2.imshow("Blurred", blurred)
cv2.waitKey(0)

output = image.copy()
cv2.rectangle(output, (320, 60), (420, 160), (0, 0, 255), 2)
cv2.imshow("Rectangle", output)
cv2.waitKey(0)

output = image.copy()
cv2.putText(output, "Hello World", (10,25), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.0, (0,255,0))
cv2.imshow("texted", output)
cv2.waitKey(0)
