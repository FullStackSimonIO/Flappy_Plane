import pygame
from pygame.locals import *



# Init Game Engine
pygame.init()



# Init Clock
clock = pygame.time.Clock()
fps = 60



# Define Screen Size
screen_width = 864
screen_height = 936



# Define System Variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False



# Initialize Screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy 911')



# Load Background Images
bg = pygame.image.load('img/bg.png')
ground = pygame.image.load('img/ground.png')



# Define Plane Class 
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
        self.vel = 0

    # Define Update Function
    def update(self):
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)
        
        # Integrate Jump Function
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            # Handle Animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # Rotate the Bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:                        
            self.image = pygame.transform.rotate(self.images[self.index], -90)


plane_group = pygame.sprite.Group()

flappy = Plane(100, int(screen_height / 2))
plane_group.add(flappy)

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

    # Check if Bird has hit ground
    if flappy.rect.bottom > 768:
        game_over = True
        flying = False
    
    if game_over == False:
        screen.blit(ground, (ground_scroll, 768))
        ground_scroll -= scroll_speed 
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
        


    pygame.display.update()


pygame.quit()