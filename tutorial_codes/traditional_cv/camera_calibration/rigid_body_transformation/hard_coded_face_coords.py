from typing import Tuple

class HardCodedCoords:
    
    def get_face_coords(self) -> Tuple[tuple, tuple] :
        
        top_left = (97,34)
        bottom_right = (203,173)
        return top_left, bottom_right
    
    def get_eye_coords(self) -> Tuple[tuple, tuple] :
        
        left_eye = (24, 62)
        right_eye = (60, 60)         
        return left_eye, right_eye