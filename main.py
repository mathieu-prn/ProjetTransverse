import pygame

# Initialize Pygame
print(pygame.init())

# Set up the game window
WIDTH = 1400
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport")
pygame_icon = pygame.image.load('assets/logo.png')
pygame.display.set_icon(pygame_icon)

# Initialize Colors
color_of_the_back=(182,32,219)


clock = pygame.time.Clock()
fullscreen=False
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key== pygame.K_f:
                fullscreen=not fullscreen
                if fullscreen:
                    screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
                else:
                    screen=pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(color_of_the_back)

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()