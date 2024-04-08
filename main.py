import pygame
import sys
from player import *
from platforms import Platform

pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whiskers & Wings : The Time Odyssey")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)


# Ground properties
ground_height = 50

# Rectangle properties
rect_width, rect_height = 25,25 
x, y = 100, 1000 #pos P1
a, b = 1700, 950 #pos P2
speed = 5

#jump
jumping = False
gravity = 1
fall_gravity = 10
jump_height = 22
velocity = jump_height

# Platform properties
"""platform_width, platform_height = 200, 10
platform_x, platform_y = WIDTH // 4, HEIGHT // 2 + HEIGHT // 4"""

platform = [Platform(300, 975, 100, 10), #cat side
            Platform(140, 900, 100, 10),
            Platform(400, 860, 15, 300), #vertical
            Platform(350, 860, 250, 10),]

# Main game loop
running = True

def collision_platform(rect1_x, rect1_y, rect1_width, rect1_height, rect2_x, rect2_y, rect2_width, rect2_height):
    if (rect1_x < rect2_x + rect2_width and
        rect1_x + rect1_width > rect2_x and
        rect1_y < rect2_y + rect2_height and
        rect1_y + rect1_height > rect2_y): 
        return True
    else:
        return False


class health_bar:
    def __init__(self, x, y, a, b):
        self.x = x 
        self.y = y 
        self.a = a 
        self.b = b 
        self.health = 100
        self.max_health = 100 
        self.attack = 10 

    def update_pos(self, x, y, a, b):
        self.x = x + self.max_health/4
        self.y = y - self.max_health/4 
        self.a = a + self.max_health/4
        self.b = b - self.max_health/4

    #barre de vie joueur (cat)
    def update_health_bar(self, surface): 
        # bar_color = (111, 210, 46) #couleur pour la jauge de vie
        # back_bar_color= (60, 63, 60) #arrière plan de la jauge de vie 
        # bar_position =[self.rect.x +10 ,self.rect.y -20 , self.health, 5]
        #position de l'arrière plan de la jauge de vie 
        # back_bar_position =[self.rect.x +10 ,self.rect.y -20, self.max_health, 5]

        #dessiner la barre de vie (cat)
        pygame.draw.rect(surface, (60, 63, 60), [100, 20, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [100, 20, self.health, 5])

        # bird
        pygame.draw.rect(surface, (60, 63, 60), [1700, 20, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [1700, 20, self.health, 5])


bar = health_bar(x, y, a, b)

cat = Cat(speed, x, y,velocity, jump_height, gravity)
bird = Bird(speed, a, b)


frame = 0 #last_update at index 0 of the list
last_update = pygame.time.get_ticks() #animation in ms

while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    #movment P1
    cat.mov(keys)
    
    #P1
    pygame.draw.rect(screen, BLACK, (cat.x, cat.y, rect_width, rect_height))    
    
    # Drawing all platform
    for platfrm in platform:
        platfrm.draw(screen)

    # Fall if not on platform
        if collision_platform(cat.x, cat.y, rect_width, rect_height, platfrm.c, platfrm.d, platfrm.width, platfrm.height):
            cat.y = platfrm.d - rect_height
            cat.jumping = False
        
    if cat.y + rect_height < HEIGHT - ground_height:
        cat.y += fall_gravity

    #movment P2
    bird.mov(keys)

    #P2
    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - last_update
    animation_speed = 150

    if elapsed_time >= animation_speed:
        #next frame
        frame = (frame + 1) % len(bird.img) #%len permet de ne pas dépasser la taille donc de tourner en boucle
        #Update the time
        last_update = current_time
    
    screen.blit(bird.img[frame], (bird.a, bird.b, rect_width, rect_height))

    # Drawing ground
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - ground_height, WIDTH, ground_height))

    # Collision with ground 
    if cat.y + rect_height >= HEIGHT - ground_height:
        cat.y = HEIGHT - ground_height - rect_height
        cat.jumping = False

    if bird.b + bird.img[0].get_height() - 17 >= HEIGHT - ground_height:
        bird.b = HEIGHT - ground_height - bird.img[0].get_height() + 17
   
    #actualiser la barre de vie du joueur 
    bar.update_pos(cat.x, cat.y, bird.a, bird.b)
    # bar.update_pos2(bird.a, bird.b)
    bar.update_health_bar(screen)

    # Update the display
    pygame.display.flip()

    # Limit frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()