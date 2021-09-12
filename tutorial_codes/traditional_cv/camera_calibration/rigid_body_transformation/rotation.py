
from typing import Tuple
import cv2 
import numpy as np 

class Rotation:
    
    def __get_rotational_matrix(self, center: Tuple[int, int], angle: float, scale_factor: float):
        
        """
        Rotates the image without cropping. 
        :param image: Image to be rotated. 
        :param angle: The angle by which image has to be rotated. 
        :param scale_factor: To scale the rotated image by a factor.  
        """
        R = cv2.getRotationMatrix2D(center, angle = angle, scale = scale_factor)         
        return R
    
    def __warped_image(self, R, image, dsize):
        
        """
        Performs affine transformation between the rotation matrix and image to
        get the new rotated image.  
        :param R: Rotational matrix to be used to rotate the image. 
        :param image: Image to be rotated. 
        :param dsize: Size of the output image.   
        """        
        
        return cv2.warpAffine(image, R, dsize=dsize)
    
    def __just_rotate(self, image: np.ndarray, angle: float, scale_factor: float) -> np.ndarray:
        
        """
        Rotates the image without worrying about the image to go out of bounds. 
        :param image: Image to be rotated. 
        :param angle: The angle by which image has to be rotated. 
        :param scale_factor: To scale the rotated image by a factor.
        """
        
        (rows, cols) = image.shape[:2]
        R = cv2.getRotationMatrix2D((cols // 2, rows // 2), angle = angle, scale = scale_factor)         
        rotated_image = cv2.warpAffine(image, R, (cols, rows))
        return rotated_image 
    
    def __rotate_and_reposition(self, image: np.ndarray, angle: float, scale_factor: float) -> Tuple[np.ndarray, np.ndarray]:
        
        """
        Rotates the image without cropping. 
        :param image: Image to be rotated. 
        :param angle: The angle by which image has to be rotated. 
        :param scale_factor: To scale the rotated image by a factor.  
        """
        (old_rows, old_cols) = image.shape[:2] 
        
        # Old center coordinates of the image before rotation. 
        old_center_x = old_cols // 2
        old_center_y = old_rows // 2
        
        # Generate the rotational matrix for given parameters. 
        R = self.__get_rotational_matrix((old_center_x, old_center_y), angle, scale_factor)
        
        # Calculate the new bounding image dimensions using the sin and 
        # cos components of the rotational matrix. 
        new_rows, new_cols = old_rows * scale_factor, old_cols * scale_factor        
        cos = np.abs(R[0, 0])
        sin = np.abs(R[0, 1])
        new_rows = abs(old_rows * cos) + abs(old_cols * sin)
        new_cols = abs(old_rows * sin) + abs(old_cols * cos)
        
        # new center coordinates of the image. 
        new_center_x = new_cols / 2
        new_center_y = new_rows / 2
        
        # After computing the new bounding dimension's the centers of the images  
        # will not be aligned any more. So, to account that translation of centers 
        # we add the different in the translation matrix. 
        R[0, 2] += (new_center_x - old_center_x)
        R[1, 2] += (new_center_y - old_center_y)
        
        # Perform Affine Transformation on the image using the transformation matrix 'R'  
        # with new image dimensions such that no part of the image is cropped out.
        rotated_image = self.__warped_image(R, image, (int(new_cols), int(new_rows)))
        
        return rotated_image, R
    
    def rotate_the_image(self, image: np.ndarray, angle: float, scale_factor: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Rotates the image without cropping. 
        :param image: Image to be rotated. 
        :param angle: The angle by which image has to be rotated. 
        :param scale_factor: To scale the rotated image by a factor.  
        """        
        cv2.imshow('img', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        rotated_without_bounds = self.__just_rotate(image.copy(), angle, scale_factor)
        rotated_with_bounds, R = self.__rotate_and_reposition(image.copy(), angle, scale_factor)
        
        return rotated_without_bounds, rotated_with_bounds, R 