import pygame
import sys

pygame.init()

# Set up the screen
WIDTH, HEIGHT = 1920, 1080
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
rect_a, rect_b = WIDTH // 3 - rect_width // 2, HEIGHT // 3 - rect_height // 2
rect_speed = 5

# Traps properties
rect_tx, rect_ty = 50, 120
trap_w, trap_h = 30, 100

# Jump
jumping = False
b_gravity = 1
fall_gravity = 10
jump = 25
b_velocity = jump

# Platform properties
platform_width, platform_height = 200, 10
platform_x, platform_y = WIDTH // 4, HEIGHT // 2 + HEIGHT // 4

# Set up the second button
button2_x, button2_y = 120, HEIGHT - ground_height - 10
button2_width, button2_height = 30, 10
b2_activate = False

# Main game loop
running = True

# Traps
trape_activated = True

# Wall visibility
wall_visible = True

def collision_platform(rect1_x, rect1_y, rect1_width, rect1_height, rect2_x, rect2_y, rect2_width, rect2_height):
    return (rect1_x < rect2_x + rect2_width and
            rect1_x + rect1_width > rect2_x and
            rect1_y < rect2_y + rect2_height and
            rect1_y + rect1_height > rect2_y)


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

    if keys[pygame.K_UP] and not jumping:
        jumping = True
        b_velocity = jump

    if jumping:
        rect_y -= b_velocity
        b_velocity -= b_gravity
        if b_velocity < -jump:
            jumping = False

    if keys[pygame.K_DOWN]:
        rect_y += rect_speed

    # Drawing P1
    pygame.draw.rect(screen, BLACK, (rect_x, rect_y, rect_width, rect_height))

    # Drawing P2
    pygame.draw.rect(screen, BLUE, (rect_a, rect_b, rect_width, rect_height))

    # Drawing traps
    if trape_activated:
        pygame.draw.rect(screen, BLACK, (rect_tx, rect_ty, trap_w, trap_h))

    # Drawing button
    pygame.draw.rect(screen, BLUE, (750, HEIGHT - ground_height - 10, 30, 10))

    # Drawing button2
    pygame.draw.rect(screen, BLUE, (button2_x, button2_y, button2_width, button2_height))

    # Check if P1 or P2 is on the button2
    if (rect_x < button2_x + button2_width and rect_x + rect_width > button2_x and
            rect_y < button2_y + button2_height and rect_y + rect_height > button2_y) or (
            rect_a < button2_x + button2_width and rect_a + rect_width > button2_x and
            rect_b < button2_y + button2_height and rect_b + rect_height > button2_y):
        b2_activate = False
    else:
        b2_activate = True

    # Drawing ground
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - ground_height, WIDTH, ground_height))

    # Fall if not on platform
    if not collision_platform(rect_x, rect_y, rect_width, rect_height, platform_x, platform_y, platform_width,
                              platform_height) and rect_y + rect_height < HEIGHT - ground_height:
        rect_y += fall_gravity

    # Drawing wall
    if (b2_activate == True or trape_activated == True):
        pygame.draw.rect(screen, BLACK, (rect_tx + 40, rect_ty, trap_w, trap_h))

    # Drawing platform
    pygame.draw.rect(screen, BLACK, (platform_x, platform_y, platform_width, platform_height))

    # zqsd (P2)
    if keys[pygame.K_q]:
        rect_a -= rect_speed
    if keys[pygame.K_d]:
        rect_a += rect_speed
    if keys[pygame.K_z]:
        rect_b -= rect_speed
    if keys[pygame.K_s]:
        rect_b += rect_speed

    # Collision with ground for P1
    if rect_y + rect_height >= HEIGHT - ground_height:
        rect_y = HEIGHT - ground_height - rect_height
        jumping = False

    # Collision with ground for P2
    if rect_b + rect_height >= HEIGHT - ground_height:
        rect_b = HEIGHT - ground_height - rect_height

    # Collision with platform for P1
    if collision_platform(rect_x, rect_y, rect_width, rect_height, platform_x, platform_y, platform_width,
                           platform_height):
        rect_y = platform_y - rect_height
        jumping = False

    # Collision with sides and ceiling for P1
    if rect_x < 0:
        rect_x = 0
    elif rect_x + rect_width > WIDTH:
        rect_x = WIDTH - rect_width

    if rect_y < 0:
        rect_y = 0
    elif rect_y + rect_height > HEIGHT - ground_height:
        rect_y = HEIGHT - ground_height - rect_height
        jumping = False

    # Collision with sides and ceiling for P2
    if rect_a < 0:
        rect_a = 0
    elif rect_a + rect_width > WIDTH:
        rect_a = WIDTH - rect_width

    if rect_b < 0:
        rect_b = 0
    elif rect_b + rect_height > HEIGHT - ground_height:
        rect_b = HEIGHT - ground_height - rect_height

    # Check if P1 or P2 is on the button
    if (rect_x < 750 + button2_width and rect_x + rect_width > 750 and
            rect_y < HEIGHT - ground_height - 10 + button2_height and rect_y + rect_height > HEIGHT - ground_height - 10) or (
            rect_a < 750 + button2_width and rect_a + rect_width > 750 and
            rect_b < HEIGHT - ground_height - 10 + button2_height and rect_b + rect_height > HEIGHT - ground_height - 10):
        trape_activated = False
    else:
        trape_activated = True

    # Update the display
    pygame.display.flip()

    # Limit frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
