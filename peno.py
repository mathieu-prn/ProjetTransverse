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
BLUE = (0, 0, 255)
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

# État du jeu
game_over = False

# Rectangle autour du gardien
rect_x = 420+30
rect_y = 72+30
rect_width = 116
rect_height = 193

# Fonction pour réinitialiser le jeu
def reset_game():
    global game_over, ball_rect, target_position, angle
    game_over = False
    ball_rect.topleft = (475, 415)
    target_position = ball_rect.center
    angle = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche de la souris
                if game_over:
                    # Vérifier si le bouton "Recommencer" est cliqué
                    if 400 <= event.pos[0] <= 600 and 225 <= event.pos[1] <= 275:
                        reset_game()
                else:
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

    # Créer une surface temporaire pour dessiner le rectangle
    temp_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
    temp_surface.fill((0, 0, 0, 0))  # Remplir avec une couleur transparente

    # Dessiner le rectangle sur la surface temporaire
    pygame.draw.rect(temp_surface, BLACK, (0, 0, rect_width, rect_height), 2)

    # Faire tourner la surface temporaire
    rotated_surface = pygame.transform.rotate(temp_surface, angle)
    rotated_rect = rotated_surface.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height // 2))

    # Dessiner la surface rotée sur l'écran principal
    screen.blit(rotated_surface, rotated_rect.topleft)

    if not game_over:
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

        # Dessiner le cercle autour du ballon
        pygame.draw.circle(screen, BLACK, ball_rect.center, 25, 2)

        # Rotation du gardien
        if not game_over:
            angle += rotation_speed
            if angle >= 360:
                angle = 0

        # Rotation de l'image du gardien
        rotated_goal = pygame.transform.rotate(goal, angle)
        rotated_goal_rect = rotated_goal.get_rect(center=(goal_x + goal_rect.width // 2, goal_y + goal_rect.height // 2))

        # Dessiner le gardien à la nouvelle position
        screen.blit(rotated_goal, rotated_goal_rect.topleft)

        # Vérifier la collision entre le cercle autour du ballon et le rectangle noir
        if rotated_rect.collidepoint(ball_rect.center) or \
           rotated_rect.collidepoint(ball_rect.centerx + 25, ball_rect.centery) or \
           rotated_rect.collidepoint(ball_rect.centerx - 25, ball_rect.centery) or \
           rotated_rect.collidepoint(ball_rect.centerx, ball_rect.centery + 25) or \
           rotated_rect.collidepoint(ball_rect.centerx, ball_rect.centery - 25):
            print("perdu")
            game_over = True
    else:
        # Afficher "perdu" à l'écran
        font = pygame.font.Font(None, 74)
        text = font.render("Perdu", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 50))

        # Dessiner le bouton "Recommencer"
        pygame.draw.rect(screen, GREEN, (400, 225, 200, 50))
        font = pygame.font.Font(None, 36)
        text = font.render("Recommencer", True, BLACK)
        screen.blit(text, (410, 235))

    # Update the display
    pygame.display.flip()
    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()
