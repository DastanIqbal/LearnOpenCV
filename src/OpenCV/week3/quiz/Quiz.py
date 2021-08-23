import cv2
import matplotlib.pyplot as plt
import numpy as np

DATA_PATH = "/src/res/opencv-courses/"

# im = cv2.imread(DATA_PATH+"images/opening.png",cv2.IMREAD_GRAYSCALE)
# cv2.imshow("Q1",im)

imageRGB = np.zeros((300,300,3),dtype="uint8")
print(np.shape)

imageRGB[150:300]=255

# imageRGB = cv2.cvtColor(imageRGB, cv2.COLOR_BGR2RGB)
# Add 200 to image
# imageRGB = cv2.add(imageRGB,200)

# plt.imshow(imageRGB)
# plt.show()

cv2.imshow("Q1",imageRGB)
# dst=cv2.threshold(im,127,255,cv2.THRESH_BINARY)

k = cv2.waitKey(1000*1)
# print(k)
cv2.destroyAllWindows()
# if k == 32:
#     print("Space key pressed")