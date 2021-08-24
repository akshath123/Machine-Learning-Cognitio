
import cv2 
import numpy as np 

class Translation:
    
    def translate_coords(self, top_left: tuple, eye_coord: tuple) -> tuple:
        
        translated_eye_coord = (eye_coord[0] + top_left[0], eye_coord[1] + top_left[1])
        return translated_eye_coord
