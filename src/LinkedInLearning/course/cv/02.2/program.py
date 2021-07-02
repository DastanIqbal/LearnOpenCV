import numpy as np
import cv2

img = cv2.imread("../../../../res/opencv.png", 1)  # 1 BGR is a default color value of image

print("*****Show image color(BGR) channel One data*****")
print(img)  # Print image data in array and type

print("\n*****Image data type*****")
print(type(img))  # Print image type

print("\n*****Number of rows in Image*****")
print(len(img))  # Length of Image, number of rows in array

print("\n*****Number of vertical column on top row in Image*****")
print(len(img[0]))  # top row, vertical column

print("\n*****Number of color channel in Image*****")
print(len(img[0][0]))  # no of channel

print("\n*****Get all the row,column and color channel from Image*****")
print(img.shape)  # print number of row,col and channel

print("\n*****Image data type*****")
print(img.dtype)  # data type of image, uint8 means max 2 pow 8 value possible in array of index

print("\n*****Get pixel value at 10th row and 5th column from Image*****")
print(img[10, 5])  # 10 row 5 th col , will get pixel value

print("\n*****Get one channel of Image*****")
print(img[:, :, 0])  # one channel image

print("\n*****Total number of row x column in Image*****")
print(img.size)  # total number of column
