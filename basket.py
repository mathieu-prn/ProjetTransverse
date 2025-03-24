import pygame, math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport - Basketball")
bg = pygame.image.load("assets/Common/Background.png")
pygame_icon = pygame.image.load('assets/Common/logo.png')
pygame.display.set_icon(pygame_icon)

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
        self.image = pygame.transform.scale(img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (150, 400)
        self.scored=False
        self.velocity = 0
        self.angle = 0
        self.x_coeff = (0, self.rect.center[0])
        self.y_coeff = (0, 0, self.rect.center[1])
        self.time = 0
        self.launched = False

    def init_trajectory_equation(self, velocity, angle, x0, y0):
        self.x_coeff = (math.cos(angle) * velocity, x0)
        self.y_coeff = (0.5 * G, -math.sin(angle) * velocity, y0)
        self.time = 0

    def change_trajectory_equation(self, bounce_coeff, angle, x0, y0):
        self.x_coeff = (self.velocity * math.cos(angle) , x0)
        self.y_coeff = (0.5 * G, -self.velocity * math.sin(angle), y0)
        self.time = 0

    def hoop_collision(self):
        if self.rect.bottom > hoop_detector.rect.top and self.velocity > 0:
            if self.rect.colliderect(hoop_detector.rect):
                if not self.scored:
                    score.increment()
                    self.scored = True
        if not self.rect.colliderect(hoop_detector.rect):
            self.scored = False

    def collision(self, walls_list):
        for wall in walls_list:
            if self.rect.inflate(5, 5).colliderect(wall.rect):
                dx = min(abs(self.rect.right - wall.rect.left), abs(self.rect.left - wall.rect.right))
                dy = min(abs(self.rect.bottom - wall.rect.top), abs(self.rect.top - wall.rect.bottom))
                if dx < dy:  # Vertical collision
                    self.angle = math.pi - self.angle
                    self.rect.x += 2 * math.cos(self.angle)
                elif dy < dx:  # Horizontal collision
                    self.angle = -self.angle
                    self.rect.y += 2 * math.sin(self.angle)
                else:  # Corner collision
                    self.angle += math.pi
                    self.rect.x += 2 * math.cos(self.angle)
                    self.rect.y += 2 * math.sin(self.angle)
                self.velocity *= bounce_coeff
                self.change_trajectory_equation(self.velocity, self.angle, self.rect.centerx, self.rect.centery)
                return True
        return False

    def unstuck(self):
        change = 20
        if self.rect.left < borderright.rect.left:
            self.rect.center = (self.rect.center[0] + change, self.rect.center[1])
        elif self.rect.right > borderleft.rect.right:
            self.rect.center = (self.rect.center[0] - change, self.rect.center[1])
        elif self.rect.top < borderbottom.rect.top:
            self.rect.center = (self.rect.center[0], self.rect.center[1] + change)
        elif self.rect.bottom > bordertop.rect.bottom:
            self.rect.center = (self.rect.center[0], self.rect.center[1] - change)

    def update_pos(self):
        self.rect.center = self.x_coeff[0]*self.time + self.x_coeff[1], self.y_coeff[0]*(self.time**2) + self.y_coeff[1]*self.time + self.y_coeff[2]
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
        self.rect.center = (885,200)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Wall(pygame.sprite.Sprite):
    def __init__(self, relative_x, relative_y, width, height, is_border):
        super().__init__()
        self.color = blue_efrei
        if is_border:
            self.rect = pygame.Rect(relative_x + 80, relative_y + 55, width, height)
        else:
            self.rect = pygame.Rect(relative_x + 80 - width / 2, relative_y + 55 - height / 2, width, height)

    def draw(self, surface=screen):
        pygame.draw.rect(surface, self.color, self.rect)


class Hoop_detector(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.color=(0, 0, 0)
        self.x=x
        self.y=y
        self.width=50
        self.height=5
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.rect=self.image.get_rect()
        self.rect.center= (x,y)

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,(self.x, self.y, self.width, self.height))

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

#Object initialization
ball = Ball()
hoop = Hoop()
score=Score()
slider = Slider()
arrow = Arrow()
launch_button = Launch()
hoop_detector = Hoop_detector(816,220)
hoop_border1 = Hoop_border(925,120,25,120)
hoop_border2 = Hoop_border(887,210,5,22)
hoop_border3 = Hoop_border(790,210,5,22)

bordertop = Wall(0, 0, 900, 6, True)
borderbottom = Wall(0, 425, 900, 6, True)
borderleft = Wall(0, 0, 6, 425, True)
borderright = Wall(900, 0, 6, 431, True)
border_walls = [bordertop, borderbottom, borderleft, borderright]

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
        launch_button.clicked(event)


    screen.fill((240, 240, 240, 0.5))
    screen.blit(bg, (0, 0))

    #if ball.wall_collision() and ball.time > 5*dt:
     #   print(ball.x_coeff, ball.y_coeff)
      #  print(bounce_coeff*ball.velocity)
       # ball.trajectory_equation(bounce_coeff,(ball.wall_collision()-1)*math.pi/2 + ball.angle, ball.rect.center[0], ball.rect.center[1])
        #print(ball.x_coeff, ball.y_coeff)
    print(ball.velocity)
    if ball.velocity>0 and ball.time > dt:
        ball.collision(border_walls)
        if ball.velocity < 10:
            ball.velocity = 0
            ball.x_coeff = (0, ball.rect.centerx)
            ball.y_coeff = (0, 0, ball.rect.centery)
        ball.unstuck()
    print(ball.x_coeff, ball.y_coeff)

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
    hoop_border1.draw(screen)
    hoop_border2.draw(screen)
    hoop_border3.draw(screen)
    # Update the display
    pygame.display.flip()
    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()