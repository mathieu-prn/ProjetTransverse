import pygame

# Initialize Pygame
print(pygame.init())

# Set up the game window
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red= (255, 0, 0)

# Define game objects
circleX = 75
circleY = 75
radius = 5

slider_rect = pygame.Rect(30, 30, 30, 200)
sliderX = 30
sliderY = 200

clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        mouse_pos = pygame.mouse.get_pos()

        if slider_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]!=0:
            # collision detection also needed here
            slider1 = pygame.mouse.get_pos()[0] - 5
            if slider1 < 30:
                slider1 = 30
            if slider1 > 230:
                slider1 = 230

    # Clear the screen
    screen.fill(white)

    # Draw game objects
    pygame.draw.rect(screen, black, slider_rect)
    pygame.draw.rect(screen, red, pygame.Rect(sliderX, sliderY, 30, 5))
    pygame.draw.circle(screen,black,(circleX,circleY),radius)

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()