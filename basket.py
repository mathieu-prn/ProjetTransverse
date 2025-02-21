import pygame, math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport - Basketball")
bg = pygame.image.load("assets/Background.png")
pygame_icon = pygame.image.load('assets/logo.png')
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
        self.rect.center = (100, 400)
        self.scored=False
        self.velocity = 0
        self.x_coeff = (0, self.rect.center[0])
        self.y_coeff = (0, 0, self.rect.center[1])
        self.time = 0
        self.launched = False

    def trajectory_equation(self, speed, angle, x0, y0):
        v_x = speed * math.cos(angle * math.pi/180)
        v_y = speed * math.sin(angle * math.pi/180)
        self.x_coeff = (v_x, x0)
        self.y_coeff = (0.5 * G, -v_y, y0)

    def hoop_collision(self):
        if self.rect.colliderect(hoop_detector.rect):
            if not self.scored:
                score.increment()
                self.scored = True
        if not self.rect.colliderect(hoop_detector.rect):
            self.scored = False

    def ground_collision(self):
        if self.rect.colliderect(borderbottom.rect):
            return True

    def update_pos(self):
        self.rect.center = self.x_coeff[0]*self.time + self.x_coeff[1], self.y_coeff[0]*(self.time**2) + self.y_coeff[1]*self.time + self.y_coeff[2]
        self.velocity = math.sqrt((math.cos(55) * self.velocity) ** 2 + (G * self.time + math.sin(55) * self.velocity) ** 2)
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

class Border(pygame.sprite.Sprite):
    def __init__(self,relative_x,relative_y,width,height,isborder):
        pygame.sprite.Sprite.__init__(self)
        self.color=blue_efrei
        self.x=relative_x
        self.y=relative_y
        self.width=width
        self.height=height
        #If it's a border, set the left corner position.
        if isborder:
            self.rect=pygame.Rect(self.x+80, self.y+55, self.width, self.height)
    def draw(self,surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Hoop_detector(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.color=(0, 0, 0)
        self.x=x
        self.y=y
        self.width=100
        self.height=10
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.rect=self.image.get_rect()
        self.rect.center= (x,y)

    def draw(self,surface):
        pygame.draw.rect(surface,self.color,(self.x, self.y, self.width, self.height))

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.font = pygame.font.Font("assets/font.ttf", 28)

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
        self.slider_rect = pygame.Rect(25, 250, 30, 7)
        self.dragging = False

    def draw(self, surface):
        pygame.draw.rect(surface, blue_efrei, self.rect.inflate(6, 6))
        pygame.draw.rect(surface, white, self.rect)
        pygame.draw.rect(surface, black, self.slider_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_rect.collidepoint(event.pos):
                self.dragging = True
            elif self.rect.collidepoint(event.pos):
                self.slider_rect.y = max(self.rect.top, min(event.pos[1], self.rect.bottom - self.slider_rect.height))
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.slider_rect.y = max(self.rect.top, min(event.pos[1], self.rect.bottom - self.slider_rect.height))

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
                ball.trajectory_equation(ball.velocity, 50, ball.rect.center[0], ball.rect.center[1])
                ball.launched = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.color = white

#Object initialization
ball = Ball()
hoop = Hoop()
score=Score()
slider = Slider()
launch_button = Launch()
hoop_detector= Hoop_detector(792,220)
bordertop=Border(0,0,900,6,True)
borderleft=Border(0,0,6,425,True)
borderbottom=Border(0,425,900,6,True)
borderright=Border(900,0,6,431,True)

# Create the scene and add the walls
scene = Scene()
scene.add_object(bordertop)
scene.add_object(borderleft)
scene.add_object(borderright)
scene.add_object(borderbottom)

ball.velocity = 90
angle = 50
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        slider.handle_event(event)
        launch_button.clicked(event)

    screen.fill((240, 240, 240, 0.5))
    screen.blit(bg, (0, 0))

    if ball.ground_collision():
        ball.trajectory_equation(bounce_coeff*ball.velocity, angle, ball.rect.center[0], ball.rect.center[1])
        ball.time = dt

    if ball.launched:
        ball.update_pos()

    ball.hoop_collision()

    hoop_detector.draw(screen)
    ball.draw(screen)
    hoop.draw(screen)
    scene.draw(screen)
    score.draw(screen)
    slider.draw(screen)
    launch_button.draw()

    # Update the display
    pygame.display.flip()
    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()