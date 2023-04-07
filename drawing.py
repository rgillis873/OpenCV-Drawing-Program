import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Variables for video capture and hand detection. Detect only one hand
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands = 1, detectionCon=0.8)
cam_img = cap.read()

# Create blackboard image
blackboard_img = np.zeros((500, 675, 3), np.uint8)

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

# Variable for storing the start point in drawing different shapes
start_drawing_point = (0,0)

# Variables used for determing which type of shape/sticker is being used for drawing
drawing_line = False
drawing_rectangle = False
drawing_circle = False
drawing_bobby = False
drawing_burns = False
drawing_gus = False

# Variable to store radius of circles being drawn
circle_radius = 1

# Variable for tracking the number of frames the user is not drawing in
not_drawing = 1

# Variable to track whether the user is displaying the detected shapes image on the blackboard or not
displayed_detected = False

# Variable used to store blackboard image when mode is switched to shape detection. This is used 
# so that bounding boxes for shapes and stickers are not kept on the blackboard image.
old_blackboard_img = None

# Store colours options for different onscreen buttons
red_colours = [(0,0,255), (0,0,125)]
green_colours = [(0,255,0), (0,125,0)]
blue_colours = [(255,217,4), (125,110,2)]
shape_button_colours = [(20,200,200),(150,150,150)]
mode_button_colours = [(20,200,200),(150,150,150)]

# Variables used to store which button is currently selected. If the value is 0, then that button is currently selected
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
    line = cv2.rectangle(cam_img, (0,0), (100,90), shape_button_colours[line_selection], cv2.FILLED)
    rectangle = cv2.rectangle(cam_img, (115,0), (215,90), shape_button_colours[rectangle_selection], cv2.FILLED)
    circle = cv2.rectangle(cam_img, (230,0), (330,90), shape_button_colours[circle_selection], cv2.FILLED)
    cv2.putText(line, "Line", (15, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(rectangle, "Rect", (130, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(circle, "Circle", (240, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))

# Function displays the red, green and blue buttons on the screen
def display_colour_buttons():
    red = cv2.rectangle(cam_img, (345,0), (445,90), red_colours[red_selection], cv2.FILLED)
    green = cv2.rectangle(cam_img, (460,0), (560,90), green_colours[green_selection], cv2.FILLED)
    blue = cv2.rectangle(cam_img, (575,0), (675,90), blue_colours[blue_selection], cv2.FILLED)
    cv2.putText(red, "Red", (360, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(green, "Green", (460, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(blue, "Blue", (585, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))

# Function displays the increase and decrease drawing line thickness buttons on the screen
def display_thickness_buttons():
    increase = cv2.rectangle(cam_img, (690,0), (790,90), (150,150,150), cv2.FILLED)
    decrease = cv2.rectangle(cam_img, (690,105), (790,195), (150,150,150), cv2.FILLED)
    cv2.putText(increase, "+", (725, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(increase, str(thickness), (727, 67), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(decrease, "-", (725, 145), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(decrease, str(thickness), (727, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))

# Function displays the draw, erase and shape detection mode buttons on the screen 
def display_mode_buttons():
    draw = cv2.rectangle(cam_img, (690,210), (790,300), mode_button_colours[draw_selection], cv2.FILLED)
    erase = cv2.rectangle(cam_img, (690,315), (790,405), mode_button_colours[erase_selection], cv2.FILLED)
    shapes = cv2.rectangle(cam_img, (690,420), (790,510), mode_button_colours[shape_selection], cv2.FILLED)
    cv2.putText(draw, "Draw", (700, 260), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(erase, "Erase", (697, 360), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(shapes, "Shape", (695, 465), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))

# Function draws the border for the drawing area on the screen   
def display_border_for_drawing_area():
    cv2.line(cam_img, (0, 100), (675, 100), (0,0,0),4)
    cv2.line(cam_img, (675, 100), (675, 600), (0,0,0),4)

# Function displays the 3 sticker button types on the screen
def display_sticker_buttons():
    bobby = cv2.rectangle(cam_img, (800,0), (890,90), shape_button_colours[bobby_selection], cv2.FILLED)
    burns = cv2.rectangle(cam_img, (800,105), (890,195), shape_button_colours[burns_selection], cv2.FILLED)
    gus = cv2.rectangle(cam_img, (800,210), (890,300), shape_button_colours[gus_selection], cv2.FILLED)
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
        cv2.rectangle(blackboard_img, (x,y-100), (x+100,y), (0,0,0), cv2.FILLED)

# Function determines if the hand detected on screen is in the drawing position.
# Drawing position is with the thumb and index finger pressed together
# parameter hand position stores the x,y coordinates of the hand detected on the screen 
def hand_in_drawing_position(hand_position):
    global cam_img
    in_position = False

    # Determine the distance between the thumb and index finger
    lmList = hand_position[0]['lmList']
    length, _, cam_img = detector.findDistance(lmList[4][:2], lmList[8][:2], cam_img)
        
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

# Function is used to detect triangles, circles and different types of sticker images in the drawing image. A
# bounding box is drawn around the detected shape and its name is written on the shape as well. The image with the 
# detected shapes is returned
#
# parameter drawing_img is the image that will be searched for any matching shapes  
def detect_shapes(drawing_img):
    detection_img = drawing_img.copy()
    
    # Convert the image to grayscale, blur it and threshold it
    gray_scale_img = cv2.cvtColor(detection_img, cv2.COLOR_BGR2GRAY)
    blur_img = cv2.GaussianBlur(gray_scale_img, (7,7), 1.5,1.5)
    _, black_white_thresholded_img = cv2.threshold(blur_img, 1, 255, cv2.THRESH_BINARY)

    # Detect any triangles, circles or stickers in the image
    detection_img = detect_triangles(detection_img, black_white_thresholded_img)
    detection_img = detect_circles(detection_img, blur_img)
    detection_img = detect_stickers(detection_img, gray_scale_img)

    return detection_img

# Function is used to detect any circles that have been drawn in the image.
# Returns the image with bounding boxes drawn around detected circles
#
# parameter detection_img is the image that will be searched for any matching circles
# blur_img is the gaussian blurred version of the image  
def detect_circles(detection_img, blur_img):
    updated_img = detection_img.copy()

    # Use Hough Transform to detect circles in the image
    detected_circles = cv2.HoughCircles(blur_img, cv2.HOUGH_GRADIENT, 1, 100,  param1=100, param2=40, minRadius=1, maxRadius=200)
    
    # For any circles that were detected, draw a bounding box around them and write the word circle on the bounding box
    if detected_circles is not None:
        detected_circles = np.round(detected_circles[0,:]).astype("int")
        for i in range(0, len(detected_circles)):
            center_x = detected_circles[i][0]
            center_y = detected_circles[i][1]
            radius = detected_circles[i][2]  
            cv2.rectangle(updated_img, (center_x-radius-5, center_y-radius-5), (center_x+radius+5, center_y+radius+5), (0,255,255), 3) 
            cv2.putText(updated_img, "Circle",(center_x, center_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)  
    return updated_img

# Function is used to detect any triangles that are drawn in the image.
# Returns the image with bounding boxes drawn around detected triangles.
#
# parameter detection_img is the image that will be searched for any matching triangles
# threshold_img is the thresholded version of the image  
def detect_triangles(detection_img, threshold_img):
    updated_img = detection_img.copy()

    # Determine the contours for any shapes in the image
    contours, _ = cv2.findContours(threshold_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # For each contour, determine its approximate shape. If the shape has 3 sides, identify it as a triangle
    for contour in contours:
        approx_curve = cv2.approxPolyDP(contour, 3, True)
        
        # Draw a bounding box and write the word triangle on any detected triangles
        if len(approx_curve) == 3:
            rect = cv2.boundingRect(contour)
            cv2.rectangle(updated_img, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 255, 255), 3)
            cv2.putText(updated_img, "Triangle", (rect[0]+(rect[2]//2), rect[1]+(rect[3]//2)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    return updated_img


# Function uses template matching to identify any sticker types that were drawn on the image. 
# There are three sticker types: Bobby (for Bobby Hill), Burns (for Mr. Burns), and Gus (for Gus Griswald).
# A bounding box is drawn around any identified stickers and their name is written on the bounding box as well
# The image with the detected stickers is returned
#
# parameter detection_img is the image that will be searched for any matching stickers
# parameter gray_detection_img is grayscale version of the image that will be searched for any matching stickers
def detect_stickers(detection_img, gray_detection_img):
    templates = [bobby_sticker, burns_sticker, gus_sticker]
    sticker_names = ["Bobby", "Burns", "Gus"]
    i = 0
    detection_copy_img = detection_img.copy()

    # For each of the 3 templates:
    # 1. Convert them to grayscale
    # 2. Use template matching to determine the matching points in the drawing image
    # 3. Use non maxima suppression to eliminate matches that are overlapping
    # 4. Locate any matching points that are equal to or greater than the threshold of 0.9
    # 5. Combine the x and y coordinates returned from np.where into iterable tuples of coordinates
    # 6. Draw a bounding box around each point and write the name of the sticker type on the bounding box 
    for template in templates:
        temp_img = template
        gray_temp = cv2.cvtColor(temp_img, cv2.COLOR_BGR2GRAY)
        results = cv2.matchTemplate(gray_detection_img, gray_temp, cv2.TM_CCOEFF_NORMED)
        suppressed_results = compute_nonmax_suppression(results)
        best_matching_points = np.where(suppressed_results >= 0.90)
        points = zip(*best_matching_points[::-1])

        for point in points:
            cv2.rectangle(detection_copy_img,point, (point[0]+100, point[1]+100), (0,255,255), 1)
            cv2.putText(detection_copy_img, sticker_names[i], (point[0]+50, point[1]+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        i += 1
    return detection_copy_img

# Function is used to add a sticker to the drawing image
#
# parameter drawing_img is the image where the sticker will be added
# parameter sticker_img is the sticker image that will be added to the image
# parameter x_coord is the x coordinate of where the sticker will be placed in the image
# parameter y_coord is the y coordinate of where the sticker will be placed in the image
def add_sticker_img(drawing_img, sticker_img, x_coord, y_coord):
    width = sticker_img.shape[1]
    height = sticker_img.shape[0]

    # Add the sticker at the specified coordinates. If the part of the sticker will be placed
    # out of bounds, don't place it. Instead print the error message.
    try:
        drawing_img[y_coord:y_coord+height, x_coord:x_coord+width] = sticker_img
    except:
        print("Out of bounds position for placing sticker")
    return drawing_img

# Function carries out non max suppression on the template match image and returns the suppressed image
#
# parameter template_match_img is the computed image resulting from matchTemplate
def compute_nonmax_suppression(template_match_img):
    rows, columns = template_match_img.shape[0], template_match_img.shape[1]
    template_match_copy_img = template_match_img.copy()

    # For each pixel in the image, look at all of its neighbours in a 3x3 window. If any of its neighbours have a higher or equal 
    # pixel value, set the current pixel value to 0
    for i in range(0, rows):
        for j in range(0, columns):
            largest_value = True
            if j-1 >= 0:
                largest_value = template_match_copy_img[i][j] > template_match_copy_img[i][j-1]
            if largest_value and j+1 < columns:
                largest_value = template_match_copy_img[i][j] > template_match_copy_img[i][j+1]
            if largest_value and i-1 >= 0:
                largest_value = template_match_copy_img[i][j] > template_match_copy_img[i-1][j]
            if largest_value and i+1 < rows:
                largest_value = template_match_copy_img[i][j] > template_match_copy_img[i+1][j]
            if largest_value and i-1 >= 0 and j-1 >= 0:
                largest_value = template_match_copy_img[i][j] > template_match_copy_img[i-1][j-1]
            if largest_value and i-1 >= 0 and j+1 < columns:
                largest_value = template_match_copy_img[i][j] > template_match_copy_img[i-1][j+1]
            if largest_value and i+1 < rows and j-1 >= 0:
                largest_value = template_match_copy_img[i][j] > template_match_copy_img[i+1][j-1]
            if largest_value and i+1 < rows and j+1 < columns:
                largest_value = template_match_copy_img[i][j] > template_match_copy_img[i+1][j+1]
            
            # If the value is not the largest in the 3x3 neighbourhood, set it to zero
            if not largest_value:
                template_match_copy_img[i][j] = 0
    return template_match_copy_img 

# Main loop for running the drawing program
while True:

    # Read in the image from the web cam and display the position of the hand on the screen
    _, cam_img = cap.read()
    cam_img = cv2.flip(cam_img, 1)
    cam_img = cv2.resize(cam_img, (900,600))
    hand_position, cam_img = detector.findHands(cam_img, flipType=False)

    # Display the buttons and border on the webcam image
    display_colour_buttons()
    display_thickness_buttons()
    display_shape_buttons()
    display_mode_buttons()
    display_border_for_drawing_area()
    display_sticker_buttons()

    # Show the webcam image and blackboard image
    cv2.imshow("Capture Window", cam_img)
    cv2.imshow("Blackboard Window", blackboard_img)

    # If the hand is detected in the image
    if hand_position:

        # Determine if the hand is in the drawing position
        if hand_in_drawing_position(hand_position):
            not_drawing = 1

            # Determine if the hand is in within the drawing area
            if hand_in_drawing_area(hand_position):
                
                # If the user is in drawing mode
                if mode == "draw":
                    # Determine the thumb position
                    x, y = hand_position[0]['lmList'][4][:2]
                    
                    # If the user is drawing a line, store the start position of the line
                    if draw_mode == "line" and drawing_line == False:
                        start_drawing_point = (x,y-100)
                        drawing_line = True
        
                    # If the user is drawing a rectangle, store the start position of the upper corner of the rectangle
                    elif draw_mode == "rectangle" and drawing_rectangle == False:
                        start_drawing_point = (x,y-100)
                        drawing_rectangle = True

                    # If the user is drawing a circle, store the center position of where the circle will be placed
                    elif draw_mode == "circle" and drawing_circle == False:
                        start_drawing_point = (x,y-100)
                        drawing_circle = True
                    
                    # If user is in the process of drawing a circle, increase the radius of the circle while they hold
                    # their hand in the drawing position. Only increase to a maximum radius of 200.
                    elif draw_mode == "circle" and drawing_circle == True:
                        circle_radius = min(circle_radius+1, 200)
                    
                    # If the user is drawing any of the three stickers, store the center point of where the sticker will be placed
                    elif draw_mode == "bobby" and drawing_bobby == False:
                        start_drawing_point = (x,y-100)
                        drawing_bobby = True
                    elif draw_mode == "burns" and drawing_bobby == False:
                        start_drawing_point = (x,y-100)
                        drawing_burns = True
                    elif draw_mode == "gus" and drawing_bobby == False:
                        start_drawing_point = (x,y-100)
                        drawing_gus = True
                
                # If the user is in erase mode, erase the 100x100 square around the user's thumb
                elif mode == "erase":
                    erase_screen(hand_position)
            
            # If user's hand is not in the drawing area, check to see if they are pressing buttons
            else:
                # Check to see if the user presses red button. Change drawing colour to red if they do
                if pressed_red_button(hand_position):
                    colour = (0,0,255)
                
                # Check to see if the user presses green button. Change drawing colour to green if they do
                elif pressed_green_button(hand_position):
                    colour = (0,255,0)

                # Check to see if the user presses blue button. Change drawing colour to blue if they do
                elif pressed_blue_button(hand_position):
                    colour = (255,217,4)

                # Check to see if user pressed the increase line thickness button. Increase the line thickness if they do.
                # To prevent button hypersensitivity, only increase thickness once for every 5 image frames that are read in.
                # Max line thickness is 100.
                elif pressed_increase_button(hand_position):
                    thickness_change += 1
                    increase_value = 1 if thickness_change % 5 == 0 else 0
                    thickness = min(100, thickness+increase_value)
                
                # Check to see if user pressed the decrease line thickness button. Decrease the line thickness if they do.
                # To prevent button hypersensitivity, only decrease thickness once for every 5 image frames that are read in.
                # Minimum line thickness is 1.
                elif pressed_decrease_button(hand_position):
                    thickness_change += 1
                    decrease_value = 1 if thickness_change % 5 == 0 else 0
                    thickness = max(1, thickness-decrease_value)
                
                # Check to see if user pressed draw line button. Change drawing mode to line if they did.
                elif pressed_line_button(hand_position):
                    draw_mode = "line"
                
                # Check to see if user pressed draw rectangle button. Change drawing mode to rectangle if they did.
                elif pressed_rectangle_button(hand_position):
                    draw_mode = "rectangle"
                
                # Check to see if user pressed draw circle button. Change drawing mode to circle if they did.
                elif pressed_circle_button(hand_position):
                    draw_mode = "circle"
                
                # Check to see if user pressed draw Bobby Hill sticker button. Change drawing mode to bobby if they did.
                elif pressed_bobby_button(hand_position):
                    draw_mode = "bobby"
                         
                # Check to see if user pressed draw Mr. Burns sticker button. Change drawing mode to burns if they did.
                elif pressed_burns_button(hand_position):
                    draw_mode = "burns"

                # Check to see if user pressed draw Gus Griswald sticker button. Change drawing mode to gus if they did.
                elif pressed_gus_button(hand_position):
                    draw_mode = "gus"
                
                # Check if user pressed button to switch to drawing mode. Change mode to drawing mode if they did.
                # Mode 0 is for drawing.
                elif pressed_draw_button(hand_position):
                    # Mode number 2 is for shape detection. If user is switching from shape detection mode to 
                    # drawing mode, replace the image with bounding boxes with the previous image without the bounding boxes
                    if mode_num == 2:
                        blackboard_img = old_blackboard_img
                        displayed_detected = False
                    mode_num = 0
                    mode = modes[mode_num]

                # Check if user pressed button to switch to erasing mode. Change mode to erasing mode if they did.
                # Mode 1 is for erasing.
                elif pressed_erase_button(hand_position):
                    # Mode number 2 is for shape detection. If user is switching from shape detection mode to
                    # drawing mode, replace the image with bounding boxes with the previous image without the bounding boxes 
                    if mode_num == 2:
                        blackboard_img = old_blackboard_img
                        displayed_detected = False
                    mode_num = 1
                    mode = modes[mode_num]

                # Check if user pressed button to switch to shape detection mode. Change mode to shape detection mode if they did.
                # Mode 2 is for shape detection.
                elif pressed_shape_detection_button(hand_position):
                    mode_num = 2
                    mode = modes[mode_num]

                    # When switching to shape detection mode, store the previous image that does not contain bounding boxes.
                    # This stored image will be used for switching back to drawing or erasing mode. This way the bounding boxes
                    # will not remain on the blackboard image
                    if not displayed_detected:
                        old_blackboard_img = blackboard_img
                        blackboard_img = detect_shapes(blackboard_img)
                        displayed_detected = True
        
        # If user's hand is not in the drawing position
        else:
            # The not_drawing variable is used to count the number of frames that the user's hand is not in drawing position.
            # The hand detection can lose focus momentarily while the hand is in motion. This can potentially interrupt the drawing process.
            # To counteract this, a check is added for drawing to see if there have been 15 frames read in without the user's hand being 
            # in the drawing position. If they were drawing something and their hand is momentarily not detected to be in the drawing position,
            # this helps to prevent unwanted drawings from occurring. 

            # If user was drawing a line and released their hand from the drawing position this means they are done 
            # drawing the line. It can now be drawn on the blackboard screen
            if drawing_line and not_drawing == 15:
                # Get the final coordinates of their thumb position and use that as the end point for drawing the line
                end_x, end_y = hand_position[0]['lmList'][4][:2]
                cv2.line(blackboard_img, start_drawing_point, (end_x, end_y-100), colour, thickness)
                drawing_line = False
            
            # If user was drawing a rectangle and released their hand from the drawing position this means they are done 
            # drawing the rectangle. It can now be drawn on the blackboard screen
            elif drawing_rectangle and not_drawing == 15:
                # Get the final coordinates of their thumb position and use that as the position for the opposite corner 
                # for drawing the rectangle
                end_x, end_y = hand_position[0]['lmList'][4][:2]
                cv2.rectangle(blackboard_img, start_drawing_point, (end_x, end_y-100), colour, thickness)
                drawing_rectangle = False
            
            # If user was drawing a circle and released their hand from the drawing position this means they are done 
            # drawing the circle. It can now be drawn on the blackboard screen
            elif drawing_circle and not_drawing == 15:
                # Draw the circle centered around where the user has indicated and with the radius they have determined
                cv2.circle(blackboard_img, start_drawing_point, circle_radius, colour, thickness)
                drawing_circle = False
                circle_radius = 1
            
            # If user was drawing a Bobby Hill sticker and released their hand from the drawing position this means they are done 
            # drawing the sticker. It can now be drawn on the blackboard screen
            elif drawing_bobby and not_drawing == 15:
                # Draw the sticker using the starting point as the center of where the sticker will be placed
                x_coord = start_drawing_point[0]-50
                y_coord = start_drawing_point[1]-50
                blackboard_img = add_sticker_img(blackboard_img, bobby_sticker, x_coord, y_coord)
                drawing_bobby = False
            
            # If user was drawing a Mr. Burns sticker and released their hand from the drawing position this means they are done 
            # drawing the sticker. It can now be drawn on the blackboard screen
            elif drawing_burns and not_drawing == 15:
                # Draw the sticker using the starting point as the center of where the sticker will be placed
                x_coord = start_drawing_point[0]-50
                y_coord = start_drawing_point[1]-50
                blackboard_img = add_sticker_img(blackboard_img, burns_sticker, x_coord, y_coord)
                drawing_burns = False
            
            # If user was drawing a Gus Griswald sticker and released their hand from the drawing position this means they are done 
            # drawing the sticker. It can now be drawn on the blackboard screen
            elif drawing_gus and not_drawing == 15:
                # Draw the sticker using the starting point as the center of where the sticker will be placed
                x_coord = start_drawing_point[0]-50
                y_coord = start_drawing_point[1]-50
                blackboard_img = add_sticker_img(blackboard_img, gus_sticker, x_coord, y_coord)
                drawing_gus = False

            # Increase this for every frame read in that the hand is not in drawing mode       
            not_drawing += 1

    # Close window with escape key
    key_press = cv2.waitKey(1)
    if key_press == 27:
        cv2.destroyAllWindows()
        break