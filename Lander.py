import pygame
import sys
import random 

def generate_stars(num_stars):
    stars = []
    for _ in range(num_stars):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        size = random.randint(1, 2)
        stars.append((x, y, size))
    return stars

def generate_terrain():
    terrain = []
    # Define the number of terrain points
    num_points = 50
    # Define the step size for x coordinates
    step = WIDTH / num_points
    # Generate terrain points
    for i in range(num_points + 1):
        x = int(i * step)
        # Generate random height for the terrain within a range
        y = int(HEIGHT * 0.90 + random.randint(-20, 20))
        terrain.append((x, y))
    # Adjust the y-coordinate of the first and last points to start at the bottom of the screen
    terrain[0] = (0, HEIGHT)
    terrain[-1] = (WIDTH, HEIGHT)
    return terrain


# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lunar Lander")

# Load the sprite
sprite = pygame.image.load("starship_small.png")
stars = generate_stars(100)
terrain = generate_terrain()
ship_x_pos, ship_y_pos = 300, 300

#Create an object around the sprite for collision detection and rotation
sprite_rect = sprite.get_rect(center=(WIDTH // 2, HEIGHT // 2))
angle = 0

# Dictionary to store the state of keys (pressed or not pressed)
keys_pressed = {}

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Update the keys_pressed dictionary when a key is pressed
            keys_pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            # Remove the key from keys_pressed when it's released
            keys_pressed.pop(event.key, None)

    # Update the ship's position based on continuous key presses
    if pygame.K_LEFT in keys_pressed:
        angle += 0.1  
    if pygame.K_RIGHT in keys_pressed:
        angle -= 0.1
    if pygame.K_SPACE in keys_pressed:
       ship_y_pos -= 0.1

    # Rotate the sprite
    rotated_sprite = pygame.transform.rotate(sprite, angle)

    # Get the rectangle bounding the rotated sprite and center it
    rotated_rect = rotated_sprite.get_rect(center=sprite_rect.center)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the stars
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), (star[0], star[1]), star[2])

    # Draw the terrain
    pygame.draw.polygon(screen, (100, 100, 100), terrain)

    # Draw the rotated sprite
    screen.blit(rotated_sprite, rotated_rect)

    
    

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
