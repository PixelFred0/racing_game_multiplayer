import pygame
import sys
from socket import *
conn = socket(AF_INET, SOCK_STREAM)
ip_Adresse = "Example..."  #Ziel IP-Adresse
port = 56789                  #Ziel Port-Nr. 
conn.connect((ip_Adresse, port))

###############################################

test1 = "client nachricht"
conn.send(test1.encode())
verrify = conn.recv(2048).decode()
print(verrify)

car_name = "Name von dem Auto" # Der Name des Autos/Datei
conn.send(bytes(str(car_name), 'utf8'))
print("Send")

###############################################

pygame.init() # startet pygame
screen = pygame.display.set_mode((300,100)) # Breite | Höhe
pygame.display.set_caption("11a Racing")# name oben im Fenster
clock = pygame.time.Clock()

###############################################

text_font = pygame.font.Font("c:/.../racing_game_multiplayer/fonts/digital-7.ttf", 50) # Font, Schriftgröße

richtung = "keine"

###############################################

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit(0)
    
    screen.fill((0,0,0)) # malt den Hintergrund an
    text = text_font.render(richtung, False, (255,255,255) )   
    screen.blit(text, (10,25)) # ein neuer Screen über dem anderen an x,y Position, letzter blit oben
    

    press = pygame.key.get_pressed()
    
    if press[pygame.K_a]: # lenken
        richtung = "a"
        conn.send(bytes(str(richtung), 'utf8'))
    if press[pygame.K_d]: 
        richtung = "d"
        conn.send(bytes(str(richtung), 'utf8'))  
    if press[pygame.K_w]: # beschleinigen
        richtung = "w"
        conn.send(bytes(str(richtung), 'utf8'))
    if press[pygame.K_s]: # bremsen
        richtung = "s"
        conn.send(bytes(str(richtung), 'utf8'))  
    if not press[pygame.K_s] and not press[pygame.K_w]:
        richtung = "n"
        conn.send(bytes(str(richtung), 'utf8'))


     
    pygame.display.update()
    clock.tick(60)