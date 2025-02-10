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
t = 0
PI = math.pi

clock = pygame.time.Clock()

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("assets/Basket/BasketBall.png")
        self.image = pygame.transform.scale(img, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (50, 400)

    def trajectory_equation(self, speed, angle, x0, y0):
        v_x = speed * math.cos(angle * math.pi/180)
        v_y = speed * math.sin(angle * math.pi/180)
        x = (v_x, x0)
        y = (0.5 * G, -v_y, y0)
        return x, y

    def calc_pos(self, x_coeff, y_coeff, time):
        new_x = x_coeff[0]*time + x_coeff[1]
        new_y = y_coeff[0]*(time**2) + y_coeff[1]*time + y_coeff[2]
        return (new_x, new_y)

    def collision(self,hoop):
        if pygame.Rect.colliderect(self.rect,hoop.rect):
            return True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Hoop(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("assets/Basket/wall_net.png")
        self.image = pygame.transform.scale(img,(190,156))
        self.rect = self.image.get_rect()
        self.rect.center = (890,200)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Wall(pygame.sprite.Sprite):
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

rect = pygame.Rect(200, 150, 100, 100)

#Associate all the different rectangles of the Hoop
class Scene:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)

#Object initialization
ball = Ball()
hoop = Hoop()
bordertop=Wall(0,0,900,6,True)
borderleft=Wall(0,0,6,425,True)
borderbottom=Wall(0,425,900,6,True)
borderright=Wall(900,0,6,431,True)
calc_eq = True

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

    screen.fill((240, 240, 240, 0.5))
    screen.blit(bg, (0, 0))

    if calc_eq:
        x_coeff, y_coeff = ball.trajectory_equation(100, 55, ball.rect.center[0], ball.rect.center[1])
        print(x_coeff, x_coeff)
        calc_eq = False


    if ball.rect.center[1]<500 and ball.rect.center[0]<1000:
        ball.rect.center = ball.calc_pos(x_coeff, y_coeff, t)

    if ball.collision(hoop):
        pygame.draw.rect(screen, blue_efrei, rect)

    ball.draw(screen)
    hoop.draw(screen)
    scene.draw(screen)
    # Update the display
    pygame.display.flip()
    t+=dt
    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()