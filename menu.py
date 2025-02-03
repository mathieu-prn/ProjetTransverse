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
    screen.fill((240,240,240, 0.5))
    screen.blit(bg,(0, 0))
    logo_long = pygame.image.load("assets/Logo long EFREI sport.png")
    screen.blit(logo_long, (345, 32))

    pygame.draw.line(screen, blue_efrei, (0,172), (1000,172), width=16)
    pygame.draw.line(screen, blue_efrei, (0, 172+32), (1000, 172+32), width=16)
    pygame.draw.rect(screen,(201,201,201),(0,330,1000,176))


    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()