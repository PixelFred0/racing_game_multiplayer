import pygame
import math


def blit_rotated_car(screen, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle) # Drehen des Bildes - um die Ecke oben links
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = top_left).center) # Anpassen des Rechteckes um das Bild, sodass es um seinen Mittelpunkt gedreht wird

    screen.blit(rotated_image, new_rect.topleft) # Zeichnet das gedrehte Bild auf dem Bildschirm

def move(x_pos,y_pos,spd,angle):
    radians = math.radians(angle) # Grad in Rad umwandeln
    vert = math.cos(radians) * spd # Änderung in der Vertikalen
    hori = math.sin(radians) * spd # Änderung in der Horizontalen

    x_pos = x_pos - vert # neue x-Position
    y_pos = y_pos + hori # neue y-Position

    return (x_pos,y_pos) # Rückgabe der neuen Positionen



