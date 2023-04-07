import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Variables for video capture and hand detection. Detect only one hand
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands = 1, detectionCon=0.8)
img = cap.read()

# Create blackboard image
img2 = np.zeros((500, 675, 3), np.uint8)

# Read in images used for stickers
bobby_sticker = cv2.imread("bobby.png")
burns_sticker = cv2.imread("burns.png")
gus_sticker = cv2.imread("gus.png")

# Variables to store drawing thickness
thickness = 3
thickness_change = 1
colour = (0,0,255)

# Variables for determining program mode. There are three modes: drawing, erasing and shape detection
mode = "draw"
mode_num = 0
modes = ["draw", "erase", "shapes"]

# Variable for storing the current drawing mode. There are six drawing modes: line, rectangle, circle, Bobby Hill sticker,
# Mr. Burns sticker and Gus Griswald sticker
draw_mode = "line"

# Variables for storing the start and end points in drawing
start_line = (0,0)
end_line = (10,10)

# Variables used for determing which type of shape/sticker is being used for drawing
drawing_line = False
drawing_rectangle = False
drawing_circle = False
drawing_bobby = False
drawing_burns = False
drawing_gus = False


circle_radius = 1
erase_button_counter = 1
not_drawing = 1
displayed_detected = False

# Variable used to store blackboard image when mode is switched to shape detection. This is used 
# so that bounding boxes for shapes and stickers are not kept on the blackboard image.
old_img2 = None

# Store colours options for different onscreen buttons
red_colours = [(0,0,255), (0,0,125)]
green_colours = [(0,255,0), (0,125,0)]
blue_colours = [(255,217,4), (125,110,2)]

shape_button_colours = [(20,200,200),(150,150,150)]

mode_button_colours = [(20,200,200),(150,150,150)]

# Variables used to store which button is currently selected. If the value is 0, that button is selected
# otherwise the value is 1

# Colour selections are grouped together
red_selection = 0
green_selection = 1
blue_selection = 1

# Drawing mode buttons are grouped together
line_selection = 0
rectangle_selection = 1
circle_selection = 1
bobby_selection = 1
burns_selection = 1
gus_selection = 1

# Mode buttons are grouped together
draw_selection = 0
erase_selection = 1
shape_selection = 1


# Function displays the line, rectangle and circle buttons on the screen
def display_shape_buttons():
    line = cv2.rectangle(img, (0,0), (100,90), shape_button_colours[line_selection], cv2.FILLED)
    rectangle = cv2.rectangle(img, (115,0), (215,90), shape_button_colours[rectangle_selection], cv2.FILLED)
    circle = cv2.rectangle(img, (230,0), (330,90), shape_button_colours[circle_selection], cv2.FILLED)
    cv2.putText(line, "Line", (15, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(rectangle, "Rect", (130, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(circle, "Circle", (240, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))

# Function displays the red, green and blue buttons on the screen
def display_colour_buttons():
    red = cv2.rectangle(img, (345,0), (445,90), red_colours[red_selection], cv2.FILLED)
    green = cv2.rectangle(img, (460,0), (560,90), green_colours[green_selection], cv2.FILLED)
    blue = cv2.rectangle(img, (575,0), (675,90), blue_colours[blue_selection], cv2.FILLED)
    cv2.putText(red, "Red", (360, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(green, "Green", (460, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(blue, "Blue", (585, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))

# Function displays the increase and decrease drawing line thickness buttons on the screen
def display_thickness_buttons():
    increase = cv2.rectangle(img, (690,0), (790,90), (150,150,150), cv2.FILLED)
    decrease = cv2.rectangle(img, (690,105), (790,195), (150,150,150), cv2.FILLED)
    cv2.putText(increase, "+", (725, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(increase, str(thickness), (727, 67), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(decrease, "-", (725, 145), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(decrease, str(thickness), (727, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))

# Function displays the draw, erase and shape detection mode buttons on the screen 
def display_mode_buttons():
    draw = cv2.rectangle(img, (690,210), (790,300), mode_button_colours[draw_selection], cv2.FILLED)
    erase = cv2.rectangle(img, (690,315), (790,405), mode_button_colours[erase_selection], cv2.FILLED)
    shapes = cv2.rectangle(img, (690,420), (790,510), mode_button_colours[shape_selection], cv2.FILLED)
    cv2.putText(draw, "Draw", (700, 260), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(erase, "Erase", (697, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(shapes, "Shape", (695, 465), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))

# Function draws the border for the drawing area on the screen   
def display_border_for_drawing_area():
    cv2.line(img, (0, 100), (675, 100), (0,0,0),4)
    cv2.line(img, (675, 100), (675, 600), (0,0,0),4)

# Function displays the 3 sticker button types on the screen
def display_sticker_buttons():
    bobby = cv2.rectangle(img, (800,0), (890,90), shape_button_colours[bobby_selection], cv2.FILLED)
    burns = cv2.rectangle(img, (800,105), (890,195), shape_button_colours[burns_selection], cv2.FILLED)
    gus = cv2.rectangle(img, (800,210), (890,300), shape_button_colours[gus_selection], cv2.FILLED)
    cv2.putText(bobby, "Bobby", (800, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(burns, "Burns", (800, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(gus, "Gus", (810, 255), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))   

# Function determines if the draw line button was pressed
# parameter hand position stores the x,y coordinates of the hand detected on the screen
def pressed_line_button(hand_position):
    global line_selection
    global rectangle_selection
    global circle_selection
    global bobby_selection
    global burns_selection
    global gus_selection

    # If button was pressed, change its colour to highlighted
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    if(x >= 0 and x <= 100 ) and (y >= 0 and y <= 90) and mode == "draw":
        pressed = True
        line_selection = 0
        rectangle_selection = 1
        circle_selection = 1
        bobby_selection = 1
        burns_selection = 1
        gus_selection = 1
    return pressed

# Function determines if the draw rectangle button was pressed
# parameter hand position stores the x,y coordinates of the hand detected on the screen
def pressed_rectangle_button(hand_position):
    global line_selection
    global rectangle_selection
    global circle_selection
    global bobby_selection
    global burns_selection
    global gus_selection

    
    # If button was pressed, change its colour to highlighted
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    if(x >= 115 and x <= 215 ) and (y >= 0 and y <= 90) and mode == "draw":
        pressed = True
        line_selection = 1
        rectangle_selection = 0
        circle_selection = 1
        bobby_selection = 1
        burns_selection = 1
        gus_selection = 1
    return pressed

# Function determines if the draw circle button was pressed
# parameter hand position stores the x,y coordinates of the hand detected on the screen
def pressed_circle_button(hand_position):
    global line_selection
    global rectangle_selection
    global circle_selection
    global bobby_selection
    global burns_selection
    global gus_selection

    # If button was pressed, change its colour to highlighted
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    if(x >= 230 and x <= 330) and (y >= 0 and y <= 90) and mode == "draw":
        pressed = True
        line_selection = 1
        rectangle_selection = 1
        circle_selection = 0
        bobby_selection = 1
        burns_selection = 1
        gus_selection = 1
    return pressed


# Function determines if the draw Bobby Hill sticker button was pressed
# parameter hand position stores the x,y coordinates of the hand detected on the screen
def pressed_bobby_button(hand_position):
    global line_selection
    global rectangle_selection
    global circle_selection
    global bobby_selection
    global burns_selection
    global gus_selection
    
    # If button was pressed, change its colour to highlighted
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    if(x >= 800 and x <= 890 ) and (y >= 0 and y <= 90) and mode == "draw":
        pressed = True
        line_selection = 1
        rectangle_selection = 1
        circle_selection = 1
        bobby_selection = 0
        burns_selection = 1
        gus_selection = 1
    return pressed


# Function determines if the draw Mr. Burns sticker button was pressed
# parameter hand position stores the x,y coordinates of the hand detected on the screen
def pressed_burns_button(hand_position):
    global line_selection
    global rectangle_selection
    global circle_selection
    global bobby_selection
    global burns_selection
    global gus_selection

    # If button was pressed, change its colour to highlighted
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    if(x >= 800 and x <= 890 ) and (y >= 105 and y <= 195) and mode == "draw":
        pressed = True
        line_selection = 1
        rectangle_selection = 1
        circle_selection = 1
        bobby_selection = 1
        burns_selection = 0
        gus_selection = 1
    return pressed

# Function determines if the draw Gus Griswald sticker button was pressed
# parameter hand position stores the x,y coordinates of the hand detected on the screen
def pressed_gus_button(hand_position):
    global line_selection
    global rectangle_selection
    global circle_selection
    global bobby_selection
    global burns_selection
    global gus_selection

    # If button was pressed, change its colour to highlighted
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    if(x >= 800 and x <= 890) and (y >= 210 and y <= 300) and mode == "draw":
        pressed = True
        line_selection = 1
        rectangle_selection = 1
        circle_selection = 1
        bobby_selection = 1
        burns_selection = 1
        gus_selection = 0
    return pressed

# Function determines if the red colour button was pressed
# parameter hand position stores the x,y coordinates of the hand detected on the screen
def pressed_red_button(hand_position):
    global red_selection
    global green_selection
    global blue_selection

    
    # If button was pressed, change its colour to highlighted
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    if(x >= 345 and x <= 445 ) and (y >= 0 and y <= 90) and mode == "draw":
        pressed = True
        red_selection = 0
        green_selection = 1
        blue_selection = 1
    return pressed

# Function determines if the green colour button was pressed
# parameter hand position stores the x,y coordinates of the hand detected on the screen
def pressed_green_button(hand_position):
    global red_selection
    global green_selection
    global blue_selection

    # If button was pressed, change its colour to highlighted
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    if(x >= 460 and x <= 560 ) and (y >= 0 and y <= 90) and mode == "draw":
        pressed = True
        red_selection = 1
        green_selection = 0
        blue_selection = 1
    return pressed

# Function determines if the blue colour button was pressed
# parameter hand position stores the x,y coordinates of the hand detected on the screen
def pressed_blue_button(hand_position):
    global red_selection
    global green_selection
    global blue_selection

    # If button was pressed, change its colour to highlighted
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    if(x >= 575 and x <= 675 ) and (y >= 0 and y <= 90) and mode == "draw":
        pressed = True
        red_selection = 1
        green_selection = 1
        blue_selection = 0
    return pressed


# Function determines if the increase thickness button was pressed
# parameter hand position stores the x,y coordinates of the hand detected on the screen
def pressed_increase_button(hand_position):
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    
    if(x >= 690 and x <= 790 ) and (y >= 0 and y <= 90) and mode == "draw":
        pressed = True
    return pressed

# Function determines if the decrease thickness button was pressed
# parameter hand position stores the x,y coordinates of the hand detected on the screen
def pressed_decrease_button(hand_position):
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    
    if(x >= 690 and x <= 790 ) and (y >= 105 and y <= 195) and mode == "draw":
        pressed = True
    return pressed

# Function determines if the drawing mode button was pressed
# parameter hand position stores the x,y coordinates of the hand detected on the screen
def pressed_draw_button(hand_position):
    global draw_selection
    global erase_selection
    global shape_selection

    # If button was pressed, change its colour to highlighted
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    if(x >= 690 and x <= 790 ) and (y >= 210 and y <= 300):
        pressed = True
        draw_selection = 0
        erase_selection = 1
        shape_selection = 1
    return pressed

# Function determines if the erasing mode button was pressed
# parameter hand position stores the x,y coordinates of the hand detected on the screen
def pressed_erase_button(hand_position):
    global draw_selection
    global erase_selection
    global shape_selection

    # If button was pressed, change its colour to highlighted
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    if(x >= 690 and x <= 790 ) and (y >= 315 and y <= 405):
        pressed = True
        draw_selection = 1
        erase_selection = 0
        shape_selection = 1
    return pressed

# Function determines if the erasing mode button was pressed
# parameter hand position stores the x,y coordinates of the hand detected on the screen 
def pressed_shape_detection_button(hand_position):
    global draw_selection
    global erase_selection
    global shape_selection

    # If button was pressed, change its colour to highlighted
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    if(x >= 690 and x <= 790 ) and (y >= 420 and y <= 510):
        pressed = True
        draw_selection = 1
        erase_selection = 1
        shape_selection = 0
    return pressed

# Function erases a 100x100 block on the drawing board turning it back to black
# parameter hand position stores the x,y coordinates of the hand detected on the screen 
def erase_screen(hand_position):
    x, y = hand_position[0]['lmList'][4][:2]
    
    # Only erase inside the drawing area boundary
    if(x >= 0 and x <= 675) and (y >= 100 and y <= 600):
        cv2.rectangle(img2, (x,y-100), (x+100,y), (0,0,0), cv2.FILLED)

# Function determines if the hand detected on screen is in the drawing position.
# Drawing position is with the thumb and index finger pressed together
# parameter hand position stores the x,y coordinates of the hand detected on the screen 
def hand_in_drawing_position(hand_position):
    global img
    in_position = False

    # Determine the distance between the thumb and index finger
    lmList = hand_position[0]['lmList']
    length, _, img = detector.findDistance(lmList[4][:2], lmList[8][:2], img)
        
    # If the distance is less than or equal to 20, the hand is in drawing position
    if length <= 20:
        in_position = True
    return in_position

# Function determines if the detected hand is currently in the bounded drawing area.
# Returns true if it is, false otherwise
# parameter hand position stores the x,y coordinates of the hand detected on the screen 
def hand_in_drawing_area(hand_position):
    in_drawing_area = False

    # Determine position of index finger and see if it is in the drawing area
    x, y = hand_position[0]['lmList'][8][:2]
    if(x >= 0 and x < 675) and (y > 100 and y <= 600):
        in_drawing_area = True
    return in_drawing_area

#def hand_in_button_area(hand_position):
#    in_button_area = False
#    x, y = hand_position[0]['lmList'][8][:2]
#    if ((x >= 0 and x <= 600) and (y >= 0 and y <= 80)) or ((x >= 540 and x <= 650) and (y >= 0 and y <= 600)):
#        in_button_area = True
#    return in_button_area

#def detect_triangle(drawing_img):


    
def detect_shapes(drawing_img):
    detection_img = drawing_img.copy()
    gray_scale_img = cv2.cvtColor(detection_img, cv2.COLOR_BGR2GRAY)
    blur_img = cv2.GaussianBlur(gray_scale_img, (3,3), 1,1)
    _, black_white_thresholded_img = cv2.threshold(blur_img, 1, 255, cv2.THRESH_BINARY)

    detection_img = detect_triangles(detection_img, black_white_thresholded_img)
    detection_img = detect_circles(detection_img, blur_img)
    detection_img = detect_stickers(detection_img)

    return detection_img

    #contours, hierarchy = cv2.findContours(black_white_thresholded_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #circles = cv2.HoughCircles(blur_img, cv2.HOUGH_GRADIENT, 1, 100,  param1=100, param2=40, minRadius=1, maxRadius=200)
    #circles = cv2.HoughCircles(blur_img, cv2.HOUGH_GRADIENT, 1, 100,  param1=100, param2=30, minRadius=1, maxRadius=200)

    #for contour in contours:
    #    approx_curve = cv2.approxPolyDP(contour, 3, True)
        #cv2.drawContours(detection_img, approx_curve, 0, (0,255,0), 3)

    #    if len(approx_curve) == 3:
    #        rect = cv2.boundingRect(contour)
    #        cv2.rectangle(detection_img, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 255, 255), 3)
    #        cv2.putText(detection_img, "Triangle", (rect[0]+(rect[2]//2), rect[1]+(rect[3]//2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))

    #if circles is not None:
    #    circles = np.round(circles[0,:]).astype("int")
    #    for i in range(0, len(circles)):
    #        center_x = circles[i][0]
    #        center_y = circles[i][1]
    #        radius = circles[i][2]  
    #        cv2.rectangle(detection_img, (center_x-radius-5, center_y-radius-5), (center_x+radius+5, center_y+radius+5), (0,255,255), 3) 
    #        cv2.putText(detection_img, "Circle",(circles[i][0], circles[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255))  
    #return detection_img

def detect_circles(detection_img, blur_img):
    updated_img = detection_img.copy()

    circles = cv2.HoughCircles(blur_img, cv2.HOUGH_GRADIENT, 1, 100,  param1=100, param2=40, minRadius=1, maxRadius=200)
    if circles is not None:
        circles = np.round(circles[0,:]).astype("int")
        for i in range(0, len(circles)):
            center_x = circles[i][0]
            center_y = circles[i][1]
            radius = circles[i][2]  
            cv2.rectangle(updated_img, (center_x-radius-5, center_y-radius-5), (center_x+radius+5, center_y+radius+5), (0,255,255), 3) 
            cv2.putText(updated_img, "Circle",(circles[i][0], circles[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255))  
    return updated_img

def detect_triangles(detection_img, threshold_img):
    updated_img = detection_img.copy()
    contours, _ = cv2.findContours(threshold_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx_curve = cv2.approxPolyDP(contour, 3, True)
        
        if len(approx_curve) == 3:
            rect = cv2.boundingRect(contour)
            cv2.rectangle(updated_img, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 255, 255), 3)
            cv2.putText(updated_img, "Triangle", (rect[0]+(rect[2]//2), rect[1]+(rect[3]//2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))
    return updated_img

def detect_stickers(drawing_img):
    #templates = ["bobby", "burns", "gus"]
    templates = [bobby_sticker, burns_sticker, gus_sticker]
    names = ["Bobby", "Burns", "Gus"]
    i = 0
    detection_img = drawing_img.copy()
    gray_detection_img = cv2.cvtColor(detection_img, cv2.COLOR_BGR2GRAY)

    for template in templates:
        #temp_img = cv2.imread(template+".png")
        temp_img = template
        #house_img = cv2.resize(house_img, (25,25))
        gray_temp = cv2.cvtColor(temp_img, cv2.COLOR_BGR2GRAY)
        #ret, threshold_temp = cv2.threshold(gray_bobby, 1, 255, cv2.THRESH_BINARY)
        res = cv2.matchTemplate(gray_detection_img, gray_temp, cv2.TM_CCOEFF_NORMED)
        suppressed_res = compute_nonmax_suppression(res)
        location = np.where(suppressed_res >= 0.90)
        #print(location)

        for point in zip(*location[::-1]):
            cv2.rectangle(detection_img,point, (point[0]+100, point[1]+100), (0,255,255), 1)
            cv2.putText(detection_img, names[i], (point[0]+50, point[1]+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))
        i += 1
    return detection_img

def add_sticker_img(main_img, sticker_img, x_coord, y_coord):
    #cv2.imshow("bob", sticker_img)
    width = sticker_img.shape[1]
    height = sticker_img.shape[0]
    #if (x_coord >= 0 and x_coord <= 675) and (y_coord >= 100 and y
    try:
        main_img[y_coord:y_coord+height, x_coord:x_coord+width] = sticker_img
    except:
        print("Out of bounds for sticker")
    #main_img[y_coord:y_coord+height, x_coord:x_coord+width] = sticker_img
    return main_img

# Function carries out non max suppression on the image and returns the suppressed image
def compute_nonmax_suppression(drawing_img):
    rows, columns = drawing_img.shape[0], drawing_img.shape[1]
    draw_copy_img = drawing_img.copy()

    # For each pixel in the image, look at all of its neighbours in a 3x3 window. If any of its neighbours have a higher or equal 
    # pixel value, set the current pixel value to 0
    for i in range(0, rows):
        for j in range(0, columns):
            largest_value = True
            if j-1 >= 0:
                largest_value = draw_copy_img[i][j] > draw_copy_img[i][j-1]
            if largest_value and j+1 < columns:
                largest_value = draw_copy_img[i][j] > draw_copy_img[i][j+1]
            if largest_value and i-1 >= 0:
                largest_value = draw_copy_img[i][j] > draw_copy_img[i-1][j]
            if largest_value and i+1 < rows:
                largest_value = draw_copy_img[i][j] > draw_copy_img[i+1][j]
            if largest_value and i-1 >= 0 and j-1 >= 0:
                largest_value = draw_copy_img[i][j] > draw_copy_img[i-1][j-1]
            if largest_value and i-1 >= 0 and j+1 < columns:
                largest_value = draw_copy_img[i][j] > draw_copy_img[i-1][j+1]
            if largest_value and i+1 < rows and j-1 >= 0:
                largest_value = draw_copy_img[i][j] > draw_copy_img[i+1][j-1]
            if largest_value and i+1 < rows and j+1 < columns:
                largest_value = draw_copy_img[i][j] > draw_copy_img[i+1][j+1]
            
            if not largest_value:
                draw_copy_img[i][j] = 0
    return draw_copy_img 

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (900,600))
    hand_position, img = detector.findHands(img, flipType=False)

    display_colour_buttons()
    display_thickness_buttons()
    display_shape_buttons()
    display_mode_buttons()
    display_border_for_drawing_area()
    display_sticker_buttons()
    #cv2.rectangle(img, (100,100), (200,200), (0,0,255), cv2.FILLED)
    
    #cv2.namedWindow("Capture Window", cv2.WINDOW_NORMAL)
    #cv2.resizeWindow("Capture Window", 800,600)
    #print(img.shape)
    cv2.imshow("Capture Window", img)

    cv2.imshow("Blackboard Window", img2)

    #if mode == "draw":
    if hand_position:
        if hand_in_drawing_position(hand_position):
            not_drawing = 1
            if hand_in_drawing_area(hand_position):
                if mode == "draw":
                    x, y = hand_position[0]['lmList'][4][:2]
                    if draw_mode == "line" and drawing_line == False:
                        start_line = (x,y-100)
                        drawing_line = True
                    elif draw_mode == "rectangle" and drawing_rectangle == False:
                        start_line = (x,y-100)
                        drawing_rectangle = True

                    elif draw_mode == "circle" and drawing_circle == False:
                        start_line = (x,y-100)
                        drawing_circle = True
                    elif draw_mode == "circle" and drawing_circle == True:
                        circle_radius = min(circle_radius+1, 200)
                    elif draw_mode == "bobby" and drawing_bobby == False:
                        start_line = (x,y-100)
                        drawing_bobby = True
                    elif draw_mode == "burns" and drawing_bobby == False:
                        start_line = (x,y-100)
                        drawing_burns = True
                    elif draw_mode == "gus" and drawing_bobby == False:
                        start_line = (x,y-100)
                        drawing_gus = True
                        #cv2.putText(img, "Circle Radius: "+str(circle_radius), (80,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
                elif mode == "erase":
                    erase_screen(hand_position)
            else:
                if pressed_red_button(hand_position):
                    colour = (0,0,255)
                elif pressed_green_button(hand_position):
                    colour = (0,255,0)
                elif pressed_blue_button(hand_position):
                    colour = (255,217,4)
                elif pressed_increase_button(hand_position):
                    thickness_change += 1
                    increase_value = 1 if thickness_change % 5 == 0 else 0
                    #thickness_change = (thickness_change % 2)
                    thickness = min(100, thickness+increase_value)
                elif pressed_decrease_button(hand_position):
                    thickness_change += 1
                    decrease_value = 1 if thickness_change % 5 == 0 else 0
                    #thickness_change = (thickness_change % 2)
                    thickness = max(1, thickness-decrease_value)
                elif pressed_line_button(hand_position):
                    draw_mode = "line"
                elif pressed_rectangle_button(hand_position):
                    draw_mode = "rectangle"
                elif pressed_circle_button(hand_position):
                    draw_mode = "circle"
                elif pressed_bobby_button(hand_position):
                    draw_mode = "bobby"
                elif pressed_burns_button(hand_position):
                    draw_mode = "burns"
                elif pressed_gus_button(hand_position):
                    draw_mode = "gus"
                elif pressed_draw_button(hand_position):
                    if mode_num == 2:
                        img2 = old_img2
                        displayed_detected = False
                    mode_num = 0
                    mode = modes[mode_num]
                elif pressed_erase_button(hand_position): 
                    if mode_num == 2:
                        img2 = old_img2
                        displayed_detected = False
                    mode_num = 1
                    mode = modes[mode_num]
                elif pressed_shape_detection_button(hand_position):
                    mode_num = 2
                    mode = modes[mode_num]
                    if not displayed_detected:
                        old_img2 = img2
                        
                        #img2 = detect_stickers(img2)
                        img2 = detect_shapes(img2)
                        #img2 = detect_stickers(img2)
                        displayed_detected = True
        else:
            #if mode == "draw":

                if drawing_line and not_drawing == 15:
                    end_x, end_y = hand_position[0]['lmList'][4][:2]
                    cv2.line(img2, start_line, (end_x, end_y-100), colour, thickness)
                    drawing_line = False
                elif drawing_rectangle and not_drawing == 15:
                    end_x, end_y = hand_position[0]['lmList'][4][:2]
                    cv2.rectangle(img2, start_line, (end_x, end_y-100), colour, thickness)
                    drawing_rectangle = False
                elif drawing_circle and not_drawing == 15:
                    cv2.circle(img2, start_line, circle_radius, colour, thickness)
                    drawing_circle = False
                    circle_radius = 1
                elif drawing_bobby and not_drawing == 15:
                    x_coord = start_line[0]-50
                    y_coord = start_line[1]-50
                    img2 = add_sticker_img(img2, bobby_sticker, x_coord, y_coord)
                    #cv2.circle(img2, start_line, circle_radius, colour, thickness)
                    drawing_bobby = False
                elif drawing_burns and not_drawing == 15:
                    x_coord = start_line[0]-50
                    y_coord = start_line[1]-50
                    img2 = add_sticker_img(img2, burns_sticker, x_coord, y_coord)
                    #cv2.circle(img2, start_line, circle_radius, colour, thickness)
                    drawing_burns = False
                elif drawing_gus and not_drawing == 15:
                    x_coord = start_line[0]-50
                    y_coord = start_line[1]-50
                    img2 = add_sticker_img(img2, gus_sticker, x_coord, y_coord)
                    #cv2.circle(img2, start_line, circle_radius, colour, thickness)
                    drawing_gus = False
                    
                not_drawing += 1

                
                
                
    #elif mode == "erase":
    #    if hand_position:
    #        if hand_in_drawing_position(hand_position):
    #            if pressed_erase_button(hand_position):
    #                print("Switch to draw mode")
    #                mode = "draw"
    #            else:
    #                erase_screen(hand_position)

        #lmList = hands[0]['lmList']
        #print(lmList)
        #length, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        
        #if length < 10:
        #    x,y = lmList[8][:2]
        #    if(x > 100 and x < 200 ) and (y > 100 and y < 200):
        #        cv2.rectangle(img, (300,300), (400,400), (255,0,0), cv2.FILLED)
   
    
    # Close window with escape key
    key_press = cv2.waitKey(1)
    if key_press == 27:
        cv2.destroyAllWindows()
        break