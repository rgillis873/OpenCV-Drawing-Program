import cv2
import numpy as np

img = cv2.imread("scribbles.png")
img2 = cv2.imread("house.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

orb = cv2.ORB_create()

kp1, dest1 = orb.detectAndCompute(img, None)

kp2, dest2 = orb.detectAndCompute(img2, None)

matcher = cv2.BFMatcher()
matches = matcher.match(dest1, dest2)

final_img = cv2.drawMatches(img, kp1, img2, kp2, matches[:20], None)

kp1img = cv2.drawKeypoints(img, kp1, None)
kp2img = cv2.drawKeypoints(img2, kp2, None)

cv2.imshow("IMG1", kp1img)
cv2.imshow("IMG2", kp2img)
cv2.imshow("Matches", final_img)
cv2.waitKey(0)
cv2.destroyAllWindows()