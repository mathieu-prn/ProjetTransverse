import pygame

# Initialize Pygame
print(pygame.init())

# Set up the game window
WIDTH = 1500
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport")

# Initialize Colors
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)


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
                    screen=pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN)
                else:
                    screen=pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(blue)

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()