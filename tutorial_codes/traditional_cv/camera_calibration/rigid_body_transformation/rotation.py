
from typing import Tuple
import cv2 
import numpy as np 

class Rotation:
    
    def __get_rotational_matrix(self, center, angle, scale_factor):
        
        R = cv2.getRotationMatrix2D(center, angle = angle, scale = scale_factor)         
        return R
    
    def __warped_image(self, R, image, dsize):
                
        return cv2.warpAffine(image, R, dsize=dsize)
    
    def __just_rotate(self, image: np.ndarray, angle: float, scale_factor: float) -> np.ndarray:
        
        (rows, cols) = image.shape[:2]
        R = cv2.getRotationMatrix2D((cols // 2, rows // 2), angle = angle, scale = scale_factor)         
        rotated_image = cv2.warpAffine(image, R, (rows, cols))
        return rotated_image 
    
    def __rotate_and_reposition(self, image: np.ndarray, angle: float, scale_factor: float) -> Tuple[np.ndarray, np.ndarray]:
        
        (old_rows, old_cols) = image.shape[:2] 
        
        old_center_x = old_cols // 2
        old_center_y = old_rows // 2
        
        R = self.__get_rotational_matrix((old_center_x, old_center_y), angle, scale_factor)
        
        new_rows, new_cols = old_rows * scale_factor, old_cols * scale_factor
        
        cos = np.abs(R[0, 0])
        sin = np.abs(R[0, 1])
        new_rows = abs(old_rows * cos) + abs(old_cols * sin)
        new_cols = abs(old_rows * sin) + abs(old_cols * cos)
        
        new_center_x = new_cols / 2
        new_center_y = new_rows / 2
        
        R[0, 2] += (new_center_x - old_center_x)
        R[1, 2] += (new_center_y - old_center_y)
        
        rotated_image = self.__warped_image(R, image, (int(new_cols), int(new_rows)))
        
        return rotated_image, R
    
    def rotate_the_image(self, image: np.ndarray, angle: float, scale_factor: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        
        rotated_without_bounds = self.__just_rotate(image.copy(), angle, scale_factor)
        rotated_with_bounds, R = self.__rotate_and_reposition(image.copy(), angle, scale_factor)
        
        return rotated_without_bounds, rotated_with_bounds, R 