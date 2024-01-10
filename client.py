import pygame as pg
import game_objects.player as player
import game_objects.ball as ball
import socket

'''
    fisierul care se ocupa de functionarea clientului
    clientului va controla intotdeauna playerul 2
'''

#initializare pygame
pg.init()
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

#se conecteaza clientul la server
def connect():
    s.connect((IP, int(PORT)))

#se primesc datele de la server si se trimite pozitia playerului 2
def server_io():
    global score1, score1_rect
    global score2, score2_rect
    global player_1, player_2
    global b
    global stop_timer
    global running

    s.sendall((str(player_2.x) + "_" + str(player_2.y)).encode("utf-8"))
    
    try:
        data = s.recv(1024)
    
        if data and data != b'':
            decode = data.decode("utf-8")
            '''check = decode.split("!")'''

            #se verifica daca se primeste mesajul de game over
            if "o1" in decode:
                player_1.score += 1

                player_1.y = (screen.get_height() - player_1.height ) / 2
                player_2.y = (screen.get_height() - player_1.height ) / 2
                b = ball.Ball(screen.get_width() / 2, screen.get_height() / 2, screen)

                score1 = font.render(str(player_1.score), True, (255, 255, 255), (0, 0, 0))
                score1_rect = score1.get_rect()
                score1_rect.center = (50 // 2, 80 // 2)

                stop_timer = 100
                return
            elif "o2" in decode:
                player_2.score += 1

                player_1.y = (screen.get_height() - player_1.height ) / 2
                player_2.y = (screen.get_height() - player_1.height ) / 2
                b = ball.Ball(screen.get_width() / 2, screen.get_height() / 2, screen)

                score2 = font.render(str(player_2.score), True, (255, 255, 255), (0, 0, 0))
                score2_rect = score2.get_rect()
                score2_rect.center = (1350 // 2, 80 // 2)

                stop_timer = 100
                return
            
            pos = decode.split("_")

            if len(pos) > 1:
                player_1.y = float(pos[1])
                b.x = float(pos[2])
                b.y = float(pos[3])

            #se verifica daca se primeste mesajul de game over
            '''if len(check) == 1:
                pos = check[0].split("_")
                player_1.y = float(pos[1])
                b.x = float(pos[2])
                b.y = float(pos[3])
            else:
                if check[0] == "o1":
                    player_1.score += 1

                    player_1.y = (screen.get_height() - player_1.height ) / 2
                    player_2.y = (screen.get_height() - player_1.height ) / 2
                    b = ball.Ball(screen.get_width() / 2, screen.get_height() / 2, screen)

                    score1 = font.render(str(player_1.score), True, (255, 255, 255), (0, 0, 0))
                    score1_rect = score1.get_rect()
                    score1_rect.center = (50 // 2, 80 // 2)

                    stop_timer = 100
                else:
                    player_2.score += 1

                    player_1.y = (screen.get_height() - player_1.height ) / 2
                    player_2.y = (screen.get_height() - player_1.height ) / 2
                    b = ball.Ball(screen.get_width() / 2, screen.get_height() / 2, screen)

                    score2 = font.render(str(player_2.score), True, (255, 255, 255), (0, 0, 0))
                    score2_rect = score2.get_rect()
                    score2_rect.center = (1350 // 2, 80 // 2)

                    stop_timer = 100'''

    except:
        print("Connection closed")
        running = False
        s.close()
        return

#executa toate update urile obiectelor la fiecare iteratie a game loop ului
def tick():
    server_io()

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
    global stop_timer
    global clock
    global IP
    global PORT

    print("Playing as Player 2")

    IP = input("Input IP for server: ")
    PORT = int(input("Input PORT for server: "))

    connect()

    #bucla infinita a jocului (la fiecare iteratie se executa tick si render)
    while running:

        #se preia o lista cu toate eventurile (precum input de la mouse)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

        keys = pg.key.get_pressed()
        player_speed = 600

        #in cazul inputului de la tastatura, se misca playerul 2
        if keys[pg.K_w] and player_2.y > 0 and stop_timer != 0:
            player_2.tick(-player_speed, delta_time)
        elif keys[pg.K_s] and player_2.y + player_2.height < screen.get_height() and stop_timer != 0:
            player_2.tick(player_speed, delta_time)

        #un sistem de pauza
        while stop_timer >= 0:

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    running = False
                    break

            render()
            stop_timer -= 1
            delta_time = clock.tick(60) / 1000
            
        tick()
        render()

        delta_time = clock.tick(60) / 1000

if __name__ == '__main__':
    main()

