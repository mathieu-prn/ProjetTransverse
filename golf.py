import pygame

# Initialize Pygame
print(pygame.init())

# Set up the game window
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Define game objects
circleX = 75
circleY = 75
radius = 5

clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(white)

    # Draw game objects
    pygame.draw.circle(screen,black,(circleX,circleY),radius)

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()