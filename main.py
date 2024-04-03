import pygame
import sys
from player import *

pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scientists in time")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)


# Ground properties
ground_height = 50

# Rectangle properties
rect_width, rect_height = 50, 50
x, y = 0, 750 #pos P1
rect_a, rect_b = WIDTH //3 - rect_width // 2, HEIGHT // 3 - rect_height // 2 #pos P2
speed = 5

#jump
jumping = False
gravity = 1
fall_gravity = 10
jump_height = 25
velocity = jump_height

# Platform properties
platform_width, platform_height = 200, 10
platform_x, platform_y = WIDTH // 4, HEIGHT // 2 + HEIGHT // 4

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

cat = Cat(speed, x, y,velocity, jump_height, gravity)

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

    # Fall if not on platform
    if not collision_platform(cat.x, cat.y, rect_width, rect_height, platform_x, platform_y, platform_width,
                              platform_height) and cat.y + rect_height < HEIGHT - ground_height:
        cat.y += fall_gravity

    #zqsd (P2)
    if keys[pygame.K_q]:
        rect_a -= speed
    if keys[pygame.K_d]:
        rect_a += speed
    if keys[pygame.K_z]:
        rect_b -= speed
    if keys[pygame.K_s]:
        rect_b += speed

    #P2
    pygame.draw.rect(screen, BLUE, (rect_a, rect_b, rect_width, rect_height))


    # Drawing ground
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - ground_height, WIDTH, ground_height))

    # Collision with ground 
    if cat.y + rect_height >= HEIGHT - ground_height:
        cat.y = HEIGHT - ground_height - rect_height
        cat.jumping = False

    if rect_b + rect_height >= HEIGHT - ground_height:
        rect_b = HEIGHT - ground_height - rect_height

    pygame.draw.rect(screen, BLACK, (platform_x, platform_y, platform_width, platform_height))
    
    if collision_platform(cat.x, cat.y, rect_width, rect_height, platform_x, platform_y, platform_width, platform_height):
        cat.y = platform_y - rect_height
        cat.jumping = False


    # Update the display
    pygame.display.flip()

    # Limit frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()