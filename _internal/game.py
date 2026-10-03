import pygame
import shutil
import os

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
player_speed = 150
currbg = None
player_pos = pygame.Vector2(429, 500)

def init(player, flag=False) -> list:
    print('initializing')
    global screen
    global clock
    global running
    global dt
    global player_speed
    global currbg
    global player_pos
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    player_speed = 150
    player_pos = pygame.Vector2(429, 500)

    if flag:
        currbg = pygame.image.load('_internal\\newbg.png').convert()
    else:
        currbg = pygame.image.load('_internal\\bg.png').convert()

    return run_pygame(player, currbg)

def exit_pygame(player) -> pygame.Vector2:
    global player_pos
    global screen
    screen.blit(player, player_pos)
    pygame.image.save(screen, 'newbg.png')
    shutil.copy('newbg.png', '_internal\\newbg.png')
    os.remove('newbg.png')
    pygame.quit()
    return player_pos


def run_pygame(player, currbg=currbg) -> list:
    global screen
    global clock
    global dt
    global player_speed
    global running
    global player_pos
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(player, player_pos)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
           player_pos.y -= player_speed * dt
        if keys[pygame.K_s]:
            player_pos.y += player_speed * dt
        if keys[pygame.K_a]:
            player_pos.x -= player_speed * dt
        if keys[pygame.K_d]:
            player_pos.x += player_speed * dt
        print(player_pos)
        


        pygame.display.flip()
    
        screen.blit(currbg, (0, 0))

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    return list(exit_pygame(player))


if __name__ == "__main__":
    init(pygame.image.load('_interal\\input.png'), True)