import pygame
from pygame.locals import *

pygame.init()

# Init Clock
clock = pygame.time.Clock()
fps = 60

# Define Screen Size
screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy 911')

# Load Images
bg = pygame.image.load('img/bg.png')
ground = pygame.image.load('img/ground.png')

# Define Variables
ground_scroll = 0
scroll_speed = 4


# Main Game Loop
run = True
while run:

    # Run Clock with predifend FPS
    clock.tick(fps)

    # Render Images on Screen
    screen.blit(bg, (0,0))
    screen.blit(ground, (ground_scroll, 768))
    ground_scroll -= scroll_speed 
    if abs(ground_scroll) > 35:
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()