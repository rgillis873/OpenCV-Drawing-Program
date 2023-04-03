import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands = 1, detectionCon=0.8)
img = cap.read()
img2 = np.zeros((500, 680, 3), np.uint8)
plus_sign = cv2.imread("plus.jpg", 0).resize((100,100))
minus_sign = cv2.imread("minus.jpg", 0).resize((100,100))
thickness = 3
colour = (0,0,255)
mode = "draw"
mode_num = 0
modes = ["draw", "erase"]
draw_mode = "line"
start_line = (0,0)
end_line = (10,10)
drawing_line = False
drawing_rectangle = False
drawing_circle = False
circle_radius = 1
erase_button_counter = 1
not_drawing = 1

red_colours = [(0,0,255), (0,0,125)]
green_colours = [(0,255,0), (0,125,0)]
blue_colours = [(255,217,4), (125,110,2)]

shape_button_colours = [(20,200,200),(150,150,150)]

red_selection = 0
green_selection = 1
blue_selection = 1

line_selection = 0
rectangle_selection = 1
circle_selection = 1


def display_colour_buttons():
    red = cv2.rectangle(img, (330,0), (430,75), red_colours[red_selection], cv2.FILLED)
    green = cv2.rectangle(img, (440,0), (540,75), green_colours[green_selection], cv2.FILLED)
    blue = cv2.rectangle(img, (550,0), (650,75), blue_colours[blue_selection], cv2.FILLED)
    cv2.putText(red, "Red", (350, 37), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(green, "Green", (450, 37), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(blue, "Blue", (570, 37), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))

def display_thickness_buttons():
    cv2.rectangle(img, (550,100), (650,200), (0,0,0), cv2.FILLED)
    cv2.rectangle(img, (550,210), (650,310), (200,200,200), cv2.FILLED)
    
def display_erase_button():
    cv2.rectangle(img, (550,320), (650,420), (120,120,120), cv2.FILLED)

def display_border_for_drawing_area():
    cv2.line(img, (0, 80), (540, 80), (0,0,0),4)
    cv2.line(img, (540, 80), (540, 800), (0,0,0),4)

def display_shape_buttons():
    line = cv2.rectangle(img, (10,0), (110,75), shape_button_colours[line_selection], cv2.FILLED)
    rectangle = cv2.rectangle(img, (115,0), (215,75), shape_button_colours[rectangle_selection], cv2.FILLED)
    circle = cv2.rectangle(img, (220,0), (320,75), shape_button_colours[circle_selection], cv2.FILLED)
    cv2.putText(line, "Line", (20, 37), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(rectangle, "Rect", (125, 37), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))
    cv2.putText(circle, "Circle", (230, 37), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0))

def pressed_line_button(hand_position):
    global line_selection
    global rectangle_selection
    global circle_selection

    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    #print(x)
    if(x >= 10 and x <= 110 ) and (y >= 0 and y <= 75):
        pressed = True
        line_selection = 0
        rectangle_selection = 1
        circle_selection = 1
    return pressed

def pressed_rectangle_button(hand_position):
    global line_selection
    global rectangle_selection
    global circle_selection

    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    #print(x)
    if(x >= 115 and x <= 215 ) and (y >= 0 and y <= 75):
        pressed = True
        line_selection = 1
        rectangle_selection = 0
        circle_selection = 1
    return pressed

def pressed_circle_button(hand_position):
    global line_selection
    global rectangle_selection
    global circle_selection

    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    if(x >= 220 and x <= 320 ) and (y >= 0 and y <= 75):
        pressed = True
        line_selection = 1
        rectangle_selection = 1
        circle_selection = 0
    return pressed

def pressed_red_button(hand_position):
    global red_selection
    global green_selection
    global blue_selection

    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    #print(x)
    if(x >= 330 and x <= 430 ) and (y >= 0 and y <= 75):
        pressed = True
        red_selection = 0
        green_selection = 1
        blue_selection = 1
    return pressed

def pressed_green_button(hand_position):
    global red_selection
    global green_selection
    global blue_selection

    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    #print(x)
    if(x >= 440 and x <= 540 ) and (y >= 0 and y <= 75):
        pressed = True
        red_selection = 1
        green_selection = 0
        blue_selection = 1
    return pressed

def pressed_blue_button(hand_position):
    global red_selection
    global green_selection
    global blue_selection

    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    #print(x)
    if(x >= 550 and x <= 650 ) and (y >= 0 and y <= 75):
        pressed = True
        red_selection = 1
        green_selection = 1
        blue_selection = 0
    return pressed

def pressed_increase_button(hand_position):
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    #print(x)
    if(x >= 550 and x <= 650 ) and (y >= 100 and y <= 200):
        pressed = True
    return pressed

def pressed_decrease_button(hand_position):
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    #print(x)
    if(x >= 550 and x <= 650 ) and (y >= 210 and y <= 310):
        pressed = True
    return pressed

def pressed_erase_button(hand_position):
    pressed = False
    x, y = hand_position[0]['lmList'][4][:2]
    #print(x)
    if(x >= 550 and x <= 650 ) and (y >= 320 and y <= 420):
        pressed = True
    return pressed
    
def erase_screen(hand_position):
    x, y = hand_position[0]['lmList'][4][:2]
    
    if(x >= 0 and x <= 800) and (y >= 0 and y <= 600):
        cv2.rectangle(img2, (x,y), (x+100,y+100), (0,0,0), cv2.FILLED)

def hand_in_drawing_position(hand_position):
    global img
    lmList = hand_position[0]['lmList']
        #print(lmList)
    length, _, img = detector.findDistance(lmList[4][:2], lmList[8][:2], img)
        
    
    if length <= 20:
        return True
        #x,y = lmList[8][:2]
        #if(x > 100 and x < 200 ) and (y > 100 and y < 200):
        #    cv2.rectangle(img, (300,300), (400,400), (255,0,0), cv2.FILLED)
    return False

def hand_in_drawing_area(hand_position):
    in_drawing_area = False
    x, y = hand_position[0]['lmList'][8][:2]
    if(x >= 0 and x < 540) and (y > 80 and y < 600):
        in_drawing_area = True
    return in_drawing_area

def hand_in_button_area(hand_position):
    in_button_area = False
    x, y = hand_position[0]['lmList'][8][:2]
    if ((x >= 0 and x <= 600) and (y >= 0 and y <= 80)) or ((x >= 540 and x <= 650) and (y >= 0 and y <= 600)):
        in_button_area = True
    return in_button_area

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hand_position, img = detector.findHands(img, flipType=False)

    display_colour_buttons()
    display_thickness_buttons()
    display_shape_buttons()
    display_erase_button()
    display_border_for_drawing_area()
    #cv2.rectangle(img, (100,100), (200,200), (0,0,255), cv2.FILLED)
    
    cv2.namedWindow("Capture Window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Capture Window", 800,600)
    cv2.imshow("Capture Window", img)

    cv2.imshow("Second Window", img2)

    #if mode == "draw":
    if hand_position:
        if hand_in_drawing_position(hand_position):
            not_drawing = 1
            if hand_in_drawing_area(hand_position):
                if mode == "draw":
                    x, y = hand_position[0]['lmList'][4][:2]
                    if draw_mode == "line" and drawing_line == False:
                        start_line = (x,y-80)
                        drawing_line = True
                            #while(hand_in_drawing_position(hand_position)):
                            #    continue
                            #end_x, end_y = hand_position[0]['lmList'][12][:2]
                            #cv2.line(img2, (x,y), (end_x, end_y), colour, thickness)
                    elif draw_mode == "rectangle" and drawing_rectangle == False:
                        start_line = (x,y-80)
                        drawing_rectangle = True

                    elif draw_mode == "circle" and drawing_circle == False:
                        start_line = (x,y-80)
                        drawing_circle = True
                    elif draw_mode == "circle" and drawing_circle == True:
                        circle_radius = min(circle_radius+1, 200)
                elif mode == "erase":
                    erase_screen(hand_position)
            else:
                if pressed_red_button(hand_position):
                    print("RED")
                    colour = (0,0,255)
                elif pressed_green_button(hand_position):
                    colour = (0,255,0)
                elif pressed_blue_button(hand_position):
                    colour = (255,217,4)
                elif pressed_increase_button(hand_position):
                    thickness += 1
                    print(thickness)
                elif pressed_decrease_button(hand_position):
                    thickness = max(1, thickness-1)
                    print(thickness)
                elif pressed_line_button(hand_position):
                    draw_mode = "line"
                elif pressed_rectangle_button(hand_position):
                    draw_mode = "rectangle"
                elif pressed_circle_button(hand_position):
                    draw_mode = "circle"
                elif pressed_erase_button(hand_position): 
                    if erase_button_counter == 5:
                        mode_num = (mode_num + 1) %2
                        mode =  modes[mode_num]
                        print("Switch to "+ mode+" mode")
                        erase_button_counter = 0
                    erase_button_counter += 1
        else:
            if drawing_line and not_drawing == 10:
                end_x, end_y = hand_position[0]['lmList'][4][:2]
                cv2.line(img2, start_line, (end_x, end_y-80), colour, thickness)
                drawing_line = False
            elif drawing_rectangle and not_drawing == 10:
                end_x, end_y = hand_position[0]['lmList'][4][:2]
                cv2.rectangle(img2, start_line, (end_x, end_y-80), colour, thickness)
                drawing_rectangle = False
            elif drawing_circle and not_drawing == 10:
                cv2.circle(img2, start_line, circle_radius, colour, thickness)
                drawing_circle = False
                circle_radius = 1
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
    key_press = cv2.waitKey(1) & 0xFF
    if key_press == 27:
        cv2.destroyAllWindows()
        break