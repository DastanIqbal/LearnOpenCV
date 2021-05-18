import numpy as np
import cv2

#Intialize array with 0 value
black = np.zeros([150, 200, 1], 'uint8')
cv2.imshow("Black", black)
print(black[0, 0, :])

cv2.waitKey(0)


#Intialize array with ones value
ones = np.ones([150, 200, 3], 'uint8')
cv2.imshow("Ones", ones)
print(ones[0, 0, :])

cv2.waitKey(0)

#Intialize array with ones and fill with max value
white = np.ones([150, 200, 3], 'uint8')
#white *= (2**8-1)
white[:, :] = (255, 255, 255)
cv2.imshow("White", white)
print(white[0, 0, :])

cv2.waitKey(0)

#Intalize array with blue color
color = ones.copy() #Deap copy
color[:, :] = (0, 255, 0)
cv2.imshow("Green", color)

cv2.waitKey(0)

cv2.destroyAllWindows()
