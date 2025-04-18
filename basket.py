from trace import Trace

import pygame, math, time
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

clock = pygame.time.Clock()

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

    def circle_collision(self, other_sprite):
        dx = self.rect.centerx - other_sprite.rect.centerx
        dy = self.rect.centery - other_sprite.rect.centery
        distance = math.hypot(dx, dy)
        other_radius = other_sprite.radius
        return distance < (self.radius + other_radius)

    def init_trajectory_equation(self, velocity, angle, x0, y0):
        self.x_coeff = (math.cos(angle) * velocity, x0)
        self.y_coeff = (0.5 * G, -math.sin(angle) * velocity, y0)
        self.time = 0

    def change_trajectory_equation(self, bounce_coeff, angle, x0, y0):
        self.x_coeff = (self.velocity * math.cos(angle), x0)
        self.y_coeff = (0.5 * G, -self.velocity * math.sin(angle), y0)
        self.time = 0

    def hoop_collision(self):
        if self.rect.bottom > hoop_detector.rect.top and self.velocity > 0:
            if self.circle_collision(hoop_detector):
                if not self.scored:
                    score.increment()
                    self.scored = True


    def reset_position(self):
        # Reset ball position and state after scoring
        self.rect.center = (150, 400)
        self.velocity = 0
        self.launched = False
        self.time = 0
        self.angle = 0
        self.scored = False
        self.x_coeff = (0, ball.rect.centerx)
        self.y_coeff = (0, 0, ball.rect.centery)

    def collision(self, walls_list):
        for wall in walls_list:
            if self.rect.inflate(1, 1).colliderect(wall.rect):
                dx = min(abs(self.rect.right - wall.rect.left), abs(self.rect.left - wall.rect.right))
                dy = min(abs(self.rect.bottom - wall.rect.top), abs(self.rect.top - wall.rect.bottom))
                ldiff = self.rect.left - wall.rect.right
                rdiff = self.rect.right - wall.rect.left
                bdiff = self.rect.bottom - wall.rect.top
                tdiff =  self.rect.top - wall.rect.bottom
                if dx < dy:  # Vertical collision
                    self.angle = math.pi + self.angle
                elif dy < dx:  # Horizontal collision
                    self.angle = -self.angle
                else:  # Corner collision
                    self.angle += math.pi
                self.velocity *= bounce_coeff
                if self.velocity < 5:
                    self.reset_position()
                else:
                    self.unstuck(min(dx, dy) + 1, ldiff, rdiff, bdiff, tdiff, dx, dy, wall)
                    self.change_trajectory_equation(self.velocity, self.angle, self.rect.centerx, self.rect.centery)
                return True
        return False

    def unstuck(self, change, ld, rd, bd, td, dx, dy, wall):
        if self.rect.right > wall.rect.left and dx<=dy and abs(rd)<abs(ld):
            self.rect.center = (self.rect.center[0] - change, self.rect.center[1])
        elif self.rect.left < wall.rect.right and dx<=dy and abs(ld)<abs(rd):
            self.rect.center = (self.rect.center[0] + change, self.rect.center[1])
        elif self.rect.bottom > wall.rect.top and dx>dy and abs(bd)<abs(td):
            self.rect.center = (self.rect.center[0], self.rect.center[1] - change)
        elif self.rect.top < wall.rect.bottom and dx>dy and abs(td)<abs(bd):
            self.rect.center = (self.rect.center[0], self.rect.center[1] + change)

    def update_pos(self):
        self.rect.center = self.x_coeff[0] * self.time + self.x_coeff[1], self.y_coeff[0] * (self.time**2) + self.y_coeff[1] * self.time + self.y_coeff[2]
        self.velocity = math.sqrt((math.cos(self.angle) * self.velocity) ** 2 + (math.sin(self.angle) * self.velocity) ** 2)
        self.time += dt

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Hoop(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("assets/Basket/wall_net.png")
        self.image = pygame.transform.scale(img,(200,164))
        self.rect = self.image.get_rect()
        self.rect.center = (885,250)

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

    def draw(self, surface=screen):
        if self.visible:
            pygame.draw.rect(surface, self.color, self.rect)

class Hoop_detector(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.color=(0, 0, 0)
        self.x=x
        self.y=y
        self.width=85
        self.height=5
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.rect=self.image.get_rect()
        self.rect.center= (x,y)
        self.radius = min(self.width, self.height) // 2

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

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,(self.x,self.y,self.width,self.height))

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.font = pygame.font.Font("assets/Common/font.ttf", 28)

    def increment(self):
        self.score += 1

    def reset(self):
        self.score = 0

    def draw(self, surface=screen):
        text = self.font.render(f"Points: {self.score}", True, blue_efrei)
        surface.blit(text, (10, 10))

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

    def draw(self, surface):
        pygame.draw.rect(surface, blue_efrei, self.rect.inflate(6, 6))
        pygame.draw.rect(surface, white, self.rect)
        pygame.draw.rect(surface, black, self.slider_rect)

    def move(self):
        if not self.rect.y < self.slider_rect.y < self.rect.y + self.rect.height - self.slider_rect.height:
            self.speed = - self.speed
        self.slider_rect.y += self.speed

    def get_value(self):
        min_y = self.rect.top
        max_y = self.rect.bottom - self.slider_rect.height
        return int(100 - (((self.slider_rect.y - min_y) / (max_y - min_y)) * 100)) + int(10 * ((self.slider_rect.y - min_y) / (max_y - min_y)))

class Launch(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(17, 396, 50, 80)
        self.color = white

    def draw(self, surface=screen):
        pygame.draw.rect(surface, blue_efrei, self.rect.inflate(6, 6))
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 45)
        text = font.render("Go!", True, blue_efrei)
        surface.blit(text, (self.rect.x, self.rect.y + 30))

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
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

        if self.number == 1:
            enable_middle_wall = False
            if enable_middle_wall:
                self.level_walls.append(Wall(400, 212.5, 6, 150, False, True))

        elif self.number == 2:
            self.level_walls.append(Wall(150, 212.5, 6, 200, False, True))
            self.level_walls.append(Wall(750, 212.5, 6, 200, False, True))

        self.all_walls = border_walls + self.level_walls

#Object initialization
ball = Ball()
hoop = Hoop()
score=Score()
slider = Slider()
arrow = Arrow()
launch_button = Launch()
hoop_detector = Hoop_detector(840,270)


bordertop = Wall(0, 0, 900, 6, True, True)
borderbottom = Wall(0, 425, 900, 6, True, True)
borderleft = Wall(0, 0, 6, 425, True, True)
borderright = Wall(900, 0, 6, 431, True, True)
hoop_border1 = Wall(857,175,25,120, False,False)
hoop_border2 = Wall(825,217,2,22, False, False)
hoop_border3 = Wall(705,217,2,22, False, False)
border_walls = [bordertop, borderbottom, borderleft, borderright, hoop_border1, hoop_border2, hoop_border3]

level = Level(actual_level)

# Create the scene and add the walls
scene = Scene()
scene.add_object(bordertop)
scene.add_object(borderleft)
scene.add_object(borderright)
scene.add_object(borderbottom)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            arrow.follow = not arrow.follow
        if not ball.launched:
            launch_button.clicked(event)


    screen.fill((240, 240, 240, 0.5))
    screen.blit(bg, (0, 0))
    screen.blit(windowbg,getrelativepos((0,0)))

    if ball.velocity>0 and ball.time > dt:
        ball.collision(level.all_walls)

    for wall in level.all_walls:
        wall.draw()

    if ball.launched:
        ball.update_pos()
    else:
        arrow.draw(screen)
        slider.draw(screen)
        launch_button.draw()
        arrow.update_direction(pygame.mouse.get_pos())
        ball.angle = -arrow.angle
        slider.move()

    ball.hoop_collision()
    ball.draw(screen)
    hoop.draw(screen)
    scene.draw(screen)
    score.draw(screen)

    # Update the display
    pygame.display.flip()
    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()