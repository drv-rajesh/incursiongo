import pygame
import math

def getRotatedImage(image, rect, angle):
    new_image = pygame.transform.rotate(image, angle)
    new_rect = new_image.get_rect(center=rect.center)
    return new_image, new_rect

def angleBetweenPoints(x1, y1, x2, y2):
    x_difference = x2 - x1
    y_difference = y2 - y1
    angle = math.degrees(math.atan2(-y_difference, x_difference))
    return angle

def centeringCoords(pict, screen):
    new_x = screen.get_width()/2 - pict.get_width()/2
    new_y = screen.get_height()/2 - pict.get_height()/2
    return new_x, new_y

