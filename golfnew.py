import pygame, sys
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
        self.rect=pygame.Rect(self.x, self.y, self.width, self.height)
    def draw(self,screen):
        pygame.draw.rect(screen, blue_efrei, self.rect.inflate(6, 6))
        pygame.draw.rect(screen, white, self.rect)
        font = pygame.font.Font(None, 45)
        text = font.render(f"Go!", True, blue_efrei)
        screen.blit(text, (self.x, self.y+30))

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

#Create objects
ball=Ball()
slider=Slider()
field=Field()
button=Launch()
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        slider.handle_event(event)
    #events

    #loop
    screen.fill(white)
    field.draw(screen)
    ball.draw(screen)
    slider.draw()
    button.draw(screen)

    font = pygame.font.Font(None, 36)
    text = font.render(f"Value: {slider.get_value()}", True, blue_efrei)
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()