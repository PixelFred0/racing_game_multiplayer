import random
import time
from socket import *
from threading import Thread
import pygame
from bewegung import *
import sys
import numpy as np

fps = 60
sand = (198,166,100)

all_spd = [] # Geschwindkeiten aller Spieler
all_angle = [] # Winkel aller Spieler
all_x = [] # X aller Spieler 
all_y = [] # Y aller Spieler 
maxspd = 3
minspd = -1.5
accel = 0.05
anglespd = 10
f = 0 # index für all_Listen im changer und move
car_list = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17] # Liste der ausgewählten Autos in Reihenfolge der Clients
car_choice = [] #  Autowahl
car_counter = 0 # index für car_list in der Auto zuweisung
conn = [] # connliste aller Clients
addr = [] # addrliste aller clients
Player = int(input("Wie viele Spieler: ")) # Spieleranzahl
all_threads= []
bounce = 0.5
all_player_car_mask = []
all_counter = []
all_runde = []
track_boarder_mask = None
finish_line_mask = None
checkpoint_1_mask = None
checkpoint_2_mask = None
client_names = []
won = False

def listenextend(): # Fügt für jeden neuen Spieler einen Platzhalter als "0" ein
  all_x.append(250)
  all_y.append(150)
  all_angle.append(0)
  all_spd.append(0)
  all_counter.append(0)
  all_runde.append(0)


def string_converter(conn): # Wandelt die Auto Auswahl in ein Integr um
  data = conn.recv(1024) 
  strings = str(data, 'utf8') # decode to unicode string
  car_number = int(strings)
  return car_number

def client_creator(): # Verbindet die Clients und speichert dessen conn und addr
  while True:
    global conn
    global addr
    global car_choice
    conn_current, addr_current = server.accept()
    conn.append(conn_current)
    addr.append(addr_current)
    print("Ich habe eine Verbindung mit dem Client:", addr_current)
    test1 = conn_current.recv(2048).decode()
    print(test1)
    conn_current.send("Du hast dich verbunden.".encode())
    car_number = string_converter(conn_current)
    print("Car Number recieved")
    car_choice.append(car_number)
    listenextend()

def conn_closer(): # Schließt alle Verbindungen
  for i in range(len(conn)):
    conn[i].close()

def collision(f):
  if track_boarder_mask.overlap(all_player_car_mask[f], (all_x[f],all_y[f])) != None:
      if all_spd[f] > 0:
        all_spd[f] = -(bounce * abs(all_spd[f]))
      else: #all_spd[f] < 0:
        all_spd[f] = bounce * abs(all_spd[f])
  if checkpoint_1_mask.overlap(all_player_car_mask[f], (all_x[f],all_y[f])) != None:
      if all_counter[f] == 0:
          all_counter[f] = 1
          print("counter1 passed")
  if checkpoint_2_mask.overlap(all_player_car_mask[f], (all_x[f],all_y[f])) != None:
      if all_counter[f] == 1:
          all_counter[f] = 2
          print("counter2 passed")
  if finish_line_mask.overlap(all_player_car_mask[f], (all_x[f],all_y[f])) != None: #Die Maske der boarder wird auf 
      if all_counter[f] == 2:
          all_runde[f] = all_runde[f] +1
          print(f"Runde: {all_runde[f]}")
          all_counter[f] = 0

def changer(conn, addr,f): # Änderung des Spielers[f] Variablen
  while True:
    all_spd[f] = np.round_(all_spd[f], decimals=2)
    data = conn.recv(1024)
    message = str(data, 'utf8')
    if "w" in message:
      if all_spd[f] < maxspd:
        all_spd[f] = all_spd[f] + accel
    if "s" in message:
      if all_spd[f] > minspd:
        all_spd[f] = all_spd[f] - accel
    if "a" in message:
      if all_spd[f] != 0:
        all_angle[f] = all_angle[f] + anglespd
    if "d" in message:
      if all_spd[f] != 0:
        all_angle[f] = all_angle[f] - anglespd
    if "n" in message:
      if all_spd[f] > 0:
        all_spd[f] = all_spd[f] - accel
      elif all_spd[f] < 0:
        all_spd[f] =  all_spd[f] + accel
    collision(f)

def track_picker(): # Rennstrecken Wähler
  global track
  global track_boarder_mask
  global pick
  global finish_line
  global finish_line_mask
  global checkpoint_1_mask
  global checkpoint_2_mask
  track0 = pygame.image.load("c:/.../racing_game_multiplayer/graphics/track_0/track.png").convert_alpha()
  track_boarder0 =  pygame.image.load("c:/.../racing_game_multiplayer/graphics/track_0/track_boarder.png").convert_alpha()# Bild zur Maske wird geladen
  track_boarder_mask0 = pygame.mask.from_surface(track_boarder0)#maske wird erzeugt
  finish_line0 =  pygame.image.load("c:/.../racing_game_multiplayer/graphics/track_0/finish_line.png").convert_alpha()# Bild zur Maske wird geladen
  finish_line_mask0 = pygame.mask.from_surface(finish_line0)#maske wird erzeugt
  checkpoint_1_0 =  pygame.image.load("c:/.../racing_game_multiplayer/graphics/track_0/checkpoint_1.png").convert_alpha()# Bild zur Maske wird geladen
  checkpoint_1_mask_0 = pygame.mask.from_surface(checkpoint_1_0)#maske wird erzeugt
  checkpoint_2_0 =  pygame.image.load("c:/.../racing_game_multiplayer/graphics/track_0/checkpoint_2.png").convert_alpha()# Bild zur Maske wird geladen
  checkpoint_2_mask_0 = pygame.mask.from_surface(checkpoint_2_0)#maske wird erzeugt

  track1 = pygame.image.load("c:/.../racing_game_multiplayer/graphics/track_1/track.png").convert_alpha()
  track_boarder1 =  pygame.image.load("c:/.../racing_game_multiplayer/graphics/track_1/track_boarder.png").convert_alpha()# Bild zur Maske wird geladen
  track_boarder_mask1 = pygame.mask.from_surface(track_boarder1)#maske wird erzeugt
  finish_line1 =  pygame.image.load("c:/.../racing_game_multiplayer/graphics/track_1/finish_line.png").convert_alpha()# Bild zur Maske wird geladen
  finish_line_mask1 = pygame.mask.from_surface(finish_line1)#maske wird erzeugt
  checkpoint_1_1 =  pygame.image.load("c:/.../racing_game_multiplayer/graphics/track_1/checkpoint_1.png").convert_alpha()# Bild zur Maske wird geladen
  checkpoint_1_mask_1 = pygame.mask.from_surface(checkpoint_1_1)#maske wird erzeugt
  checkpoint_2_1 =  pygame.image.load("c:/.../racing_game_multiplayer/graphics/track_1/checkpoint_2.png").convert_alpha()# Bild zur Maske wird geladen
  checkpoint_2_mask_1 = pygame.mask.from_surface(checkpoint_2_1)#maske wird erzeugt

  track2 = pygame.image.load("c:/.../racing_game_multiplayer/graphics/track_2/track.png").convert_alpha()
  track_boarder2 =  pygame.image.load("c:/.../racing_game_multiplayer/graphics/track_2/track_boarder.png").convert_alpha()# Bild zur Maske wird geladen
  track_boarder_mask2 = pygame.mask.from_surface(track_boarder2)#maske wird erzeugt
  finish_line2 =  pygame.image.load("c:/.../racing_game_multiplayer/graphics/track_2/finish_line.png").convert_alpha()# Bild zur Maske wird geladen
  finish_line_mask2 = pygame.mask.from_surface(finish_line2)#maske wird erzeugt
  checkpoint_1_2 =  pygame.image.load("c:/.../racing_game_multiplayer/graphics/track_2/checkpoint_1.png").convert_alpha()# Bild zur Maske wird geladen
  checkpoint_1_mask_2 = pygame.mask.from_surface(checkpoint_1_2)#maske wird erzeugt
  checkpoint_2_2 =  pygame.image.load("c:/.../racing_game_multiplayer/graphics/track_2/checkpoint_2.png").convert_alpha()# Bild zur Maske wird geladen
  checkpoint_2_mask_2 = pygame.mask.from_surface(checkpoint_2_2)#maske wird erzeugt

  all_track = [track0, track1, track2]
  all_track_boarder_mask = [track_boarder_mask0,track_boarder_mask1,track_boarder_mask2]
  all_finish_line = [finish_line0,finish_line1,finish_line2,]
  all_finish_line_mask = [finish_line_mask0,finish_line_mask1,finish_line_mask2]
  all_checkpoint_mask_1 = [checkpoint_1_mask_0,checkpoint_1_mask_1,checkpoint_1_mask_2]
  all_checkpoint_mask_2 = [checkpoint_2_mask_0,checkpoint_2_mask_1,checkpoint_2_mask_2]
  pick = 0 #random.randint(0,2)
  track = all_track[pick]
  track_boarder_mask = all_track_boarder_mask[pick]
  finish_line = all_finish_line[pick]
  finish_line_mask = all_finish_line_mask[pick]
  checkpoint_1_mask = all_checkpoint_mask_1[pick]
  checkpoint_2_mask = all_checkpoint_mask_2[pick]

def gamestate():
  global won
  for x in all_runde:
    if x == 2:
      won = True
      winner = x
  if won:
    winner_name = client_names[x]
    winner_text = (f"Der Gewinner ist {winner_name}")
    text_font = pygame.font.Font("c:/path/to/the/fonts/digital-7.ttf", 50)
    text = text_font.render(winner_text, False, (255,255,255) )   
    screen.blit(text, (10,25))



server = socket(AF_INET, SOCK_STREAM)
print("Socket wurde erstellt")

servername = gethostname() # Der Name des Servers
print("Servername:", servername)
ip_Addresse = gethostbyname(servername) # Die IP-Adresse des SAervers
print("IP Address:", ip_Addresse)
port = 56789
print("Port-Nr.:", port)

server.bind((ip_Addresse, port)) # erstes IP-Adresse ist leer, damit alle IP-Adressen akzeptiert werden
server.listen(Player) # maximale Teilnehmer Zahl
print(f"Der Server wartet auf {Player} Teilnehmer")

conn_current, addr_current = server.accept() # Verbindung zum 1. Client
conn.append(conn_current)
addr.append(addr_current)
print("Ich habe eine Verbindung mit dem Client:", addr[0])
test1 = conn[0].recv(2048).decode()
print(test1)
conn[0].send("Du hast dich verbunden.".encode())
car_number = string_converter(conn[0])
print("Car Number0 recieved")
car_choice.append(car_number)
listenextend()

client_t = Thread(target= client_creator) # Thread für den Client_Creator

if not client_t.is_alive():
  client_t.start() # startet client_creator

pygame.init() # startet pygame
screen = pygame.display.set_mode((1200,800)) # Breite | Höhe, des Fensters
pygame.display.set_caption("11a Racing")     # name oben im Fenster
clock = pygame.time.Clock()                  # Startet eine Uhr, sodass die Frames angepasst werden können.

player_car0 = pygame.image.load("c:/.../racing_game_multiplayer/graphics/car_0.png").convert_alpha()
player_car_mask0 = pygame.mask.from_surface(player_car0)
player_car1 = pygame.image.load("c:/.../racing_game_multiplayer/graphics/car_1.png").convert_alpha()
player_car_mask1 = pygame.mask.from_surface(player_car1)
player_car2 = pygame.image.load("c:/.../racing_game_multiplayer/graphics/car_2.png").convert_alpha()
player_car_mask2 = pygame.mask.from_surface(player_car2)
player_car3 = pygame.image.load("c:/.../racing_game_multiplayer/graphics/car_freddy.png").convert_alpha()
player_car_mask3 = pygame.mask.from_surface(player_car3)
player_car4 = pygame.image.load("c:/.../racing_game_multiplayer/graphics/car_bjarne.png").convert_alpha()
player_car_mask4 = pygame.mask.from_surface(player_car4)
player_car5 = pygame.image.load("c:/.../racing_game_multiplayer/graphics/lambo.png").convert_alpha()
player_car_mask5 = pygame.mask.from_surface(player_car5)
player_car6 = pygame.image.load("c:/.../racing_game_multiplayer/graphics/car_erik.png").convert_alpha()
player_car_mask6 = pygame.mask.from_surface(player_car6)
player_car7 = pygame.image.load("c:/.../racing_game_multiplayer/car_lambo_rot.png").convert_alpha()
player_car_mask7 = pygame.mask.from_surface(player_car7)
all_player_car = [player_car0, player_car1, player_car2, player_car3, player_car4, player_car5, player_car6, player_car7] # Liste aller verfügbaren Autos
all_player_car_mask = [player_car_mask0,player_car_mask1,player_car_mask2,player_car_mask3,player_car_mask4,player_car_mask5,player_car_mask6,player_car_mask7,]
connected = True
while connected: # Schleife bis alle Spieler verbunen sind
  if len(car_choice) == Player:
    for s in car_choice: # Zuweisung des ausgewählten Autos
      car_list[car_counter] = all_player_car[s] # Ausgewähltes Auto wird in die Liste eingefügt
      car_counter = car_counter + 1 # index für die Liste wird um einen erhöht
    connected = False
  else:
    time.sleep(0.7)
print("alle spieler sind bereit")

track_picker()

thread_counter = 0
threads_done = True
while threads_done: # erzeugt Client Threads
  if thread_counter < Player:
    t = Thread(target=changer, args = (conn[thread_counter], addr[thread_counter],thread_counter)) # Client thread
    if not t.is_alive():
      t.start()
      print("Startet t Thread")
    thread_counter = thread_counter +1
  else:
    threads_done = False


print("startet")
while True:
    # Benden des Programms
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          server.close() # Schließen der sockets
          conn_closer()

          pygame.quit()
          sys.exit()

    screen.fill(sand) # malt den Hintergrund farbig an
    screen.blit(track, (0,0)) # eine neue Schicht über dem anderen an x,y Position, letzter blit oben
    screen.blit(finish_line, (0,0))
    
    
    if not won:
      for f in range(len(all_spd)):
        all_x[f],all_y[f] = move(all_x[f],all_y[f],all_spd[f],all_angle[f])
        blit_rotated_car(screen, car_list[f] , (all_x[f],all_y[f]), all_angle[f])
    
    gamestate()
    pygame.display.update()
    clock.tick(fps) # wartet 1/fps Sekunden