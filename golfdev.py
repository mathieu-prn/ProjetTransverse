import pygame, json, math
from utility import *

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport - Golf")
bg = pygame.image.load("assets/Background.png")

# Initialize Colors
black = (0, 0, 0)
white = (255, 255, 255)
red=(255,0,0)
blue_efrei=(18,121,190)
grey=(211,211,211)
green=(148,186,134)

def getlevel():
    '''Reads the level number saved in the saves file and returns it'''
    filename="saves/golflevel.json"
    dico=loadfile(filename)
    for key,value in dico.items():
        if key=="level":
            print("Returned level:",value)
            return value

def updatelevel(levelnumber):
    '''Updates the level number saved in the saves file and returns it'''
    filename="saves/golflevel.json"
    dico=loadfile(filename)
    for key,value in dico.items():
        if key=="level":
            dico[key]=levelnumber
            with open(filename,"w") as file:
                json.dump(dico,file)
            level.number=levelnumber


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("assets/Golf/GolfBall.png")
        self.image = pygame.transform.scale(img, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = getrelativepos((25,212.5))

    def draw(self):
        screen.blit(self.image, self.rect)

    def collision(self,walls):
        for wall in walls:
            if pygame.Rect.colliderect(self.rect,wall.rect):
                return wall

    def checkwin(self):
        if pygame.Rect.colliderect(self.rect, level.hole.collisionrect):
            return True


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

    def draw(self):
        pygame.draw.rect(screen, blue_efrei, self.rect.inflate(6, 6))
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 45)
        text = font.render(f"Go!", True, blue_efrei)
        screen.blit(text, (self.x, self.y+30))

    def clicked(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.color= grey
                ball.rect.center=getrelativepos((836,212.5))
        elif event.type == pygame.MOUSEBUTTONUP:
            self.color= white

class Field(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect=pygame.Rect(80,55,900,425)
    def draw(self):
        pygame.draw.rect(screen, green, self.rect)

class Wall(pygame.sprite.Sprite):
    def __init__(self,relative_x,relative_y,width,height,walls,isborder):
        pygame.sprite.Sprite.__init__(self)
        self.color=blue_efrei
        self.x=relative_x
        self.y=relative_y
        self.width=width
        self.height=height
        #If it's a border, set the left corner position. If it's a wall set the center position.
        if isborder:
            self.rect=pygame.Rect(self.x+80, self.y+55, self.width, self.height)
        else:
            self.rect=pygame.Rect(self.x+80-self.width/2, self.y+55-self.height/2, self.width, self.height)
        walls.append(self) #add the new wall to the walls list --> It will be useful for collisions
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("assets/Golf/GolfBall.png")
        self.image = pygame.transform.scale(img, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = (int(ball.rect.center[0]) + 40, 267.5)
        self.angle = 0
        self.rotation_speed = 0.1

    def draw(self):
        screen.blit(self.image, self.rect)

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

    def validate_position(self,follow):
                if follow:
                    print("follow False")
                    return False
                else:
                    print("follow True")
                    return True

class Flag(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("assets/Golf/Flag.png")
        self.rect=self.image.get_rect()
        self.x,self.y=pos
        self.pos=(self.x-7,self.y-75)
    def draw(self):
        screen.blit(self.image, self.pos)

class Hole(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("assets/Golf/Hole.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.collisionrect=pygame.draw.circle(screen, white, self.rect.center, 7)
    def draw(self):
        pygame.draw.circle(screen, white, self.rect.center, 7)
        screen.blit(self.image, self.rect)

class Level(pygame.sprite.Sprite):
    def __init__(self,number,hole_pos):
        pygame.sprite.Sprite.__init__(self)
        self.number=number
        self.hole=Hole(getrelativepos(hole_pos))
        self.flag=Flag(getrelativepos(hole_pos))

    def load(self):
        self.hole.draw()
        self.flag.draw()
        #Load the right level depending on the level number
        print("Loaded level",self.number)
        match self.number:
            case 1:
                wall1=Wall(750,212.5,6,200,walls,False)
            case 2:
                wall1=Wall(150,212.5,6,200,walls,False)
                wall2 = Wall(750, 212.5, 6, 200, walls, False)
            case _:
                pass
        #draw walls
        for wall in walls:
            wall.draw()

#Create field
field=Field()
walls=[]
bordertop=Wall(0,0,900,6,walls,True)
borderleft=Wall(0,0,6,425,walls,True)
borderbottom=Wall(0,425,900,6,walls,True)
borderright=Wall(900,0,6,431,walls,True)

#Create objects
ball=Ball()
slider=Slider()
button=Launch()
arrow=Arrow()
mouse_pressed = False
follow = True

#Level
level=Level(getlevel(),(850,212.5)) #set the initial level

# Game loop --> repeats until we leave the game
clock = pygame.time.Clock()
running = True
while running:
    # events --> The first one closes the game if we quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #custom events --> add it as methods of classes and call the methods here, it will run each method each loop of the game and each method will check for what it needs to run
        if follow:
            if event.type == pygame.MOUSEBUTTONDOWN:
                follow = arrow.validate_position(follow)
            arrow.follow_mouse(follow)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if field.rect.collidepoint(event.pos):
                    follow = arrow.validate_position(follow)
            slider.handle_event(event)
            button.clicked(event)

    #loop --> every action
    #bg
    screen.fill((240, 240, 240, 0.5))
    screen.blit(bg,(0,0))

    #field
    field.draw()

    #Objects
    slider.draw()
    button.draw()
    arrow.draw()

    #Load Level
    level.load()
    ball.draw()

    #check for collisions
    ball.collision(walls)

    if ball.checkwin():
        ball.rect.center = getrelativepos((25, 212.5))
        updatelevel(level.number+1)

    # Update the display --> Update the new display with the new objects and positions
    pygame.display.flip()

    # Set the frame rate --> Don't change
    clock.tick(60)

# Quit the game
pygame.quit()