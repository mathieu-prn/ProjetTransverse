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
pygame_icon = pygame.image.load('assets/logo.png')
pygame.display.set_icon(pygame_icon)

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
        self.velocity=0
        self.angle=0

    def draw(self):
        screen.blit(self.image, self.rect)

    def collision(self,walls):
        for wall in walls:
            if pygame.Rect.colliderect(pygame.Rect(self.rect.inflate(5,5)),wall.rect):
                print("collided with", wall)
                if wall.rect[2]==6:
                    self.angle = math.pi - self.angle  # Reflect across the Y-axis
                elif wall.rect[3]==6:
                    self.angle = -self.angle
                self.velocity *= 0.9  # Optional: Reduce velocity slightly to simulate energy loss
                return True

    def checkwin(self):
        if pygame.Rect.colliderect(self.rect, level.hole.collisionrect) and self.velocity<10:
            return True

    def updateposition(self,launched):
        if launched:
            self.velocity=slider.get_value()*0.4
            self.angle = arrow.angle
        acceleration=-0.7
        vx=self.velocity*math.cos(self.angle)
        vy=self.velocity*math.sin(self.angle)
        x,y=self.rect.center
        self.rect.center=(x+vx,y+vy)
        self.velocity+=acceleration

        if self.velocity < 0:
            self.velocity = 0

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
                ball.updateposition(True)
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
    def __init__(self, length=50):
        pygame.sprite.Sprite.__init__(self)
        self.length = length  # Default arrow length
        self.direction = pygame.Vector2(1, 0)  # Default direction (to the right)

    def draw(self):
        """Draws the arrow based on the last updated direction."""
        arrow_end = ball.rect.center + self.direction * (20+slider.get_value())
        pygame.draw.line(screen, blue_efrei, ball.rect.center, arrow_end, 3)

        # Arrowhead calculation
        self.angle = math.atan2(self.direction.y, self.direction.x)
        self.arrowangle = math.atan2(-self.direction.y, -self.direction.x)
        arrow_size = 10
        left = (arrow_end.x + arrow_size * math.cos(self.arrowangle + math.pi / 6),
                arrow_end.y + arrow_size * math.sin(self.arrowangle + math.pi / 6))
        right = (arrow_end.x + arrow_size * math.cos(self.arrowangle - math.pi / 6),
                 arrow_end.y + arrow_size * math.sin(self.arrowangle - math.pi / 6))
        pygame.draw.polygon(screen, blue_efrei, [arrow_end, left, right])

    def update_direction(self, mouse_pos):
        """Updates the arrow direction unless it's locked."""
        if not self.validate_position(follow):  # Check if following is allowed
            direction = pygame.Vector2(mouse_pos) - ball.rect.center
            if direction.length() > 0:
                self.direction = direction.normalize()  # Store direction

    def validate_position(self,follow):
                return not follow

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
    def __init__(self,number):
        pygame.sprite.Sprite.__init__(self)
        self.number=number
        self.hole=Hole(getrelativepos((850,212.5)))
        self.flag=Flag(getrelativepos((850,212.5)))

    def draw(self):
        #Load the right level depending on the level number
        match self.number:
            case 1: #Level 1
                wall1=Wall(750,212.5,6,200,walls,False)
            case 2: #Level 2
                wall1=Wall(150,212.5,6,200,walls,False)
                wall2 = Wall(750, 212.5, 6, 200, walls, False)
            case 3: #And so on
                self.hole=Hole(getrelativepos((850,50)))
                self.flag=Flag(getrelativepos((850,50)))
                wall1=Wall(750,150,6,300,walls,False)
                wall2=Wall(150,275,6,300,walls,False)
            case 4:
                self.hole = Hole(getrelativepos((850, 50)))
                self.flag = Flag(getrelativepos((850, 50)))
                wall1 = Wall(750, 150, 6, 300, walls, False)
                wall2 = Wall(150, 275, 6, 300, walls, False)
                wall3 = Wall(450, 212.5, 6, 300, walls, False)
            case _:
                pass
        #draw walls
        for wall in walls:
            wall.draw()
        self.hole.draw()
        self.flag.draw()

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
level=Level(getlevel()) #set the initial level

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
    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # Update arrow direction if allowed
    arrow.update_direction((mouse_x, mouse_y))

    # Draw ball and arrow
    button.draw()

    # check for collisions
    ball.collision(walls)
    if ball.velocity>0:
        ball.updateposition(False)
    else:
        arrow.draw()
        slider.draw()

    #Load Level
    level.draw()
    ball.draw()

    if ball.checkwin():
        ball.velocity=0
        ball.rect.center = getrelativepos((25, 212.5))
        updatelevel(level.number+1)

    # Update the display --> Update the new display with the new objects and positions
    pygame.display.flip()

    # Set the frame rate --> Don't change
    clock.tick(120)

# Quit the game
pygame.quit()