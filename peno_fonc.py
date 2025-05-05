import pygame, json, math
from utility import *

# ---------- Initialization & Global Setup ----------
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.image.load("assets/Common/Background.png")  # Background

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

# State of the game
game_over = False

#Lock of Target
target_lock = False

#Angle of keeper
clockwise = True

def run():
    global game_over,target_lock,clockwise
    pygame.display.set_caption("EfreiSport - Penalty")

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
            self.rect = self.image_rot.get_rect(center=(self.x, self.y))
            self.rect_pos = (self.x, self.y)
            self.angle = 0
            self.rotation_speed = 1

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
            self.rect = self.image_rot.get_rect(center=(self.x,self.y))

    class Target(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.x = 500
            self.y = 440
            self.pos = (self.x, self.y)
        def draw(self, surface=screen):
            pygame.draw.circle(surface,blue_shade,self.pos,5)

    # Function to reset the game
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
                if event.button == 1:  # Left click
                    if game_over:
                        # Check if the "Start Again" button is clicked
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
        # Design of the page
        screen.fill((240, 240, 240, 0.5))
        screen.blit(bg, (0, 0))

        pygame.draw.rect(screen, blue_efrei, (32, 48, 936, 430))
        pygame.draw.rect(screen, light_grey, (32 + 6, 48 + 6, 936 - 12, 430 - 12))

        pygame.draw.line(screen, blue_efrei, (300, 72), (300, 72 + 190), width=6) # Left
        pygame.draw.line(screen, blue_efrei, (405 + 190 + 105, 72), (405 + 190 + 105, 72 + 190), width=6) #right
        pygame.draw.line(screen, blue_efrei, (298, 72), (404 + 194+105, 72), width=6) #top

        pygame.draw.line(screen, blue_efrei, (38, 72 + 190), (38 + 928, 72 + 190), width=8)

        pygame.draw.circle(screen, blue_efrei, (500, 440), 10)  # Penalty point
        target.draw()
        if not game_over:
            # Find the direction vector between ball and target
            dx = target.x - football.x
            dy = target.y - football.y
            distance = math.hypot(dx, dy)

            if distance > football.velocity:
                # Normalize the direction vector
                dx /= distance
                dy /= distance

                # Update the ball's position
                football.x += dx * football.velocity
                football.y += dy * football.velocity
            else:
                # If ball almost at target, move to target position
                football.x = target.x
                football.y = target.y

            # Draw football at new position
            football.rect.center = (football.x, football.y)
            football.draw()

            # Rotate keeper
            if keeper.angle >= 90 or keeper.angle <= -90:
                temp = clockwise
                clockwise = not temp
            keeper.rotate_keeper(clockwise)

            # Draw the keeper at new position
            keeper.draw()

            # Keeper's hitbox height and width
            keeper.rect.height = 20
            keeper.rect.width = 20

            pygame.draw.rect(screen, blue_efrei, keeper.rect)
            if  football.rect.colliderect(keeper.rect):
                print("lost")
                game_over = True
        else:
            # Show "lost" on screen
            font = pygame.font.Font(None, 74)
            text = font.render("Perdu", True, RED)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 50))

            # Draw the Start Again button
            pygame.draw.rect(screen, GREEN, (400, 225, 200, 50))
            font = pygame.font.Font(None, 36)
            text = font.render("    Start Again", True, BLACK)
            screen.blit(text, (410, 235))

        # Update the display
        pygame.display.flip()
        # Set the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()
