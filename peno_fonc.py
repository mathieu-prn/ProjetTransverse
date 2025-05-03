import pygame, json, math
from utility import *

# ---------- Initialization & Global Setup ----------
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport - Penalty")
bg = pygame.image.load("assets/Common/Background.png")  # Background

#ball_image = pygame.image.load("assets/Football/ball.png")  # Ball
#ball_rect = ball_image.get_rect()
#ball_rect.topleft = (475, 415)

logo_long = pygame.image.load("assets/Common/Logo long EFREI sport.png")  # Logo
pygame.display.set_icon(logo_long)

font = pygame.font.Font("assets/Common/font.ttf", 48)  # Main font
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
blue_efrei = (18, 121, 190)
blue_shade = (100, 210, 255)
GREY = (211, 211, 211)
light_grey = (234, 234, 234)
GREEN = (148, 186, 134)
BUNKER_YELLOW = (237, 225, 141)
WATER_BLUE = (0, 167, 250)

#goal = pygame.image.load("assets/Football/goalkeeper v2.png")
#goal_rect = goal.get_rect()

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Football/ball.png")
        self.rect = self.image.get_rect()
        self.x = 500
        self.y = 440
        self.rect.center = (self.x, self.y)
        self.velocity = 5
        self.angle = 0
        self.target_position = self.rect.center

    def draw(self, surface=screen):
        surface.blit(self.image, self.rect)


class Goalkeeper(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Football/goalkeeper v2.png")
        self.image_rot = self.image
        self.x = 500
        self.y = 167
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect_pos = (self.x, self.y)
        self.angle = 0
        self.rotation_speed = 2.5

    def draw(self, surface=screen):
        surface.blit(self.image_rot, self.rect)
        pygame.draw.circle(surface, blue_shade, self.rect_pos, 5)

    def rotate_keeper(self,clockwise):
        if clockwise:
            self.angle = self.angle + self.rotation_speed
        if not clockwise:
            self.angle = self.angle - self.rotation_speed
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.image_rot = rotated_image
        self.rect = self.image_rot.get_rect(center=self.rect.center)
        self.rect_pos = (500 - self.angle - pygame.Vector2(10,0).rotate(self.angle)[0],263 - pygame.Vector2(0, 100).rotate(self.angle)[1])
        self.x = self.rect_pos[0]
        self.y = self.rect_pos[1]
        self.rect = self.image_rot.get_rect(center=(self.x, self.y))

class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 500
        self.y = 440
        self.pos = (self.x, self.y)
    def draw(self, surface=screen):
        pygame.draw.circle(surface,blue_shade,self.pos,5)
# Vitesse de la balle
#v = 5  # pixels par frame

# Position cible (initialisée à la position actuelle de la balle)
#target_position = ball_rect.center

# Position initiale
#goal_x = 420
#goal_y = 72
#angle = 0
#rotation_speed = 2  # Vitesse de rotation

# État du jeu
game_over = False

#Lock of Target
target_lock = False

#Angle of keeper
clockwise = True

# Fonction pour réinitialiser le jeu
def reset_game():
    global game_over
    game_over = False
    football.x = 500
    football.y = 440
    football.rect.center = (500, 440)
    target.pos = football.rect.center
    target.x =football.x
    target.y =football.y
    keeper.angle = 0

football = Ball()
keeper = Goalkeeper()
target = Target()

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
                    if target.x == football.x and target.y == football.y:
                        target.x = event.pos[0]
                        target.y = event.pos[1]
                        target.pos = (target.x, target.y)
                        if target_lock:
                            target_lock = False
                        else:
                            target_lock = True
    #print(f"Ball: {football.rect}, Keeper: {keeper.rect}, Collision: {football.rect.colliderect(keeper.rect)}")
    # Design of the page
    screen.fill((240, 240, 240, 0.5))
    screen.blit(bg, (0, 0))

    pygame.draw.rect(screen, blue_efrei, (32, 48, 936, 430))
    pygame.draw.rect(screen, light_grey, (32 + 6, 48 + 6, 936 - 12, 430 - 12))

    pygame.draw.line(screen, blue_efrei, (405, 72), (405, 72 + 190), width=6) # Left
    pygame.draw.line(screen, blue_efrei, (405 + 190, 72), (405 + 190, 72 + 190), width=6) #right
    pygame.draw.line(screen, blue_efrei, (403, 72), (404 + 194, 72), width=6) #top

    pygame.draw.line(screen, blue_efrei, (38, 72 + 190), (38 + 928, 72 + 190), width=8)

    pygame.draw.circle(screen, blue_efrei, (500, 440), 10)  # Penalty point
    target.draw()
    if not game_over:
        # Calculer la direction vers la position cible
        #dx = target_position[0] - ball_rect.centerx
        dx = target.x - football.x
        #dy = target_position[1] - ball_rect.centery
        dy = target.y - football.y
        distance = math.hypot(dx, dy)

        #if distance > v:
        if distance > football.velocity:
            # Normaliser le vecteur de direction
            dx /= distance
            dy /= distance

            # Mettre à jour la position de la balle
            #ball_rect.centerx += dx * v
            football.x += dx * football.velocity
            #ball_rect.centery += dy * v
            football.y += dy * football.velocity
        else:
            # Si la distance est inférieure à la vitesse, positionner directement la balle à la cible
            #ball_rect.center = target_position
            football.x = target.x
            football.y = target.y

        # Dessiner la balle à la nouvelle position
        #screen.blit(ball_image, ball_rect.topleft)
        football.rect.center = (football.x, football.y)
        football.draw()

        # Rotation du gardien
        #angle += rotation_speed
        if keeper.angle >= 90 or keeper.angle <= -90:
            temp = clockwise
            clockwise = not temp
        keeper.rotate_keeper(clockwise)

        # Rotation de l'image du gardien
        #rotated_keeper = pygame.transform.rotate(keeper.image, keeper.angle)
        #rotated_rect = rotated_keeper.get_rect(center=(keeper.x + keeper.rect.width // 2, keeper.y + keeper.rect.height // 2))

        # Dessiner le gardien à la nouvelle position
        #screen.blit(rotated_goal, rotated_rect.topleft)
        keeper.draw()

        # Vérifier la collision entre le ballon et le gardien
        #if ball_rect.colliderect(rotated_rect):
        if  football.rect.colliderect(keeper.rect):
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
