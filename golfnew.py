import pygame, sys, math
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport - Golf")

# Initialize Colors
black = (0, 0, 0)
white = (255, 255, 255)
red=(255,0,0)
blue_efrei=(18,121,190)
grey=(211,211,211)


clock = pygame.time.Clock()

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("assets/GolfBall.png")
        self.image = pygame.transform.scale(img, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = (110, 267.5)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Slider(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.X = 25
        self.Y = 250
        self.rect = pygame.Rect(25, 150, 30, 200)
        self.slider_rect = pygame.Rect(self.X, self.Y, 30, 5)
        self.dragging = False

    def draw(self):
        pygame.draw.rect(screen, blue_efrei, self.rect.inflate(6, 6))
        pygame.draw.rect(screen, white, self.rect)
        pygame.draw.rect(screen, black, pygame.Rect(self.X, self.Y, 30, 5))
        font = pygame.font.Font(None, 36)
        text = font.render(f"Value: {slider.get_value()}", True, blue_efrei)
        screen.blit(text, (10, 10))

    def handle_event(self, event):
        """Handles mouse events to move the slider."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.Y = max(self.rect.top, min(event.pos[1], self.rect.bottom - 5))
            self.slider_rect.y = self.Y

    def get_value(self):
        """Returns a value between 1 and 100 based on slider position."""
        min_y = self.rect.top
        max_y = self.rect.bottom - 5
        return int(100 - ((self.Y - min_y-1) / (max_y - min_y+1)) * 100)

class Launch(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x=17
        self.y=396
        self.width=50
        self.height=80
        self.color= white
        self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
    def draw(self,screen):
        pygame.draw.rect(screen, blue_efrei, self.rect.inflate(6, 6))
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 45)
        text = font.render(f"Go!", True, blue_efrei)
        screen.blit(text, (self.x, self.y+30))
    def clicked(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.color= grey
        elif event.type == pygame.MOUSEBUTTONUP:
            self.color= white


class Field(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("assets/GolfField.png")
        self.rect=self.image.get_rect()
        self.pos=(80,55)
    def draw(self, surface):
        surface.blit(self.image, self.pos)

class Wall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color=blue_efrei
    def draw(self, screen,width, height,x,y):
        pygame.draw.rect(screen, self.color, pygame.Rect(width, height, x, y))

class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("assets/GolfBall.png")
        self.image = pygame.transform.scale(img, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = (int(ball.rect.center[0]) + 40, 267.5)
        self.angle = 0
        self.rotation_speed = 0.1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def follow_mouse(self,follow):
        if follow:

        # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

        # Determine the direction of the mouse relative to the ball
            mouse_dx = mouse_x - ball.rect.center[0]
            mouse_dy = mouse_y - ball.rect.center[1]
            target_angle = math.atan2(mouse_dy, mouse_dx)

        # Adjust the angle of the arrow based on mouse position
            if target_angle > self.angle+0.1:
                self.angle += self.rotation_speed
            elif target_angle < self.angle-0.1:
                self.angle -= self.rotation_speed

        # Calculate new position for the arrow
            self.rect.center = (ball.rect.center[0] + 40 * math.cos(self.angle),ball.rect.center[1] + 40 * math.sin(self.angle))

    def validate_position(self,event,follow):
        if pygame.mouse.get_pressed()[0]:
            return True


class Flag(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("assets/Flag.png")
        self.rect=self.image.get_rect()
        self.pos=(891,192.5)
    def draw(self, surface):
        surface.blit(self.image, self.pos)

class Hole(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("assets/Hole.png")
        self.rect = self.image.get_rect()
        self.rect.center = (900, 267.5)
    def draw(self, surface):
        surface.blit(self.image, self.rect)


#Create objects
ball=Ball()
slider=Slider()
field=Field()
button=Launch()
arrow=Arrow()
flag=Flag()
hole=Hole()
mouse_pressed = False
follow = True
# Game loop --> repeats until we leave the game
running = True
while running:
    # events --> The first one closes the game if we quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #custom events --> add it as methods of classes and call the methods here, it will run each method each loop of the game and each method will check for what it needs to run
        slider.handle_event(event)
        arrow.follow_mouse(follow)
        if arrow.validate_position(event,follow):
            follow = False
        button.clicked(event)





    #loop --> every action
    screen.fill(white)
    field.draw(screen)
    ball.draw(screen)
    slider.draw()
    button.draw(screen)
    arrow.draw(screen)
    flag.draw(screen)
    hole.draw(screen)

    font = pygame.font.Font(None, 36)
    text = font.render(f"Value: {slider.get_value()}", True, blue_efrei)
    screen.blit(text, (10, 10))

    # Update the display --> Update the new display with the new objects and positions
    pygame.display.flip()

    # Set the frame rate --> Don't change
    clock.tick(60)

# Quit the game
pygame.quit()