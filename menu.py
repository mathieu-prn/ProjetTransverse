import pygame

# Initialize Pygame
print(pygame.init())

# Set up the game window
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport - Menu")
bg = pygame.image.load("assets/Background.png")

# Initialize Colors
red=(255,0,0)
green=(0,255,0)
blue_efrei=(18,121,190)


clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((red))
    screen.blit(bg,(0, 0))

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()