import cv2 
import numpy as np
from typing import Tuple 
from drawings import Drawings
from rotation import Rotation
from translation import Translation
from hard_coded_face_coords import HardCodedCoords

def image_resize(image: np.ndarray, height: int = 400) -> np.ndarray:
    
    h, w, _ = image.shape
    r = height / h 
    width = int(r * w)    
    resized_image = cv2.resize(image, (width, height))
    
    return resized_image

def get_face_coords() -> Tuple[tuple, tuple]:
    
    ob = HardCodedCoords()
    return ob.get_face_coords() 

def get_eye_coords() -> Tuple[tuple, tuple]:
    
    ob = HardCodedCoords()
    return ob.get_eye_coords()

def crop_face(top_left: tuple, bottom_right: tuple, image: np.ndarray) -> np.ndarray:  
    
    face_crop = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    return face_crop

def rotate_points(rotational_matrix, coord):
    
    coords = np.array([[coord[0]],[coord[1]],[1]]) 
    rotated_coords = np.matmul(rotational_matrix, coords)
    return (int(rotated_coords[0]), int(rotated_coords[1]))

if __name__ == "__main__":
    
    rot_ob = Rotation()
    drawing_ob = Drawings() 
    translation_ob = Translation()
    image = cv2.imread("images/joker.jpeg")
    
    # resizing while maintaining the aspect ratio 
    resized_image = image_resize(image)
        
    rotated_without_bounds, \
    rotated_bounds, \
    _ = rot_ob.rotate_the_image(resized_image, 90, 1.0)
    
    top_left, bottom_right = get_face_coords() 
    
    face_crop = crop_face(top_left, bottom_right, rotated_bounds)
    
    left_eye, right_eye = get_eye_coords() 
    drawing_ob.compare_post_rotaion(rotated_without_bounds, rotated_bounds.copy())
    drawing_ob.show_key_points(left_eye, right_eye, face_crop.copy())
    
    left_eye = translation_ob.translate_coords(top_left, left_eye)
    right_eye = translation_ob.translate_coords(top_left, right_eye)
    
    drawing_ob.show_key_points(left_eye, right_eye, rotated_bounds.copy())
    
    _, orig_rotated_bounds, rotational_matrix = rot_ob.rotate_the_image(rotated_bounds.copy(), -90, 1.0)
    
    left_eye_rotated = rotate_points(rotational_matrix, left_eye)
    right_eye_rotated = rotate_points(rotational_matrix, right_eye)
    
    drawing_ob.show_key_points(left_eye_rotated, right_eye_rotated, orig_rotated_bounds.copy())
    
    
    