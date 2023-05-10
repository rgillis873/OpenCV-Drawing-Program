What's included in this folder:
Image of Bobby Hill used for sticker in drawing program named as: bobby.png
Image of Mr. Burns used for sticker in drawing program named as: burns.png
Image of Gus Griswald used for sticker in drawing program named as: gus.png
The python file used to implement the drawing program named as: drawing.py

Link to video demo of the program:


Installation instructions before running the program:
Install OpenCV for python:
from command line run: pip install opencv-python

Install NumPy for python (pretty sure this is installed with OpenCV, but just in case it's not):
pip install numpy

Install MediaPipe libray:
pip install mediapipe

Install CVZone:
pip install cvzone

Prior to running the program:
Make sure webcam is not disabled, as the program needs to access it

To run the program:
from the command line, inside this folder, run the command:
python drawing.py

Using the program:
When the program loads you will see two windows: one with your webcam image and buttons and another with a black background.
The webcam window is what you can use to control the drawing program and your drawing output is displayed on the second window with 
the black background.
In the webcam window there are various buttons overlayed on the screen. The button functionality works as follows:
Line Button - Select this button to switch to drawing with lines
Rect Button - Select this button to switch to drawing with rectangles 
Circle Button - Select this button to switch to drawing with circles
Red Button - Select this button to switch to drawing with the colour red
Green Button - Select this button to switch to drawing with the colour green
Blue Button - Select this button to switch to drawing with the colour blue
+ Button - Press this button to increase the thickness of the shape you are drawing with. The thickness value is displayed on the button as well.
- Button - Press this button to Decrease the thickness of the shape you are drawing with. The thickness value is displayed on the button as well.
Bobby Button - Select this button to switch to drawing with sticker images of Bobby Hill
Burns Button - Select this button to switch to drawing with sticker images of Mr. Burns
Gus Button - Select this button to switch to drawing with sticker images of Gus Griswald
Draw Button - Select this button to use the drawing mode of the application. 
Erase Button - Select this button to use the erasing mode of the application. None of the drawing buttons are selectable if you are in this mode.
Shape Button - Select this button to use the shape detection mode of the application. None of the drawing buttons are selectable if you are in this mode.

Certain buttons are grouped together and only the selected button for the grouping will change to a highlighted colour. The other buttons in 
the grouping will be either gray or a faded colour.

Button Groupings:
Line, Rect, Circle, Bobby, Burns and Gus buttons are grouped together.
Red, Green and Blue buttons are grouped together.
Draw, Erase and Shape buttons are grouped together.

Drawing Area:
There is a boundary box drawn on the screen in black separating the buttons from the drawing area. In order to be able to draw, your hand needs 
to be positioned inside the drawing boundary area.

Hand Position for Drawing and Button Pushing:
In order to draw or push buttons, you need to have your thumb and index finger pressed together. This is the drawing position.

Pressing buttons:
With your hand in the drawing position, move your pressed thumb and index finger over the desired button. The colour of the button will 
change to show that you selected it.

Drawing:

Drawing Lines:
To draw a line, place your hand in the drawing position at the area you want to start drawing the line from. Move your hand across the screen 
with the thumb and index finger still pressed together until you reach the point where you want the line to end. Once you reach desired end point 
for the line, release your thumb and index finger from each other. Where you leave your thumb is where the end of the line will be placed.
![line_drawing](https://user-images.githubusercontent.com/59716448/236934340-d652dd81-abed-4041-907c-ff5c9b417ba4.gif)

Drawing Rectangles:
To draw a rectangle, place your hand in the drawing position at the area you want to start drawing the rectangle from. Move your hand across the screen 
with the thumb and index finger still pressed together until you reach the point where you want to place the opposite corner of the rectangle. 
Once you reach desired end point for rectangle, release your thumb and index finger from each other. Where you leave your thumb is where 
the opposite corner of the rectangle will be placed.
![rectangle_drawing](https://user-images.githubusercontent.com/59716448/236934623-9299852c-15e1-4666-b614-7887e46ee87c.gif)

Drawing Circles:
To draw a circle, place your hand in the drawing position at the area you want the center of the circle to be. The longer you hold your thumb and 
index finger together at this point, the larger the circle that you draw will be. To finish drawing the circle, just release your thumb and index 
finger.
![circles_smaller](https://github.com/rgillis873/COMP4102-Project/assets/59716448/0ffe7e59-96a2-488c-bde6-a32c8f794d84)

Drawing Stickers:
To draw a sticker, similar to drawing circles, place your hand in the drawing position at the area where you want the center of the sticker to be.
Then release your thumb and index finger to finish placing the sticker.
![stickers_small_enough](https://github.com/rgillis873/COMP4102-Project/assets/59716448/14f269ba-9ec6-4eb7-9760-bc63433af2a1)

Erasing:
To erase things from the blackboard image, first press the erase button to switch to eraser mode. Then using the same hand position as you do 
for drawing, move your thumb and index finger over the area you want to erase. It will erase a 100x100 pixel area around that point and turn 
it back to black.
![erasing_smaller](https://github.com/rgillis873/COMP4102-Project/assets/59716448/7d2d8e87-db32-4e87-9484-ba94a6452b3c)

Shape Detection:
To enter shape detection mode, press the shape button. The blackboard image will then change to have yellow bounding boxes drawn around any 
triangles, circles or sticker images that are detected on the blackboard image. The shapes and stickers will also have a label to show 
what they have been identified as.
![shapes_smaller](https://github.com/rgillis873/COMP4102-Project/assets/59716448/2aee9172-e5c2-4c1e-938b-67a80e3eb6df)
