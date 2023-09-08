import pygame
from pygame.locals import *
import random



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
skyskraper_gap = 150
skyskraper_frequency = 1500 # in milliseconds
last_skyskraper = pygame.time.get_ticks() - skyskraper_frequency
score = 0
pass_skyskrapers = False

font = pygame.font.SysFont('Bauhaus 93', 60)
white = (255, 255, 255)

# Initialize Screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Terrorists')





# Load Background Images
bg = pygame.image.load('img/bg.png')
ground = pygame.image.load('img/ground.png')
btn_img = pygame.image.load('img/restart.png')

def draw_text(text, font, text_color, x, y):

    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

def reset_game():
    skyskraper_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score


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
            flap_cooldown = 5
            self.counter += 1

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


class Skyscrapers(pygame.sprite.Sprite):

    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        # Position One is from Top, Position 2 from Bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(skyskraper_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(skyskraper_gap / 2)]
    
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False
        # Get Mouse Position
        pos = pygame.mouse.get_pos()
        # Check Mouse hover
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # Draw Button
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
        return action
    
plane_group = pygame.sprite.Group()
skyskraper_group = pygame.sprite.Group()

flappy = Plane(100, int(screen_height / 2))

plane_group.add(flappy)

# Create Button
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, btn_img)



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
    skyskraper_group.draw(screen)
    plane_group.update()

    screen.blit(ground, (ground_scroll, 768))

    # Check Score
    if len(skyskraper_group) > 0:
        if plane_group.sprites()[0].rect.left > skyskraper_group.sprites()[0].rect.left\
            and plane_group.sprites()[0].rect.right < skyskraper_group.sprites()[0].rect.right\
            and pass_skyskrapers == False:
            pass_skyskrapers = True
        if pass_skyskrapers == True:
            if plane_group.sprites()[0].rect.left > skyskraper_group.sprites()[0].rect.right:
                score += 1
                pass_skyskrapers = False

    draw_text(str(score), font, white, int(screen_width / 2), 20)

    # Check for Collision
    if pygame.sprite.groupcollide(plane_group, skyskraper_group, False, False) or flappy.rect.top < 0:
        game_over = True



    # Check if Bird has hit ground
    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False
    
    if flying == True and game_over == False:
        # Generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_skyskraper > skyskraper_frequency:
            skyskraper_height = random.randint(-100, 100)
            btm_skyskraper = Skyscrapers(screen_width, int(screen_height / 2) + skyskraper_height, -1)
            top_skyskraper = Skyscrapers(screen_width, int(screen_height / 2) + skyskraper_height, 1)
            skyskraper_group.add(btm_skyskraper)
            skyskraper_group.add(top_skyskraper)
            last_skyskraper = time_now
        
        skyskraper_group.update()

        ground_scroll -= scroll_speed 
        if abs(ground_scroll) > 35:
            ground_scroll = 0
        
        skyskraper_group.update()


    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True
        


    pygame.display.update()


pygame.quit()