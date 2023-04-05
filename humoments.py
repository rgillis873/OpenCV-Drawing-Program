import cv2
import numpy as np

img = cv2.imread("draw2.png")
gray_scale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur_img = cv2.GaussianBlur(gray_scale_img, (3,3), 1,1)
ret1, thresholded_img = cv2.threshold(blur_img, 1, 255, cv2.THRESH_BINARY)
edges_img = cv2.Canny(thresholded_img, 0.1, 0.3)
contours, _ = cv2.findContours(edges_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#contours_img = cv2.drawContours(img, contours, -1, (0,255,255), 3)

for contour in contours:
    approx_curve = cv2.approxPolyDP(contour,  0.1*cv2.arcLength(contour,True), True)

    if(len(approx_curve >= 5)):
        contours_img = cv2.drawContours(img, contour, 0, (0,255,255), 3)

house_img = cv2.imread("house.png")
gray_house_img = cv2.cvtColor(house_img, cv2.COLOR_BGR2GRAY)
blur_house = cv2.GaussianBlur(gray_house_img, (3,3), 1,1)
ret2, thresholded_house = cv2.threshold(blur_house, 1, 255, cv2.THRESH_BINARY)
edges_house = cv2.Canny(thresholded_house, 0.1, 0.3)

cv2.imshow("IMG1", edges_img)
cv2.imshow("House", edges_house)
cv2.imshow("c_IMG1", contours_img)
cv2.waitKey(0)
cv2.destroyAllWindows()