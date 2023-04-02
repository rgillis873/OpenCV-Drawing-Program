import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands = 1, detectionCon=0.8)
img = cap.read()
img2 = np.zeros((600, 800, 3), np.uint8)
plus_sign = cv2.imread("plus.jpg", 0).resize((100,100))
minus_sign = cv2.imread("minus.jpg", 0).resize((100,100))
thickness = 3
colour = (0,255,0)
mode = "draw"

def display_colour_buttons():
    red = cv2.rectangle(img, (330,0), (430,75), (0,0,255), cv2.FILLED)
    green = cv2.rectangle(img, (440,0), (540,75), (0,255,0), cv2.FILLED)
    blue = cv2.rectangle(img, (550,0), (650,75), (255,0,0), cv2.FILLED)
    cv2.putText(red, "Red", (350, 37), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(green, "Green", (450, 37), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(blue, "Blue", (570, 37), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))

def display_thickness_buttons():
    cv2.rectangle(img, (550,100), (650,200), (0,0,0), cv2.FILLED)
    cv2.rectangle(img, (550,210), (650,310), (200,200,200), cv2.FILLED)
    
def display_erase_button():
    cv2.rectangle(img, (550,320), (650,420), (120,120,120), cv2.FILLED)

def display_shape_buttons():
    line = cv2.rectangle(img, (10,0), (110,75), (150,150,150), cv2.FILLED)
    rectangle = cv2.rectangle(img, (115,0), (215,75), (150,150,150), cv2.FILLED)
    circle = cv2.rectangle(img, (220,0), (320,75), (150,150,150), cv2.FILLED)
    cv2.putText(line, "Line", (20, 37), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(rectangle, "Rect", (125, 37), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(circle, "Circle", (230, 37), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))

def pressed_line_button(hand_position):
    pressed = False
    x, y = hand_position[0]['lmList'][12][:2]
    #print(x)
    if(x >= 10 and x <= 110 ) and (y >= 0 and y <= 75):
        pressed = True
    return pressed

def pressed_rectangle_button(hand_position):
    pressed = False
    x, y = hand_position[0]['lmList'][12][:2]
    #print(x)
    if(x >= 115 and x <= 215 ) and (y >= 0 and y <= 75):
        pressed = True
    return pressed

def pressed_circle_button(hand_position):
    pressed = False
    x, y = hand_position[0]['lmList'][12][:2]
    #print(x)
    if(x >= 220 and x <= 320 ) and (y >= 0 and y <= 75):
        pressed = True
    return pressed

def pressed_red_button(hand_position):
    pressed = False
    x, y = hand_position[0]['lmList'][12][:2]
    #print(x)
    if(x >= 330 and x <= 430 ) and (y >= 0 and y <= 75):
        pressed = True
    return pressed

def pressed_green_button(hand_position):
    pressed = False
    x, y = hand_position[0]['lmList'][12][:2]
    #print(x)
    if(x >= 440 and x <= 540 ) and (y >= 0 and y <= 75):
        pressed = True
    return pressed

def pressed_blue_button(hand_position):
    pressed = False
    x, y = hand_position[0]['lmList'][12][:2]
    #print(x)
    if(x >= 550 and x <= 650 ) and (y >= 0 and y <= 75):
        pressed = True
    return pressed

def pressed_increase_button(hand_position):
    pressed = False
    x, y = hand_position[0]['lmList'][12][:2]
    #print(x)
    if(x >= 550 and x <= 650 ) and (y >= 100 and y <= 200):
        pressed = True
    return pressed

def pressed_decrease_button(hand_position):
    pressed = False
    x, y = hand_position[0]['lmList'][12][:2]
    #print(x)
    if(x >= 550 and x <= 650 ) and (y >= 210 and y <= 310):
        pressed = True
    return pressed

def pressed_erase_button(hand_position):
    pressed = False
    x, y = hand_position[0]['lmList'][12][:2]
    #print(x)
    if(x >= 550 and x <= 650 ) and (y >= 320 and y <= 420):
        pressed = True
    return pressed
    
def erase_screen(hand_position):
    x, y = hand_position[0]['lmList'][12][:2]
    
    if(x >= 0 and x <= 800) and (y >= 0 and y <= 600):
        cv2.rectangle(img2, (x,y), (x+50,y+50), (0,0,0), cv2.FILLED)

def hand_in_drawing_position(hand_position):
    global img
    lmList = hand_position[0]['lmList']
        #print(lmList)
    length, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        
    
    if length < 8:
        return True
        #x,y = lmList[8][:2]
        #if(x > 100 and x < 200 ) and (y > 100 and y < 200):
        #    cv2.rectangle(img, (300,300), (400,400), (255,0,0), cv2.FILLED)
    return False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hand_position, img = detector.findHands(img, flipType=False)

    display_colour_buttons()
    display_thickness_buttons()
    display_shape_buttons()
    display_erase_button()
    #cv2.rectangle(img, (100,100), (200,200), (0,0,255), cv2.FILLED)
    
    cv2.namedWindow("Capture Window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Capture Window", 800,600)
    cv2.imshow("Capture Window", img)

    cv2.imshow("Second Window", img2)

    if mode == "draw":
        if hand_position:
            if hand_in_drawing_position(hand_position):
                #print(hand_position)
                cv2.rectangle(img2, (100,100), (200,200), colour, thickness)

                if pressed_red_button(hand_position):
                    print("RED")
                    colour = (0,0,255)
                elif pressed_green_button(hand_position):
                    colour = (0,255,0)
                elif pressed_blue_button(hand_position):
                    colour = (255,0,0)
                elif pressed_increase_button(hand_position):
                    thickness += 1
                    print(thickness)
                elif pressed_decrease_button(hand_position):
                    thickness = max(1, thickness-1)
                    print(thickness)

                elif pressed_line_button(hand_position):
                    print("line")
                elif pressed_rectangle_button(hand_position):
                    print("rectangle")
                elif pressed_circle_button(hand_position):
                    print("circle")
                elif pressed_erase_button(hand_position):
                    print("Switch to erase mode")
                    mode = "erase"
    elif mode == "erase":
        if hand_position:
            if hand_in_drawing_position(hand_position):
                if pressed_erase_button(hand_position):
                    print("Switch to draw mode")
                    mode = "draw"
                else:
                    erase_screen(hand_position)

        #lmList = hands[0]['lmList']
        #print(lmList)
        #length, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        
        #if length < 10:
        #    x,y = lmList[8][:2]
        #    if(x > 100 and x < 200 ) and (y > 100 and y < 200):
        #        cv2.rectangle(img, (300,300), (400,400), (255,0,0), cv2.FILLED)
   
    
    # Close window with escape key
    key_press = cv2.waitKey(1) & 0xFF
    if key_press == 27:
        cv2.destroyAllWindows()
        break