import pygame, json, math
from utility import *


# ---------- Initialization & Global Setup ----------
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport - Golf")
bg =pygame.image.load("assets/Common/Background.png") # Background
logo_long = pygame.image.load("assets/Common/Logo long EFREI sport.png") # Logo
pygame.display.set_icon(logo_long)

font = pygame.font.Font("assets/Common/font.ttf", 48) # Main font
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
blue_efrei = (18, 121, 190)
GREY = (211, 211, 211)
light_grey=(234,234,234)
GREEN = (148, 186, 134)
BUNKER_YELLOW = (237, 225, 141)
WATER_BLUE = (0, 167, 250)

goal=pygame.image.load("assets/goalkeeper.png")
goal_rect = goal.get_rect()

# Position initiale
goal_x = 332 + 100
goal_y = 72
angle = 0
rotation_speed = 2  # Vitesse de rotation
direction = 1

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Design of the page

    # Overlay "efrei sport"
    screen.fill((240,240,240, 0.5))
    screen.blit(bg,(0, 0))

    pygame.draw.rect(screen, (blue_efrei), (32, 48, 936, 430))
    pygame.draw.rect(screen, (light_grey), (32+6, 48+6, 936-12, 430-12))

    pygame.draw.line(screen, blue_efrei, (332, 72), (332, 72+170), width=6)
    pygame.draw.line(screen, blue_efrei, (332+340, 72), (332+340, 72+170), width=6)
    pygame.draw.line(screen, blue_efrei, (330, 72), (332+343, 72), width=6)

    pygame.draw.line(screen, blue_efrei, (38, 72+170), (38+928, 72+170), width=8)

    screen.blit(goal, (332+100, 72))
    # Rotation
    rotated_goal = pygame.transform.rotate(goal, angle)
    rotated_rect = rotated_goal.get_rect(center=(goal_x + goal_rect.width // 2, goal_y + goal_rect.height))

    # Afficher l'image pivotée
    screen.blit(rotated_goal, rotated_rect.topleft)

    # Mettre à jour l'angle

    # Mettre à jour l'angle avec aller-retour
    angle += rotation_speed * direction
    if angle >= 180 or angle <= 0:
        direction *= -1  # Inverser la direction

    # Update the display
    pygame.display.flip()
    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()