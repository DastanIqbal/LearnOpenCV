import numpy as np
import cv2

#Read opencv.png logo file from local
img = cv2.imread("./../res/opencv.png") 

#Create Window
cv2.namedWindow("Logo",cv2.WINDOW_NORMAL)

#Show local opencv.png in window
cv2.imshow("Logo",img)

#Wait user key press
cv2.waitKey(0)

#Deep copy the opencv.png to output.png in local
cv2.imwrite("output.jpg",img)
exit()
