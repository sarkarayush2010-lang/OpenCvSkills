#this was actually pretty short to make
# 
#
# import cv2, numpy as np
# image=cv2.imread("logo1.png")
# cv2.imshow("image",image)
# cv2.waitKey()
# cv2.destroyAllWindows()

# image=cv2.imread("logo1.png")
# print(image)

# image=cv2.imread("logo1.png")
# image=cv2.resize(image,(640,480))
# cv2.imshow("resized",image)
# cv2.waitKey()
# cv2.destroyAllWindows()


# image=cv2.imread("logo1.png")
# image=cv2.resize(image,(640,480))
# greyimage=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# print(greyimage)
# cv2.imshow("resized",image)
# cv2.imshow("grey",greyimage)
# cv2.waitKey()
# cv2.destroyAllWindows()


# image=cv2.imread("myphoto.jpg")
# image=cv2.resize(image,(1600,900))
# greyimage=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# threshold,blackandwhiteimage=cv2.threshold(greyimage,150,255,cv2.THRESH_BINARY)
# cv2.imshow("resized",image)
# cv2.imshow("bandw", blackandwhiteimage)
# cv2.imshow("grey",greyimage)
# cv2.waitKey()
# cv2.destroyAllWindows()

#try eroding,dialating,invert,drawing shapes,putting text,

#eroding
# img=cv2.imread("myphoto.jpg")
# img = cv2.resize(img, (320,180))
# kernel = np.ones((5,5))
# print (kernel)
# eroded_img= cv2.erode(img, (kernel))
# cv2.imshow("OpenCV Window", img)
# cv2.imshow("OpenCV Erode Image", eroded_img)
# cv2.waitKey()
# cv2.destroyAllWindows()


#dialating

# img=cv2.imread("myphoto.jpg")
# img = cv2.resize(img, (320,180))
# kernel = np.ones((5,5))
# print (kernel)
# dialated_img= cv2.dilate(img, (kernel))
# cv2.imshow("OpenCV Window", img)
# cv2.imshow("OpenCV Erode Image", dialated_img)
# cv2.waitKey()
# cv2.destroyAllWindows()


#inverting
# image=cv2.imread("logo1.jpg")
# image=cv2.resize(image,(600,480))
# greyimage=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# threshold,blackandwhiteimage=cv2.threshold(greyimage,150,255,cv2.THRESH_BINARY)
# blackandwhiteimage=cv2.bitwise_not(blackandwhiteimage)
# cv2.imshow("bandw", blackandwhiteimage)
# cv2.waitKey()
# cv2.destroyAllWindows()

#drawing shapes
# image=cv2.imread("myphoto.jpg")
# image=cv2.resize(image,(1600,900))
# cv2.rectangle(image, (20, 20), (150, 120), (0,255,0), 3)
# cv2.line(image, (20, 460), (150, 360), (0,255,0), 3)
# cv2.circle(image, (600, 70), 50, (0,255,0), 3)
# cv2.imshow("resized",image)
# cv2.waitKey()
# cv2.destroyAllWindows()
#text
# image=cv2.imread("myphoto.jpg")
# image=cv2.resize(image,(1600,900))
# cv2.putText(image,"hello world", (400,500), cv2.FONT_HERSHEY_DUPLEX, 2, (0,255,0), 4)
# cv2.imshow("resized",image)
# cv2.waitKey()
# cv2.destroyAllWindows()

# image=cv2.imread("numbers.jpeg")
# image=cv2.resize(image,(450,800))
# greyimage=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# threshold,blackandwhiteimage=cv2.threshold(greyimage,80,255,cv2.THRESH_BINARY_INV)
# contours,hirearchy=cv2.findContours(blackandwhiteimage.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(image, contours, -1, (0,255,150),3)
# for cntr in contours:
#     boxCoordinates=cv2.boundingRect(cntr)
#     print(boxCoordinates)
#     cv2.rectangle(image, (boxCoordinates[0]-20, boxCoordinates[1]-20), (boxCoordinates[0]+boxCoordinates[2]+20,boxCoordinates[1]+ boxCoordinates[3]+20), (0,255,0), 3)

# cv2.imshow("normal", image)
# cv2.imshow("grey", greyimage)
# cv2.imshow("black", blackandwhiteimage)
# cv2.waitKey()
# cv2.destroyAllWindows()

# import cv2
# camera=cv2.VideoCapture(1)
# while camera.isOpened():
#     ret,frame=camera.read()
#     if ret:
#         cv2.imshow('video', frame)
#         if cv2.waitKey(1) & 0xFF==ord("q"):
#             break
# camera.release()
# cv2.destroyAllWindows()


# import cv2
# camera=cv2.VideoCapture(1)

# while camera.isOpened():
#     ret,frame=camera.read()
#     greyframe=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#     threshold,blackframe=cv2.threshold(greyframe,80,255,cv2.THRESH_BINARY_INV)
#     if ret:
#         cv2.imshow('video', frame)
#         cv2.imshow('greyvideo',greyframe)
#         cv2.imshow('blackvideo',blackframe)

#         if cv2.waitKey(1) & 0xFF==ord("q"):
#             break
# camera.release()
# cv2.destroyAllWindows()

# import cv2
# camera=cv2.VideoCapture(1)
# while camera.isOpened():
#     ret,frame=camera.read()
#     if ret:
#         roi = frame[0:480, 0:320]
#         cv2.imshow('video', frame)
#         cv2.imshow('roi', roi)
#         if cv2.waitKey(1) & 0xFF==ord("q"):
#             break
# camera.release()
# cv2.destroyAllWindows()



# import cv2
# camera=cv2.VideoCapture(1)
# while camera.isOpened():
#     ret,frame=camera.read()
#     if ret:
#         frame[0:480, 0:320]=(0,0,255)
#         cv2.imshow('video', frame)
#         if cv2.waitKey(1) & 0xFF==ord("q"):
#             break
# camera.release()
# cv2.destroyAllWindows()


import cv2
camera=cv2.VideoCapture(1)
while camera.isOpened():
    ret,frame=camera.read()
    if ret:
        frame[0:480, 0:320]=cv2.flip(frame[0:480, 320:640],1)
        cv2.imshow('video', frame)
        if cv2.waitKey(1) & 0xFF==ord("q"):
            break
camera.release()
cv2.destroyAllWindows()

#make line filter social media top to bottom
#whatever behind the line stays fixed
#can not use for loop and no other while loop

#version 1
'''
import cv2
import numpy as np

camera=cv2.VideoCapture(0)
liney=0
speed=4
canvas=None
while camera.isOpened():
    ret,frame=camera.read()
    if ret:
        if canvas is None:
            canvas=frame.copy()
        
        canvas[liney:liney+speed, :] = frame[liney:liney+speed, :]
        display_frame=canvas.copy()
        cv2.line(display_frame, (0, liney), (frame.shape[1], liney),(255,0,0),2)
        cv2.imshow('video', display_frame)
        liney+=speed
        if liney>=frame.shape[0]:
            liney=0
            canvas=frame.copy()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
camera.release()
cv2.destroyAllWindows()
'''
#sorry i kinda ran out of time but i did the above thing by myself (the rest may or may not be with ai help) but that counts right?

import cv2
import numpy as np
camera=cv2.VideoCapture(0, cv2.CAP_DSHOW)
liney=0
speed=4
canvas=None

while camera.isOpened():
    ret,frame=camera.read()
    if ret:
        if canvas is None:
            canvas=frame.copy()
        canvas[liney:liney+speed,:]=frame[liney:liney+speed,:]
        display_frame=frame.copy()
        if liney>0:
            display_frame[0:liney,:]=canvas[0:liney,:]
        cv2.line(display_frame, (0,liney),(frame.shape[1],liney), (255,50,50), 2)
        cv2.imshow('filter', display_frame)
        liney+=speed
        if liney>=frame.shape[0]:
            liney=0
            canvas=frame.copy()
        if cv2.waitKey(1)& 0xFF == ord("q"):
            break
camera.release()
cv2.destroyAllWindows()