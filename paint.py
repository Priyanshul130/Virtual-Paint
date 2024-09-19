import numpy as np
from tkinter import *

from tkinter.ttk import *
import cv2
from collections import deque

#define the upper and lower and boundrie for a color to be consired blue

lower=np.array([0,102,102])
upper=np.array([102,255,255])


#create the window
frame=Tk()
frame.geometry("500x500")
frame.title("virtual paint")



#setup deque to store seperate colors in seperate arrays
bPoints=[deque()]
gPoints=[deque()]
rPoints=[deque()]
yPoints=[deque()]


bIndex=0#index to blue deque
gIndex=0#index to green deque
rIndex=0#index to red  deque
yIndex=0#index to yellow deque


#colors
blue=(255,0,0)
green=(0,255,0)
red=(0,0,255)
yellow=(0,255,255)
white=(255,255,255)
gray=(150,150,150)


color_index=0
colors=[blue,green,red,yellow]
fontName=cv2.FONT_HERSHEY_SIMPLEX

#setup the paint inter face
paintWindow = np.zeros((471,636,3)) + 255
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

#load the video
cam=cv2.VideoCapture(0)

#define a 5*5 slider erosion and dilation
slider=np.ones((5,5),np.uint8)


#keep looping
while True:
    #grab the corent paint window
    grabbed, frame=cam.read()
    frame=cv2.flip(frame,1)# to flip the camera
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #add the coloring option to the video frame
    frame=cv2.rectangle(frame,(40,1),(140,65),gray,-1)
    frame=cv2.rectangle(frame,(160,1),(255,65),colors[0],-1)#-1 denotes the color rectngle filled by colour
    frame=cv2.rectangle(frame,(275,1),(370,65),colors[1],-1)
    frame=cv2.rectangle(frame,(391,1),(485,65),colors[2],-1)
    frame=cv2.rectangle(frame,(505,1),(600,65),colors[3],-1)
    cv2.putText(frame, "CLEAR ALL", (49, 33), fontName, 0.5, white, 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), fontName, 0.5, white, 2, cv2.LINE_AA)
    cv2.putText(frame, "green", (298, 33), fontName, 0.5, white, 2, cv2.LINE_AA)
    cv2.putText(frame, "red", (420, 33), fontName, 0.5, white, 2, cv2.LINE_AA)
    cv2.putText(frame, "yellow", (520, 33), fontName, 0.5, gray, 2, cv2.LINE_AA)

    #check if we have reache the end of the video frame

    if not grabbed:
        break
    #determine which pixel fall within the gree boundries and then blur the binary image
    greenMask = cv2.inRange(hsv, lower, upper)
    greenMask = cv2.erode(greenMask, slider, iterations=2)
    greenMask = cv2.morphologyEx(greenMask, cv2.MORPH_OPEN, slider)
    greenMask = cv2.dilate(greenMask, slider, iterations=1)

    #find contours in the image
    (cnts,_) = cv2.findContours(greenMask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    centre=None
    if cnts is not None:
        #check to see if any contour will found
        if len(cnts) >0:
            #will assume the contour as 0
            cnt=cnts[0]
            # Get the radius of the enclosing circle around the found contour
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            # Draw the circle around the contour
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            # Get the moments to calculate the center of the contour (in this case Circle)
            M = cv2.moments(cnt)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            #if touching button
            if center[1] <= 65:
                if 40 <= center[0] <= 140:#if touched Clear All button
                    #clear everything
                    bPoints=[deque()]
                    gPoints=[deque()]
                    rPoints=[deque()]
                    yPoints=[deque()]


                    bIndex=0#index to blue deque
                    gIndex=0#index to green deque
                    rIndex=0#index to red  deque
                    yIndex=0


                    paintWindow.fill(255)

                elif 160 <= center[0] <= 255:
                    color_index = 0 # Blue
                    
                elif 275 <= center[0] <= 370:
                    color_index = 1 # Green
                    
                elif 390 <= center[0] <= 485:
                    color_index = 2 # Red
                    
                elif 505 <= center[0] <= 600:
                    color_index = 3 # Yellow


            #add the pixel information to correct deque
            else :
                if color_index == 0:
                    bPoints[bIndex].appendleft(center)
                    
                elif color_index == 1:
                    gPoints[gIndex].appendleft(center)
                    
                elif color_index == 2:
                    rPoints[rIndex].appendleft(center)
                    
                elif color_index == 3:
                    yPoints[yIndex].appendleft(center)

        #draw lines of all the colors
        points=[bPoints,gPoints,rPoints,yPoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                    cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)


    


            

def save():

    cv2.imwrite("your drawing",paintWindow)
    #show the frame and paint window image
    cv2.imshow("tracking",frame)
    cv2.imshow("paint",paintWindow)
    #if the q key is presses stop the loop
    #if cv2.waitKey(1)==ord("q"):
        #return

button=Button(frame,text="save",command=save())
#clean up the camera and close any open window
cam.release()
cv2.destroyAllWindows()

        

    
    

    







