import cv2
import numpy as np

img = cv2.imread("scribbles.png")
gray_scale_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur_img = cv2.GaussianBlur(gray_scale_img, (3,3), 1,1)
ret, black_white_thresholded_img = cv2.threshold(blur_img, 1, 255, cv2.THRESH_BINARY)

#bobby_img = cv2.imread("bobbyhill.jpg")
#house_img = cv2.resize(house_img, (25,25))
#gray_bobby = cv2.cvtColor(bobby_img, cv2.COLOR_BGR2GRAY)
#ret, threshold_house = cv2.threshold(gray_bobby, 1, 255, cv2.THRESH_BINARY)
#edge_house = cv2.Canny(threshold_house, 0.1, 0.3)

#pyramid_img = black_white_thresholded_img.copy()
##width = threshold_house.shape[0]
#height = threshold_house.shape[1]
#for i in range(0, 5):
#res = cv2.matchTemplate(blur_img, gray_bobby, cv2.TM_CCOEFF_NORMED)
#location = np.where(res >= 0.70)

templates = ["bobby", "burns", "gus"]

for template in templates:
    temp_img = cv2.imread(template+".png")
    #house_img = cv2.resize(house_img, (25,25))
    gray_temp = cv2.cvtColor(temp_img, cv2.COLOR_BGR2GRAY)
    #ret, threshold_temp = cv2.threshold(gray_bobby, 1, 255, cv2.THRESH_BINARY)
    res = cv2.matchTemplate(blur_img, gray_temp, cv2.TM_CCOEFF_NORMED)
    location = np.where(res >= 0.90)

    for point in zip(*location[::-1]):
        cv2.rectangle(img,point, (point[0]+100, point[1]+100), (0,255,255), 1)
        cv2.putText(img, template, (point[0]+50, point[1]+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))

#print(res)
#min_val,max_val, min_loc, max_loc = cv2.minMaxLoc(res)

#top_left = min_loc
#bottom_right = (top_left[0] + 100, top_left[1] + 100)
#cv2.rectangle(img,top_left, bottom_right, 255, 2)
#cv2.imwrite("pyramid"+str(i)+".png", threshold_house)
#threshold_house = cv2.pyrDown(pyramid_img)

#cv2.imshow("House", edge_house)


#sailboat_template = cv2.imread("sailboat_template.png")
#gray_sail = cv2.cvtColor(sailboat_template, cv2.COLOR_BGR2GRAY)
#blur_sail = cv2.GaussianBlur(gray_sail, (3,3), 1,1)
#edges = cv2.Canny(blur_sail, 50, 200)
#cv2.imshow("edges", edges)

contours, hierarchy = cv2.findContours(black_white_thresholded_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

circles = cv2.HoughCircles(blur_img, cv2.HOUGH_GRADIENT, 1, 100,  param1=100, param2=40, minRadius=1, maxRadius=200)
#circles = cv2.HoughCircles(black_white_thresholded_img, cv2.HOUGH_GRADIENT, 1, 100,  param1=100, param2=30, minRadius=1, maxRadius=200)
#circles = cv2.HoughCircles(black_white_thresholded_img, cv2.HOUGH_GRADIENT, 1, black_white_thresholded_img.shape[0]/8, param1=100, param2=30, minRadius=1, maxRadius=200)

for contour in contours:
    approx_curve = cv2.approxPolyDP(contour, 3, True)
    #cv2.drawContours(img, approx_curve, 0, (0,255,0), 3)

    if len(approx_curve) == 3:
        rect = cv2.boundingRect(approx_curve)
        cv2.rectangle(img, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 255, 255), 3)
        cv2.putText(img, "Triangle", (rect[0]+(rect[2]//2), rect[1]+(rect[3]//2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))

    
    #elif len(approx_curve) == 5:
    #    rect = cv2.boundingRect(approx_curve)
    #    cv2.rectangle(img, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 255, 255), 3)
    #    cv2.putText(img, "House", (rect[0]+(rect[2]//2), rect[1]+(rect[3]//2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))

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

if circles is not None:
    circles = np.round(circles[0,:]).astype("int")
    for i in range(0, len(circles)):
        center_x = circles[i][0]
        center_y = circles[i][1]
        radius = circles[i][2]  
        cv2.rectangle(img, (center_x-radius-5, center_y-radius-5), (center_x+radius+5, center_y+radius+5), (0,255,255), 3) 
        #cv2.rectangle(img, (center_x-radius-5, center_y-radius-5), (center_x+radius+5, center_y+radius+5), (0,255,255), 3)  
        #cv2.circle(img, (circles[i][0], circles[i][1]), circles[i][2], (0,255,255), 3)  
        cv2.putText(img, "Circle",(circles[i][0], circles[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255))  


while(True):
    cv2.imshow("Blackboard Window", img)
    key_press = cv2.waitKey(1)
    if key_press == 27:
        cv2.destroyAllWindows()
        break
