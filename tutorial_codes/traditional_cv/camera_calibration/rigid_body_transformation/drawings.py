import cv2 
import numpy as np 

class Drawings:
    
    def compare_post_rotaion(self, 
                             rotated_without_bounds: np.ndarray, 
                             rotated_with_bounds: np.ndarray) -> None:
        
        win_name = "rotated_without_bounds"
        cv2.namedWindow(win_name) 
        cv2.moveWindow(win_name, 40, 30)
        cv2.imshow(win_name, rotated_without_bounds)
        win_name = "rotated_with_bounds"
        cv2.imshow(win_name, rotated_with_bounds)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
    
    def show_key_points(self, 
                        left_eye: tuple, 
                        right_eye: tuple, 
                        image: np.ndarray) -> None:
        
        cv2.circle(image, left_eye, 2, (0, 255, 255), 2) 
        cv2.circle(image, right_eye, 2, (0, 255, 255), 2) 
        cv2.imshow("eye coords", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()        