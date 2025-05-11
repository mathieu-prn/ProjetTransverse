from trace import Trace

import pygame, math, time
from pyexpat.errors import messages

import utility
from utility import getrelativepos

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport - Basketball")
bg = pygame.image.load("assets/Common/Background.png")
windowbg = pygame.transform.scale(pygame.image.load("assets/Basket/bg.png"), (900, 425))
pygame_icon = pygame.image.load('assets/Common/logo.png')
pygame.display.set_icon(pygame_icon)

actual_level = 1

# Initialize Colors
black = (0, 0, 0)
white = (255, 255, 255)
red=(255,0,0)
blue_efrei=(18,121,190)
grey=(211,211,211)

# Initialize constants
G = 9.81
dt = 1/10
PI = math.pi
bounce_coeff = 0.7

#Initialize sounds
soundeffect_clicked = pygame.mixer.Sound("assets/Common/Sounds/clicked.mp3")
soundeffect_bounce = pygame.mixer.Sound("assets/Basket/Sounds/bounce.mp3")
soundeffect_inthebasket = pygame.mixer.Sound("assets/Basket/Sounds/inthebasket.mp3")

soundeffect_clicked.set_volume(0.5)

clock = pygame.time.Clock()

def run(): # Main function, called in the menu (game_select.py)


    class Ball(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load("assets/Basket/BasketBall.png")
            self.image = pygame.transform.scale(img, (45, 45))
            self.rect = self.image.get_rect()
            self.rect.center = (150, 400)
            self.scored = False
            self.velocity = 0
            self.angle = 0
            self.x_coeff = (0, self.rect.center[0])
            self.y_coeff = (0, 0, self.rect.center[1])
            self.time = 0
            self.radius = self.rect.width // 2
            self.launched = False
            self.player = score1

        #intialize coefficients for the trajectory equation
        def init_trajectory_equation(self, velocity, angle, x0, y0):
            self.x_coeff = (math.cos(angle) * velocity, x0)
            self.y_coeff = (0.5 * G, -math.sin(angle) * velocity, y0)
            self.time = 0

        #change coefficients on collision with a wall (make it bounce)
        def change_trajectory_equation(self, bounce_coeff, angle, x0, y0):
            self.x_coeff = (self.velocity * math.cos(angle), x0)
            self.y_coeff = (0.5 * G, -self.velocity * math.sin(angle), y0)
            self.time = 0

        #checks if there is a collision with the rect that detects a score
        def hoop_collision(self):
            if self.rect.bottom > hoop_detector.rect.top and self.velocity > 0:
                if self.rect.colliderect(hoop_detector):
                    if not self.scored:
                        self.player.increment()
                        soundeffect_inthebasket.play()
                        self.scored = True

        #resets position and coefficients
        def reset_position(self):
            # Reset ball position and state after scoring
            self.rect.center = (150, 400)
            self.velocity = 0
            self.launched = False
            self.time = 0
            self.angle = 0
            arrow.direction = pygame.Vector2(1, 0)
            arrow.follow = True
            self.x_coeff = (0, ball.rect.centerx)
            self.y_coeff = (0, 0, ball.rect.centery)

        #checks if the ball collides with a wall
        def collision(self, walls_list):
            for wall in walls_list:
                if self.rect.inflate(1, 1).colliderect(wall.rect):
                    #Counts the bounces
                    if not ball.scored:
                        self.player.bounces += 1
                    #Bounce sound
                    if self.velocity > 5 and self.time > 0.2:
                        soundeffect_bounce.play()
                    #Detects what type of collision
                    dx = min(abs(self.rect.right - wall.rect.left), abs(self.rect.left - wall.rect.right))
                    dy = min(abs(self.rect.bottom - wall.rect.top), abs(self.rect.top - wall.rect.bottom))
                    ldiff = self.rect.left - wall.rect.right
                    rdiff = self.rect.right - wall.rect.left
                    bdiff = self.rect.bottom - wall.rect.top
                    tdiff =  self.rect.top - wall.rect.bottom
                    if dx <= dy:  # Vertical collision
                        self.angle = math.pi + self.angle
                    elif dy < dx:  # Horizontal collision
                        self.angle = -self.angle
                    self.velocity *= bounce_coeff
                    if self.velocity < 5 and not ball.scored:
                            time.sleep(0.5)
                            self.reset_position()
                    else:
                        self.unstuck(min(dx, dy) + 1, ldiff, rdiff, bdiff, tdiff, dx, dy, wall)
                        self.change_trajectory_equation(self.velocity, self.angle, self.rect.centerx, self.rect.centery)
                    return True
            return False

        #moves the ball so it does not collide infintely and is stuck
        def unstuck(self, change, ld, rd, bd, td, dx, dy, wall):
            if self.rect.right > wall.rect.left and dx<=dy and abs(rd)<abs(ld):
                self.rect.center = (self.rect.center[0] - change, self.rect.center[1])
            elif self.rect.left < wall.rect.right and dx<=dy and abs(ld)<abs(rd):
                self.rect.center = (self.rect.center[0] + change, self.rect.center[1])
            elif self.rect.bottom > wall.rect.top and dx>dy and abs(bd)<abs(td):
                self.rect.center = (self.rect.center[0], self.rect.center[1] - change)
            elif self.rect.top < wall.rect.bottom and dx>dy and abs(td)<abs(bd):
                self.rect.center = (self.rect.center[0], self.rect.center[1] + change)

        #calculates the new position using the coefficients of the trajectory
        def update_pos(self):
            self.rect.center = self.x_coeff[0] * self.time + self.x_coeff[1], self.y_coeff[0] * (self.time**2) + self.y_coeff[1] * self.time + self.y_coeff[2]
            self.velocity = math.sqrt((math.cos(self.angle) * self.velocity) ** 2 + (math.sin(self.angle) * self.velocity) ** 2)
            self.time += dt

        #draws the object
        def draw(self, surface):
            surface.blit(self.image, self.rect)


    class Hoop(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            img = pygame.image.load("assets/Basket/wall_net.png")
            self.image = pygame.transform.scale(img,(200,164))
            self.rect = self.image.get_rect()
            self.rect.center = (885,250)

        #draws the object
        def draw(self, surface):
            surface.blit(self.image, self.rect)

    class Wall(pygame.sprite.Sprite):
        def __init__(self, relative_x, relative_y, width, height, is_border, visible):
            super().__init__()
            self.color = blue_efrei
            self.visible = visible
            if is_border:
                self.rect = pygame.Rect(relative_x + 80, relative_y + 55, width, height)
            else:
                self.rect = pygame.Rect(relative_x + 80 - width / 2, relative_y + 55 - height / 2, width, height)

        #draws the object
        def draw(self, surface=screen):
            if self.visible:
                pygame.draw.rect(surface, self.color, self.rect)

    class Hoop_detector(pygame.sprite.Sprite):
        def __init__(self, x,y):
            pygame.sprite.Sprite.__init__(self)
            self.color=(0, 0, 0)
            self.x=x
            self.y=y
            self.width=105
            self.height=5
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.image.fill(self.color)
            self.rect=self.image.get_rect()
            self.rect.center= (x,y)

        #draws the object
        def draw(self, surface):
            pygame.draw.rect(surface, self.color, self.rect)


    class Hoop_border(pygame.sprite.Sprite):
        def __init__(self,x,y,width,height):
            pygame.sprite.Sprite.__init__(self)
            self.color=(0,0,0)
            self.x=x
            self.y=y
            self.width=width
            self.height=height

        #draws the object
        def draw(self,surface):
            pygame.draw.rect(surface,self.color,(self.x,self.y,self.width,self.height))

    class Score(pygame.sprite.Sprite):
        def __init__(self, x, y, name, color):
            super().__init__()
            self.score = 0
            self.bounces = 0
            self.new_score = 0
            self.color = color
            self.position = (x, y)
            self.level = 1
            self.name = name
            self.font = pygame.font.Font("assets/Common/font.ttf", 28)

        #calculates the score depending on the number of bounces
        def increment(self):
            if self.bounces == 0:
                self.new_score = 10
            elif self.bounces == 1:
                self.new_score = 8
            elif 2<=self.bounces<=4:
                self.new_score = 5
            elif 5<=self.bounces<=10:
                self.new_score = 3
            elif 11<=self.bounces<=20:
                self.new_score = 2
            else:
                self.new_score = 1
            self.score += self.new_score

        #resets score
        def reset(self):
            self.score = 0

        #draws the object
        def draw(self, surface=screen):
            text = self.font.render(f"Points: {self.score}", True, self.color)
            surface.blit(text, self.position)

    class Player(pygame.sprite.Sprite):
        def __init__(self, name, color):
            super().__init__()
            self.name = name
            self.color = color
            self.position = (400, 10)
            self.font = pygame.font.Font("assets/Common/font.ttf", 28)

        #draws object
        def draw(self, surface=screen):
            text = self.font.render(f"{self.name}'s turn", True, self.color)
            surface.blit(text, self.position)

    #Associate all the different rectangles of the Hoop
    class Scene:
        def __init__(self):
            self.objects = []

        def add_object(self, obj):
            self.objects.append(obj)

        def draw(self, surface):
            for obj in self.objects:
                obj.draw(surface)

    class Slider(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.rect = pygame.Rect(25, 150, 30, 200)
            self.slider_rect = pygame.Rect(25, 151, 30, 7)
            self.speed = 3

        #draws object
        def draw(self, surface):
            pygame.draw.rect(surface, blue_efrei, self.rect.inflate(6, 6))
            pygame.draw.rect(surface, white, self.rect)
            pygame.draw.rect(surface, black, self.slider_rect)

        #moves slider automatically
        def move(self):
            if not self.rect.y < self.slider_rect.y < self.rect.y + self.rect.height - self.slider_rect.height:
                self.speed = - self.speed
            self.slider_rect.y += self.speed

        #calculates the value of the slider
        def get_value(self):
            min_y = self.rect.top
            max_y = self.rect.bottom - self.slider_rect.height
            return int(125 - (((self.slider_rect.y - min_y) / (max_y - min_y)) * 125)) + int(10 * ((self.slider_rect.y - min_y) / (max_y - min_y)))

    class Launch(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.rect = pygame.Rect(17, 396, 50, 80)
            self.color = white

        # draws object
        def draw(self, surface=screen):
            pygame.draw.rect(surface, blue_efrei, self.rect.inflate(6, 6))
            pygame.draw.rect(surface, self.color, self.rect)
            font = pygame.font.Font(None, 45)
            text = font.render("Go!", True, blue_efrei)
            surface.blit(text, (self.rect.x, self.rect.y + 30))

        #launches the ball by passing the angle and speed value and calculating coeffs
        def clicked(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    soundeffect_clicked.play()
                    self.color = grey
                    ball.velocity = (slider.get_value()/100) * 120
                    ball.init_trajectory_equation(ball.velocity, ball.angle, ball.rect.center[0], ball.rect.center[1])
                    ball.launched = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.color = white

    class Arrow(pygame.sprite.Sprite):
        def __init__(self, length=50):
            super().__init__()
            self.length = length
            self.direction = pygame.Vector2(1, 0)
            self.angle = 0
            self.follow = True

        # draws object
        def draw(self, surface):
            arrow_end = pygame.Vector2(ball.rect.center) + self.direction * (20 + slider.get_value())
            pygame.draw.line(surface, blue_efrei, ball.rect.center, arrow_end, 3)
            self.angle = math.atan2(self.direction.y, self.direction.x)
            arrow_angle = math.atan2(-self.direction.y, -self.direction.x)
            arrow_size = 10
            left = (arrow_end.x + arrow_size * math.cos(arrow_angle + math.pi / 6),
                    arrow_end.y + arrow_size * math.sin(arrow_angle + math.pi / 6))
            right = (arrow_end.x + arrow_size * math.cos(arrow_angle - math.pi / 6),
                     arrow_end.y + arrow_size * math.sin(arrow_angle - math.pi / 6))
            pygame.draw.polygon(surface, blue_efrei, [arrow_end, left, right])

        #calculates the angle depending on the arrow
        def update_direction(self, mouse_pos):
            if arrow.follow:
                direction = pygame.Vector2(mouse_pos) - pygame.Vector2(ball.rect.center)
                if direction.length() > 0:
                    self.direction = direction.normalize()
                    self.angle = math.atan2(self.direction.y, self.direction.x)

    class Level(pygame.sprite.Sprite):
        def __init__(self, number):
            super().__init__()
            self.number = number
            self.level_walls = []    # Level-specific walls

            #adds wall depending on level
            if self.number == 1:
                pass
            elif self.number == 2:
                self.level_walls.append(Wall(400, 212.5, 6, 100, False, True))
            elif self.number == 3:
                self.level_walls.append(Wall(400, 50, 6, 100, False, True))
                self.level_walls.append(Wall(400, 300, 6, 250, False, True))
            elif self.number == 4:
                self.level_walls.append(Wall(500, 150, 100, 6, False, True))
                self.level_walls.append(Wall(650, 200, 100, 6, False, True))

            self.all_walls = border_walls + self.level_walls

    #Object initialization

    class Message(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.font = pygame.font.Font("assets/Common/font.ttf", 28)
            self.fontcolor = blue_efrei
            self.button_width = 150
            self.button_height = 50
            self.button_pos = (500 - self.button_width / 2, 275)
            self.button_color = white
            self.button_rect = pygame.Rect(self.button_pos, (self.button_width, self.button_height))

        # shows info messages
        def draw(self, msg_type, surface=screen):
            self.fontcolor = ball.player.color
            if msg_type == "next":
                if ball.player.bounces == 0:
                    msg = f"You scored without any bounce! Congratulations! You scored {ball.player.new_score}/10 points."
                else:
                    msg = f"You won in {ball.player.bounces} bounces! You scored {ball.player.new_score}/10 points."
                button_msg = "Next player"
            elif msg_type == "end":
                msg = f"Congratulations, {score1.name if score1.score>score2.score else score2.name}! You won!"
                button_msg = "Ok"
            else:
                msg = "Message not defined"
                button_msg = "OK"

            #Draw
            text = self.font.render(msg, True, self.fontcolor)
            text_width, text_height = text.get_size()
            surface.blit(text, (surface.get_width() / 2 - text_width / 2, surface.get_height() / 2 - text_height / 2))
            pygame.draw.rect(surface, black, self.button_rect.inflate(6, 6))
            pygame.draw.rect(surface, self.button_color, self.button_rect)

            button_text = self.font.render(button_msg, True, black)

            #Below is to center the text in the button
            tbutton_width, tbutton_height = button_text.get_size()
            tbuttonx=self.button_pos[0]+((self.button_width-tbutton_width)/2)
            tbuttony=self.button_pos[1]+((self.button_height-tbutton_height)/2)
            surface.blit(button_text,(tbuttonx, tbuttony)) #Draw the text

        #passes to the next player
        def clicked(self, event):
            global display_msg
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    soundeffect_clicked.play()
                    if ball.scored:
                        ball.player.level += 1
                        ball.reset_position()
                        ball.scored = False
                        ball.player.bounces = 0
                        ball.player.new_score = 0
                        if ball.player == score1:
                            ball.player = score2
                        else:
                            ball.player = score1
                    else:
                        pass
                    display_msg = False
            elif event.type == pygame.MOUSEBUTTONUP:
                self.button_color = white

    #Initializing game objects
    score1=Score(10, 10, "Player 1", blue_efrei)
    score2=Score(850, 10, "Player 2", red)
    ball = Ball()
    hoop = Hoop()
    slider = Slider()
    arrow = Arrow()
    launch_button = Launch()
    hoop_detector = Hoop_detector(841,270)

    #Initializing basic walls
    bordertop = Wall(0, 0, 900, 6, True, True)
    borderbottom = Wall(0, 425, 900, 6, True, True)
    borderleft = Wall(0, 0, 6, 425, True, True)
    borderright = Wall(900, 0, 6, 431, True, True)
    hoop_border1 = Wall(857,175,25,120, False,False)
    hoop_border2 = Wall(825,217,2,22, False, False)
    hoop_border3 = Wall(705,217,2,22, False, False)
    hoop_walls = [hoop_border2, hoop_border3]
    border_walls = [bordertop, borderbottom, borderleft, borderright, hoop_border1]

    #Initializing info objects
    level = Level(score1.level)
    message = Message()
    player = Player(score1.name, score1.color)

    # Create the scene and add the walls
    scene = Scene()
    scene.add_object(bordertop)
    scene.add_object(borderleft)
    scene.add_object(borderright)
    scene.add_object(borderbottom)

    # Game loop
    running = True
    while running:
        #Updates current level and player
        level = Level(ball.player.level)
        player = Player(ball.player.name, ball.player.color)

        #Event detection
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                arrow.follow = not arrow.follow
            if not ball.launched:
                launch_button.clicked(event)
            if ball.scored:
                message.clicked(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "Exit"

        #Screen drawing
        screen.fill((240, 240, 240, 0.5))
        screen.blit(bg, (0, 0))
        screen.blit(windowbg,getrelativepos((0,0)))

        #enables collision
        if ball.velocity>0 and ball.time > dt:
            ball.collision(level.all_walls)
            if not ball.scored:
                ball.collision(hoop_walls)

        #draws walls
        for wall in level.all_walls + hoop_walls:
            wall.draw()

        #draws some game objects if ball not launched
        if ball.launched:
            ball.update_pos()
        else:
            arrow.draw(screen)
            slider.draw(screen)
            launch_button.draw()
            arrow.update_direction(pygame.mouse.get_pos())
            ball.angle = -arrow.angle
            slider.move()

        #darws resting game objects
        ball.hoop_collision()
        ball.draw(screen)
        hoop.draw(screen)
        scene.draw(screen)
        score1.draw(screen)
        score2.draw(screen)
        player.draw()

        #checks if the game is finished or next player
        if ball.scored:
            if score1.level>4 and score2.level>=4:
                message.draw("end")
            else:
                message.draw("next")

        # Update the display
        pygame.display.flip()
        # Set the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()