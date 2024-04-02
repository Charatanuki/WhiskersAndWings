import pygame
import sys

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
rect_x, rect_y = 0, 750
rect_a, rect_b = WIDTH //3 - rect_width // 2, HEIGHT // 3 - rect_height // 2
rect_speed = 5

#jump
jumping = False
b_gravity = 1
fall_gravity = 10
jump = 25
b_velocity = jump

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

while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # left, right, jump, down (P1)
    if keys[pygame.K_LEFT]:
        rect_x -= rect_speed
    if keys[pygame.K_RIGHT]:
        rect_x += rect_speed

    if keys[pygame.K_UP] and not jumping :
        jumping = True
        b_velocity = jump
        
    if jumping:
        rect_y-=b_velocity
        b_velocity-=b_gravity
        if b_velocity<- jump:
            jumping = False

    if keys[pygame.K_DOWN]:
        rect_y += rect_speed

    #P1
    pygame.draw.rect(screen, BLACK, (rect_x, rect_y, rect_width, rect_height))

    # Fall if not on platform
    if not collision_platform(rect_x, rect_y, rect_width, rect_height, platform_x, platform_y, platform_width,
                              platform_height) and rect_y + rect_height < HEIGHT - ground_height:
        rect_y += fall_gravity

    #zqsd (P2)
    if keys[pygame.K_q]:
        rect_a -= rect_speed
    if keys[pygame.K_d]:
        rect_a += rect_speed
    if keys[pygame.K_z]:
        rect_b -= rect_speed
    if keys[pygame.K_s]:
        rect_b += rect_speed

    #P2
    pygame.draw.rect(screen, BLUE, (rect_a, rect_b, rect_width, rect_height))


    # Drawing ground
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - ground_height, WIDTH, ground_height))

    # Collision with ground 
    if rect_y + rect_height >= HEIGHT - ground_height:
        rect_y = HEIGHT - ground_height - rect_height
        jumping = False

    if rect_b + rect_height >= HEIGHT - ground_height:
        rect_b = HEIGHT - ground_height - rect_height

    pygame.draw.rect(screen, BLACK, (platform_x, platform_y, platform_width, platform_height))
    
    if collision_platform(rect_x, rect_y, rect_width, rect_height, platform_x, platform_y, platform_width, platform_height):
        rect_y = platform_y - rect_height
        jumping = False


    # Update the display
    pygame.display.flip()

    # Limit frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()