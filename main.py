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

class Plane(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    def update(self):
        # Handle Animation
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index > 2:
                self.index = 0
        self.image = self.images[self.index]


plane_group = pygame.sprite.Group()

flappy = Plane(100, int(screen_height / 2))
plane_group.add(flappy)

# Define Variables
ground_scroll = 0
scroll_speed = 4


# Main Game Loop
run = True
while run:

    # Run Clock with predifend FPS
    clock.tick(fps)

    ### Render Images on Screen
    # Render Background
    screen.blit(bg, (0,0))

    # Render Plane on BG
    plane_group.draw(screen)
    plane_group.update()

    # Render Ground & Scroll BG
    screen.blit(ground, (ground_scroll, 768))
    ground_scroll -= scroll_speed 
    if abs(ground_scroll) > 35:
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()