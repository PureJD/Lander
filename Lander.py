import pygame
import sys
import random 
import math

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
pygame.mixer.init()

# Set up the window
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lunar Lander")

# Load the sprite
thruster_sound = pygame.mixer.Sound("sounds/thruster.wav")
thruster_sound.set_volume(0.05)
sprite = pygame.image.load("images/starship_small.png")
mount_sprite = pygame.image.load("images/mount_small.png")
thrust_sprite_original = pygame.image.load("images/thrust.png")
stars = generate_stars(100)
terrain = generate_terrain()
ship_x_pos, ship_y_pos = 300, 300

#Create an object around the sprite for collision detection and rotation
sprite_rect = sprite.get_rect(center=(WIDTH // 2, HEIGHT // 2))
#Position argument for sprit to stop it jumping across the screen 
ship_x_pos, ship_y_pos = WIDTH // 2, HEIGHT // 2
#Initial angle of the ship (Can be used for physics as matches angles in physics)
angle = 0

mount_rect = mount_sprite.get_rect(center=(WIDTH // 2, terrain[0][1] - 140))
thrust_rect = thrust_sprite_original.get_rect(center=(WIDTH // 2, HEIGHT - 100))

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
        angle += 0.5 
    elif pygame.K_RIGHT in keys_pressed:
        angle -= 0.5
    elif pygame.K_SPACE in keys_pressed:
        pygame.mixer.Sound.play(thruster_sound)
        # Define the magnitude of the velocity (how fast the ship moves)
        velocity_magnitude = 1  # Adjust this value as needed
        # Calculate the horizontal and vertical components of velocity based on the angle
        velocity_x = velocity_magnitude * math.cos(math.radians(angle - 90))  # Horizontal component
        velocity_y = -velocity_magnitude * math.sin(math.radians(angle - 90))  # Vertical component
        # Update ship's position based on velocity
        ship_x_pos -= velocity_x
        ship_y_pos -= velocity_y
        # Update the position of the sprite_rect object
        sprite_rect.centerx = ship_x_pos
        sprite_rect.centery = ship_y_pos
        # Update thrust sprite position and angle
        thrust_rect.centerx = ship_x_pos  # Align thrust sprite center with ship center
        thrust_rect.centery = ship_y_pos + 40  # Position thrust sprite below the ship
        thrust_sprite = pygame.transform.rotate(thrust_sprite_original, angle)  # Rotate thrust sprite

    # Rotate the sprite
    rotated_sprite = pygame.transform.rotate(sprite, angle)

    # Get the rectangle bounding the rotated sprite and center it
    rotated_rect = rotated_sprite.get_rect(center=sprite_rect.center)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the stars, terrain, rotated sprite, mount sprite, and thrust sprite
    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), (star[0], star[1]), star[2])
    pygame.draw.polygon(screen, (40, 40, 40), terrain)
    screen.blit(rotated_sprite, rotated_rect)
    screen.blit(mount_sprite, mount_rect)
    screen.blit(thrust_sprite_original, thrust_rect)

    # Gravity physics 
    gravity_strength = 0.3
    ship_x_pos += gravity_strength
    ship_y_pos += gravity_strength
    sprite_rect.centerx = ship_x_pos
    sprite_rect.centery = ship_y_pos

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()