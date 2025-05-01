import pygame, json, math
from utility import *

# ---------- Initialization & Global Setup ----------
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport - Golf")
bg = pygame.image.load("assets/Common/Background.png")  # Background

ball_image = pygame.image.load("assets/Football/ball.png")  # Ball
ball_rect = ball_image.get_rect()
ball_rect.topleft = (475, 415)

logo_long = pygame.image.load("assets/Common/Logo long EFREI sport.png")  # Logo
pygame.display.set_icon(logo_long)

font = pygame.font.Font("assets/Common/font.ttf", 48)  # Main font
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
blue_efrei = (18, 121, 190)
GREY = (211, 211, 211)
light_grey = (234, 234, 234)
GREEN = (148, 186, 134)
BUNKER_YELLOW = (237, 225, 141)
WATER_BLUE = (0, 167, 250)

goal = pygame.image.load("assets/Football/goalkeeper v2.png")
goal_rect = goal.get_rect()

# Vitesse de la balle
v = 5  # pixels par frame

# Position cible (initialisée à la position actuelle de la balle)
target_position = ball_rect.center

# Position initiale
goal_x = 420
goal_y = 72
angle = 0
rotation_speed = 2  # Vitesse de rotation

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche de la souris
                target_position = event.pos

    # Design of the page
    screen.fill((240, 240, 240, 0.5))
    screen.blit(bg, (0, 0))

    pygame.draw.rect(screen, blue_efrei, (32, 48, 936, 430))
    pygame.draw.rect(screen, light_grey, (32 + 6, 48 + 6, 936 - 12, 430 - 12))

    pygame.draw.line(screen, blue_efrei, (405, 72), (405, 72 + 190), width=6) # Left
    pygame.draw.line(screen, blue_efrei, (405 + 190, 72), (405 + 190, 72 + 190), width=6) #right
    pygame.draw.line(screen, blue_efrei, (403, 72), (404 + 194, 72), width=6) #top

    pygame.draw.line(screen, blue_efrei, (38, 72 + 190), (38 + 928, 72 + 190), width=8)

    pygame.draw.circle(screen, blue_efrei, (500, 440), 25)  # Penalty point

    # Calculer la direction vers la position cible
    dx = target_position[0] - ball_rect.centerx
    dy = target_position[1] - ball_rect.centery
    distance = math.hypot(dx, dy)

    if distance > v:
        # Normaliser le vecteur de direction
        dx /= distance
        dy /= distance

        # Mettre à jour la position de la balle
        ball_rect.centerx += dx * v
        ball_rect.centery += dy * v
    else:
        # Si la distance est inférieure à la vitesse, positionner directement la balle à la cible
        ball_rect.center = target_position

    # Dessiner la balle à la nouvelle position
    screen.blit(ball_image, ball_rect.topleft)

    # Rotation du gardien
    angle += rotation_speed
    if angle >= 360:
        angle = 0

    # Rotation de l'image du gardien
    rotated_goal = pygame.transform.rotate(goal, angle)
    rotated_rect = rotated_goal.get_rect(center=(goal_x + goal_rect.width // 2, goal_y + goal_rect.height // 2))

    # Dessiner le gardien à la nouvelle position
    screen.blit(rotated_goal, rotated_rect.topleft)

    # Update the display
    pygame.display.flip()
    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
