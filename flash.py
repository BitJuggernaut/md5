import pygame
import random
import threading
import time
from playsound import playsound

global done

window_x = 300
window_y = 200

def perotachnika():
    playsound('el_matador_8232191926486850177.mp3')

def get_rand_colour():
    colour_r = random.randint(0,255)
    colour_g = random.randint(0,255)
    colour_b = random.randint(0,255)
    return (colour_r,colour_g,colour_b)


def leave_flash(seconds):
    global done
    time.sleep(seconds)
    done = True

#screen = pygame.display.set_mode((window_x,window_y))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Rainbow!")
clock = pygame.time.Clock()

done = False
counter = 0
colour = get_rand_colour()

threading.Thread(target=perotachnika).start()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    threading.Thread(target=leave_flash, args=(5,)).start()

    counter += 1
    if counter > 3:
        colour = get_rand_colour()
        counter = 0

    screen.fill(colour)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
