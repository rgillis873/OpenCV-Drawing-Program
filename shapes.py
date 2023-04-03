import cv2
import numpy as np

img = cv2.imread("triangles.png")
gray_scale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur_img = cv2.GaussianBlur(gray_scale_img, (3,3), 1,1)
ret, black_white_thresholded_img = cv2.threshold(blur_img, 1, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(black_white_thresholded_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#contours_img = cv2.drawContours(black_white_thresholded_img, contours, -1, (0,255,0), 3)

#i = 0
for contour in contours:
    #if i == 0:
    #    continue

    #i = 1
    #epsilon =  0.1*cv2.arcLength(contour, True)
    approx_curve = cv2.approxPolyDP(contour, 3, True)
    cv2.drawContours(img, approx_curve, 0, (0,255,0), 3)
    #rect = cv2.boundingRect(contour)
    #print(rect)
    #cv2.rectangle(img, (rect[0], rect[1]), (rect[2], rect[3]), (0, 120, 120), 3)

    print(len(approx_curve))


    if len(approx_curve) == 3:
        rect = cv2.boundingRect(contour)
        cv2.rectangle(img, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 255, 255), 3)
        cv2.putText(img, "Triangle", (rect[0]+(rect[2]//2), rect[1]+(rect[3]//2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))

#print(contours)

while(True):
    cv2.imshow("Blackboard Window", img)
    key_press = cv2.waitKey(1)
    if key_press == 27:
        cv2.destroyAllWindows()
        break
