import cv2
import numpy as np

img = cv2.imread("draw2.png")
gray_scale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur_img = cv2.GaussianBlur(gray_scale_img, (3,3), 1,1)
ret, black_white_thresholded_img = cv2.threshold(blur_img, 1, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(black_white_thresholded_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

circles = cv2.HoughCircles(black_white_thresholded_img, cv2.HOUGH_GRADIENT, 1, black_white_thresholded_img.shape[0]/8, param1=100, param2=30, minRadius=1, maxRadius=100)

for contour in contours:
    approx_curve = cv2.approxPolyDP(contour, 3, True)
    cv2.drawContours(img, approx_curve, 0, (0,255,0), 3)

    if len(approx_curve) == 3:
        rect = cv2.boundingRect(approx_curve)
        cv2.rectangle(img, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 255, 255), 3)
        cv2.putText(img, "Triangle", (rect[0]+(rect[2]//2), rect[1]+(rect[3]//2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))

    
    elif len(approx_curve) == 5:
        rect = cv2.boundingRect(approx_curve)
        cv2.rectangle(img, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 255, 255), 3)
        cv2.putText(img, "House", (rect[0]+(rect[2]//2), rect[1]+(rect[3]//2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))

    #elif len(approx_curve) == 4:
    #    rect = cv2.boundingRect(contour)
    #    width = rect[2]
        #height = rect[3]
        #difference = width - height
        #cv2.rectangle(img, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 255, 255), 3)
        #if difference > 5:
        #    cv2.putText(img, "Rectangle", (rect[0]+(rect[2]//2), rect[1]+(rect[3]//2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))
        #else:
            #cv2.putText(img, "Square", (rect[0]+(rect[2]//2), rect[1]+(rect[3]//2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))



while(True):
    cv2.imshow("Blackboard Window", img)
    key_press = cv2.waitKey(1)
    if key_press == 27:
        cv2.destroyAllWindows()
        break
