import pygame as pg
import random
import math
import game_objects.player as player
import game_objects.ball as ball
import socket

'''
    fisierul care se ocupa de functionarea serverului
    este necesar ca acesta este rulat inaintea clientului
    serverul va controla intotdeauna playerul 1
'''

#initializare pygame
pg.init()
pg.display.set_caption("Pong")
#creeaza un ecran 700x700
screen = pg.display.set_mode((700, 700))
clock = pg.time.Clock()
running = True
delta_time = 0
stop_timer = 200

player_1 = player.Player(50, (screen.get_height() - player.Player.height ) / 2, screen)
player_2 = player.Player(screen.get_width() - 50 - player.Player.width, (screen.get_height() - player.Player.height ) / 2, screen)
b = ball.Ball(screen.get_width() / 2, screen.get_height() / 2, screen)

#variabile folosite de networking
IP = ""  
PORT = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn, addr = (None, None)

#UI
font = pg.font.Font('freesansbold.ttf', 20)

l1 = font.render('Player1', True, (255, 255, 255), (0, 0, 0))
l1_rect = l1.get_rect()
l1_rect.center = (80 // 2, 20 // 2)

l2 = font.render('Player2', True, (255, 255, 255), (0, 0, 0))
l2_rect = l2.get_rect()
l2_rect.center = (1300 // 2, 20 // 2)

score1 = font.render(str(player_1.score), True, (255, 255, 255), (0, 0, 0))
score1_rect = score1.get_rect()
score1_rect.center = (50 // 2, 80 // 2)

score2 = font.render(str(player_2.score), True, (255, 255, 255), (0, 0, 0))
score2_rect = score2.get_rect()
score2_rect.center = (1350 // 2, 80 // 2)

#se creaza un server cu un ip si un port care poate accepta o conexiune
def accept_connection():
    global conn
    global addr

    s.bind((IP, PORT))
    s.listen()
    conn, addr = s.accept()

#se trimite clientului pozitia playerului 1 si pozitia mingii
def client_io():
    global running

    conn.sendall((str(player_1.x) + "_" + str(player_1.y) + "_" + str(b.x) + "_" + str(b.y)).encode("utf-8"))
    
    try:
        data = conn.recv(1024)

        #serverul primeste de la client pozitia playerului 2
        if data and data != b'':
            decode = data.decode("utf-8")
            pos = decode.split("_")
            player_2.y = float(pos[1])

    except:
        print("Connection closed")
        running = False
        conn.close()
        s.close()
        return

def collision():
    global score1, score1_rect
    global score2, score2_rect
    global player_1, player_2
    global stop_timer
    global b

    b_pos = (b.x, b.y)

    #coliziunea intre playeri si minge
    if b_pos[0] - 5 >= player_1.x and b_pos[0] - 5 <= player_1.x + player_1.width:
        if b_pos[1] + 5 >= player_1.y and b_pos[1] + 5 <= player_1.y + player_1.height or b_pos[1] - 5 >= player_1.y and b_pos[1] - 5 <= player_1.y + player_1.height:
            #se alege un unghi random pentru minge
            angle = random.randint(140, 220)
            angle += 180
            b.speed_x = math.cos(math.radians(angle)) * b.speed 
            b.speed_y = math.sin(math.radians(angle)) * b.speed 
    
    if b_pos[0] + 5 >= player_2.x and b_pos[0] + 5 <= player_2.x + player_2.width:
        if b_pos[1] + 5 >= player_2.y and b_pos[1] + 5 <= player_2.y + player_2.height or b_pos[1] - 5 >= player_2.y and b_pos[1] - 5 <= player_2.y + player_2.height:
            angle = random.randint(140, 220)
            b.speed_x = math.cos(math.radians(angle)) * b.speed 
            b.speed_y = math.sin(math.radians(angle)) * b.speed 

    #se verifica daca mingea iese din ecran (stanga sau dreapta ecranului)
    if b_pos[0] - 5 <= 0: #and b_pos[0] + 5 >= -10:
        player_2.score += 1

        #se reseteaza pozitiile playerilor si mingii si se modifica scorul
        player_1.y = (screen.get_height() - player_1.height ) / 2
        player_2.y = (screen.get_height() - player_1.height ) / 2
        b = ball.Ball(screen.get_width() / 2, screen.get_height() / 2, screen)

        score2 = font.render(str(player_2.score), True, (255, 255, 255), (0, 0, 0))
        score2_rect = score2.get_rect()
        score2_rect.center = (1350 // 2, 80 // 2)

        #in cazul game over, se trimite clientului un mesaj pentru a reseta jocul
        conn.sendall("o2!".encode("utf-8"))
        stop_timer = 100

    elif b_pos[0] + 5 >= screen.get_width(): #and b_pos[0] + 5 <= screen.get_width() + 10:
        player_1.score += 1

        player_1.y = (screen.get_height() - player_1.height ) / 2
        player_2.y = (screen.get_height() - player_1.height ) / 2
        b = ball.Ball(screen.get_width() / 2, screen.get_height() / 2, screen)

        score1 = font.render(str(player_1.score), True, (255, 255, 255), (0, 0, 0))
        score1_rect = score1.get_rect()
        score1_rect.center = (50 // 2, 80 // 2)

        conn.sendall("o1!".encode("utf-8"))
        stop_timer = 100

    #se verifica daca mingea se loveste de partea de sus si de jos a ecranului si se modifica directia
    if b_pos[1] - 5 <= 0:
        b.speed_y = abs(b.speed_y)
    elif b_pos[1] + 5 >= screen.get_height():
        b.speed_y = -abs(b.speed_y)

#executa toate update urile obiectelor la fiecare iteratie a game loop ului
def tick(delta_time):
    client_io()
    b.tick(delta_time)
    collision()

#se deseneaza totul pe ecran
def render():
    screen.fill((0, 0, 0))

    screen.blit(l1, l1_rect)
    screen.blit(l2, l2_rect)
    screen.blit(score1, score1_rect)
    screen.blit(score2, score2_rect)

    player_1.render()
    player_2.render()
    b.render()

    pg.display.flip()

def main():
    global running
    global screen
    global delta_time
    global clock
    global stop_timer
    global IP
    global PORT

    print("Playing as Player 1")

    IP = input("Input IP for server: ")
    PORT = int(input("Input PORT for server: "))

    accept_connection()

    #bucla infinita a jocului (la fiecare iteratie se executa tick si render)
    while running:

        #se preia o lista cu toate eventurile (precum input de la mouse)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()
        player_speed = 600

        #in cazul inputului de la tastatura, se misca playerul 1
        if keys[pg.K_w] and player_1.y > 0 and stop_timer != 0:
            player_1.tick(-player_speed, delta_time)
        elif keys[pg.K_s] and player_1.y + player_1.height < screen.get_height() and stop_timer != 0:
            player_1.tick(player_speed, delta_time)

        #un sistem de pauza
        while stop_timer >= 0:

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    running = False
                    break

            render()

            stop_timer -= 1
            delta_time = clock.tick(60) / 1000

        tick(delta_time)
        render()

        delta_time = clock.tick(60) / 1000

if __name__ == '__main__':
    main()

