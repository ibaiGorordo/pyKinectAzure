import cv2
import numpy as np
from typing import List
from model.Joint import Joint
from model.joint2D import Joint2D


class Drawer:

    blue_color = (255, 0, 0)
    red_color = (0, 0, 255)
    white_color = (255, 255, 255)
    green_color = (0, 255, 0)

    def __init__(self):
        pass

    @staticmethod
    def draw_circle_on_image(image: np.ndarray, joint_list: List[Joint2D]) -> np.ndarray:
        for joint in joint_list:
            image = cv2.circle(image, (int(joint.x), int(joint.y)), 3, Drawer.red_color, 3)

        return image

    @staticmethod
    def draw_skeleton_on_image(image: np.ndarray) -> np.ndarray:

        pass

