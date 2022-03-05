import cv2
import numpy


img = cv2.imread('00-puppy.jpg')

scale_percent = 40      # percent of original file
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)

# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

print('Resized Dimensions : ',resized.shape)

while True:
    cv2.imshow('Mywindow', resized)
    
    # IF we waited for 1ms AND pressed the Esc key
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
