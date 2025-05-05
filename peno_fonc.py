import pygame, json, math, random
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

#Initialize sounds
soundeffect_clicked = pygame.mixer.Sound("assets/Common/Sounds/clicked.mp3")
soundeffect_kick = pygame.mixer.Sound("assets/Football/Sounds/ball_kicked.mp3")
soudeffect_hit = pygame.mixer.Sound("assets/Football/Sounds/validate_force.mp3")
soundeffect_net = pygame.mixer.Sound("assets/Football/Sounds/net.mp3")
soundeffect_cheer = pygame.mixer.Sound("assets/Football/Sounds/cheers.mp3")
soundeffect_lose = pygame.mixer.Sound("assets/Football/Sounds/awww.mp3")

# Boolean for loss
game_over_lose = False

# Boolean for win
game_over_win = False

#1 if ball was launched, else 0
number_target = 0

#Boolean that tells if the ball is at the target
ball_at_target = False

#Says if the strength is locked
locked = False

#Angle of keeper
clockwise = True

#Function to run the program
def run():

    #Global Setup
    global game_over_lose,game_over_win, clockwise,number_target,ball_at_target,locked
    pygame.display.set_caption("EfreiSport - Penalty")

    #Class for football
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
            self.z = 1
            self.strength_force = 0.2
            self.increase = True
            self.offsetx = 0
            self.offsety = 0
            self.force_velocity = 0.02

        def strength(self):
            if self.increase:
                self.strength_force += self.force_velocity
            elif not self.increase:
                self.strength_force -= self.force_velocity
            if self.strength_force >= 1:
                self.increase = False
            elif self.strength_force <= 0.2:
                self.increase = True

        def random_factor(self):
            angle = random.randint(0, 360)
            self.offsetx = math.cos(math.radians(angle)) * random.uniform(0.2,self.strength_force)*110
            self.offsety = math.sin(math.radians(angle)) * random.uniform(0.2,self.strength_force)*110
            print(self.offsetx,self.offsety)

        def draw(self, number_target,ball_at_target,locked,surface=screen):
            if number_target == 0:

                pygame.draw.circle(surface,(100, 210, 255), (500,440), 17+self.strength_force*100, 2)
            elif number_target == 1 and not ball_at_target and locked: #Statement to change the ball's size when kicked
                football.z -= 0.005
                football.image = pygame.transform.smoothscale(football.image, (50 * football.z,50 * football.z))
            surface.blit(self.image, self.rect)

    #Class for keeper
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
            self.mask = pygame.mask.from_surface(self.image)
            self.z = 20

            #Keeper's hitbox
            self.hitbox_surface = pygame.Surface((40, 150), pygame.SRCALPHA)
            pygame.draw.rect(self.hitbox_surface, (255, 0, 0, 150), self.hitbox_surface.get_rect())

        def draw(self, surface=screen):
            surface.blit(self.image_rot, self.rect)
            '''pygame.draw.circle(surface, blue_shade, self.rect_pos, 5)'''
            #Show the keeper's hitbox
            rotated_hitbox = pygame.transform.rotate(self.hitbox_surface, self.angle)
            hitbox_rect = rotated_hitbox.get_rect(center=(self.x, self.y))
            surface.blit(rotated_hitbox, hitbox_rect)

        def rotate_keeper(self,clockwise,ball_at_target):   #Rotation of keeper
            if not ball_at_target:
                if clockwise:
                    self.angle = self.angle + self.rotation_speed
                if not clockwise:
                    self.angle = self.angle - self.rotation_speed
                rotated_image = pygame.transform.rotate(self.image, self.angle)
                self.image_rot = rotated_image
                self.rect = self.image_rot.get_rect(center=(self.x,self.y))
                self.rect_pos = (500 - self.angle - pygame.Vector2(10,0).rotate(self.angle)[0],263 - pygame.Vector2(0, 100).rotate(self.angle)[1])
                self.x = self.rect_pos[0]
                self.y = self.rect_pos[1]
                self.mask = pygame.mask.from_surface(self.image_rot)
            elif ball_at_target:
                rotated_image = pygame.transform.rotate(self.image, self.angle)
                self.image_rot = rotated_image
                self.rect = self.image_rot.get_rect(center=(self.x, self.y))
                self.rect_pos = (500 - self.angle - pygame.Vector2(10, 0).rotate(self.angle)[0],263 - pygame.Vector2(0, 100).rotate(self.angle)[1])
                self.x = self.rect_pos[0]
                self.y = self.rect_pos[1]
                self.mask = pygame.mask.from_surface(self.image_rot)

    #Class for football's target
    class Target(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.x = 500
            self.y = 440
            self.pos = (self.x, self.y)
        def draw(self, surface=screen):
            pygame.draw.circle(surface,blue_shade,self.pos,5)

    #Assign game difficulty level
    class Level(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.x1 = 260
            self.y1 = 13
            self.x2 = 455
            self.y2 = 13
            self.x3 = 650
            self.y3 = 13
            self.chosen = "Easy"
            #if event.pos[0] >= self.x1 and event.pos[0] <= self.x1+90 and event.pos[1] >= self.y1 and event.pos[1] <= self.y1+30:
            #    self.chosen = "Easy"
            #elif event.pos[0] >= self.x2 and event.pos[0] <= self.x2+90 and event.pos[1] >= self.y2 and event.pos[1] <= self.y2+30:
            #    self.chosen = "Medium"
            #elif event.pos[0] >= self.x3 and event.pos[0] <= self.x3+90 and event.pos[1] >= self.y3 and event.pos[1] <= self.y3+30:
            #    self.chosen = "Hard"
        def draw(self, surface=screen):
            if self.chosen == "Easy":
                pygame.draw.rect(surface, blue_efrei, pygame.Rect(self.x1-5, self.y1-3, 100, 36))
            pygame.draw.rect(surface, GREEN, pygame.Rect(self.x1, self.y1, 90, 30))
            if self.chosen == "Medium":
                pygame.draw.rect(surface, blue_efrei, pygame.Rect(self.x2-5, self.y2-3, 100, 36))
            pygame.draw.rect(surface, blue_shade, pygame.Rect(self.x2, self.y2, 90, 30))
            if self.chosen == "Hard":
                pygame.draw.rect(surface, BLACK, pygame.Rect(self.x3-5, self.y3-3, 100, 36))
            pygame.draw.rect(surface, blue_efrei, pygame.Rect(self.x3, self.y3, 90, 30))
            font = pygame.font.Font(None, 30)
            text1 = font.render("Easy", True, BLACK)
            text2 = font.render("Medium", True, BLACK)
            text3 = font.render("Hard", True, BLACK)
            surface.blit(text1, (self.x1+23, self.y1 +5))
            surface.blit(text2, (self.x2+7, self.y2 +5))
            surface.blit(text3, (self.x3+23, self.y3 +5))

    # Function to reset the game
    def reset_game():
        global game_over_lose,game_over_win,number_target,clockwise,ball_at_target,locked
        game_over_lose = False
        game_over_win = False
        locked = False
        number_target = 0
        clockwise = True
        ball_at_target = False
        football.image = pygame.image.load("assets/Football/ball.png")
        football.x = 500
        football.y = 440
        football.z = 1
        football.rect.center = (500, 440)
        target.pos = football.rect.center
        target.x =football.x
        target.y =football.y
        keeper.angle = 0

    #Assignment of objects
    football = Ball()
    keeper = Goalkeeper()
    target = Target()
    difficulty = Level()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if game_over_lose or game_over_win:
                        # Check if the "Start Again" button is clicked
                        if 400 <= event.pos[0] <= 600 and 285 <= event.pos[1] <= 335:
                            reset_game()
                    elif event.pos[0] >= difficulty.x1 and event.pos[0] <= difficulty.x1+90 and event.pos[1] >= difficulty.y1 and event.pos[1] <= difficulty.y1+30:
                        soundeffect_clicked.play()
                        if difficulty.chosen != "Easy":
                            difficulty.chosen = "Easy"
                            keeper.rotation_speed = 1
                            football.force_velocity = 0.02
                            reset_game()
                    elif event.pos[0] >= difficulty.x2 and event.pos[0] <= difficulty.x2+90 and event.pos[1] >= difficulty.y2 and event.pos[1] <= difficulty.y2+30:
                        soundeffect_clicked.play()
                        if difficulty.chosen != "Medium":
                            difficulty.chosen = "Medium"
                            keeper.rotation_speed = 1.75
                            football.force_velocity = 0.05
                            reset_game()
                    elif event.pos[0] >= difficulty.x3 and event.pos[0] <= difficulty.x3+90 and event.pos[1] >= difficulty.y3 and event.pos[1] <= difficulty.y3+30:
                        soundeffect_clicked.play()
                        if difficulty.chosen != "Hard":
                            difficulty.chosen = "Hard"
                            keeper.rotation_speed = 3.5
                            football.force_velocity = 0.1
                            reset_game()
                    elif target.x == football.x and target.y == football.y and number_target == 0 and not locked:
                        soudeffect_hit.play()
                        locked = True
                    elif target.x == football.x and target.y == football.y and number_target == 0:
                        soundeffect_kick.play()
                        #See if player locked target
                        football.random_factor()
                        target.x = event.pos[0] + football.offsetx
                        target.y = event.pos[1] + football.offsety
                        target.pos = (target.x, target.y)
                        number_target += 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Exit"


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
        difficulty.draw()
        target.draw()
        if not game_over_lose and not game_over_win:
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

            if target.x == football.x and target.y == football.y and number_target == 1:
                ball_at_target = True

            # Rotate keeper
            if keeper.angle >= 90 or keeper.angle <= -90:
                temp = clockwise
                clockwise = not temp
            keeper.rotate_keeper(clockwise,ball_at_target)

            # Draw the keeper at new position
            keeper.draw()

            # Draw football at new position
            football.rect.center = (football.x, football.y)
            if not locked:
                football.strength()
            football.draw(number_target,ball_at_target,locked)

            keeper.rect.update(keeper.x - 10, keeper.y - 10, 20, 20)
            rotated_hitbox = pygame.transform.rotate(keeper.hitbox_surface, keeper.angle)
            hitbox_rect = rotated_hitbox.get_rect(center=(keeper.x, keeper.y))
            if football.rect.colliderect(hitbox_rect) and ball_at_target:
                soundeffect_lose.play()
                game_over_lose = True
            elif not football.rect.colliderect(hitbox_rect) and ball_at_target and football.x >= 310 and football.x <= 696 and football.y >= 72 and football.y <= 262:
                soundeffect_net.play()
                soundeffect_cheer.play()
                game_over_win = True
            elif ball_at_target:
                soundeffect_lose.play()
                game_over_lose = True

        else:
            keeper.rotate_keeper(clockwise, ball_at_target)
            keeper.draw()
            football.draw(number_target,ball_at_target,locked)
            # Show "lost" on screen
            if game_over_lose:
                font = pygame.font.Font(None, 90)
                text = font.render("Loss...", True, BLACK)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 50))
            elif game_over_win:
                font = pygame.font.Font(None, 90)
                text = font.render("Win!", True, BLACK)
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 50))
            # Draw the Start Again button
            pygame.draw.rect(screen, GREEN, (400, 285, 200, 50))
            font = pygame.font.Font(None, 36)
            text = font.render("    Start Again", True, BLACK)
            screen.blit(text, (410, 295))

        # Update the display
        pygame.display.flip()
        # Set the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()