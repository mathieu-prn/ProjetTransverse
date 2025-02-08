import pygame, math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport - Basketball")
bg = pygame.image.load("assets/Background.png")

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

clock = pygame.time.Clock()

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("assets/GolfBall.png")
        self.image = pygame.transform.scale(img, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = (50, 400)

    def trajectory_equation(self, speed, angle, x0, y0):
        v_x = speed * math.cos(angle)
        v_y = speed * math.sin(angle)
        x = (v_x, x0)
        y = (0.5 * G, -v_y, y0)
        return x, y

    def calc_pos(self, x_coeff, y_coeff, time):
        new_x = x_coeff[0]*time + x_coeff[1]
        new_y = y_coeff[0]*(time**2) + y_coeff[1]*time + y_coeff[2]
        return (new_x, new_y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


#Object initialization
ball = Ball()

calc_eq = True

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)

    if calc_eq:
        x_coeff, y_coeff = ball.trajectory_equation(100, 45, ball.rect.center[0], ball.rect.center[1])
        print(x_coeff, x_coeff)
        calc_eq = False


    if ball.rect.center[1]<500 and ball.rect.center[0]<1000:
        ball.rect.center = ball.calc_pos(x_coeff, y_coeff, t)

    ball.draw(screen)
    # Update the display
    pygame.display.flip()
    t+=dt

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()