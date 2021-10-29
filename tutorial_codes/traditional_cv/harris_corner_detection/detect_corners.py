
import cv2
import numpy as np  

filenames = ["desk_corner_1.jpeg", "desk_corner_2.jpeg", "desk_corner_3.jpeg"]

for filename in filenames:

    # Reading the image
    image = cv2.imread(filename)    
    image = cv2.resize(image, (0, 0), fx = 0.5, fy = 0.5)    
    # Converting the image to grayscale (Need to calculate the gradients)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    # Get the corner response score for each pixel 
    dst = cv2.cornerHarris(gray, blockSize = 15, ksize = 11, k = 0.04)
    # Threshold for an optimal value, it may vary depending on the image.
    image[dst>0.01*dst.max()]=[0,0,255]
    # save the image
    new_filename = filename.split(".")[0] + "_harris_corner.jpeg"
    cv2.imwrite(new_filename, image)