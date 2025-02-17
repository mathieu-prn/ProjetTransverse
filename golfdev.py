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
bunker_yellow=(237,225,141)

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

def end(walls):
    ball.velocity = 0
    walls = walls[:4]
    bunkers = []
    score.reset()
    ball.rect.center = getrelativepos((25, 212.5))

def lose():
    message.draw("lose")
    end(walls)

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

    def collision(self, walls):
        for wall in walls:
            if pygame.Rect.colliderect(self.rect.inflate(5, 5), wall.rect):
                print("Collided with", wall)

                dx = min(abs(self.rect.right - wall.rect.left), abs(self.rect.left - wall.rect.right))
                dy = min(abs(self.rect.bottom - wall.rect.top), abs(self.rect.top - wall.rect.bottom))

                if dx < dy:  # More movement in X direction → Vertical Wall Collision
                    print("Vertical Wall Collision")
                    self.angle = math.pi - self.angle  # Reflect X direction
                    self.rect.x += 2 * math.cos(self.angle)  # Move out of collision

                elif dy<dx:
                    print("Horizontal Wall Collision")
                    self.angle = -self.angle  # Reflect Y direction
                    self.rect.y += 2 * math.sin(self.angle)  # Move out of collision

                else:
                    print("Corner Collision")
                    self.angle = self.angle + math.pi  # Reflect both X and Y direction
                    self.rect.x += 2 * math.cos(self.angle)  # Move out of collision
                    self.rect.y += 2 * math.sin(self.angle)  # Move out of collision

                self.velocity *= 0.9  # Energy loss on bounce

                return True
        return False

    def unstuck(self):
        if ball.rect.left<field.rect.left:
            print("Tried to unstuck left")
            ball.rect.center=(ball.rect.center[0]+4,ball.rect.center[1])
        elif ball.rect.right>field.rect.right:
            print("Tried to unstuck right")
            ball.rect.center=(ball.rect.center[0]-4,ball.rect.center[1])
        elif ball.rect.top<field.rect.top:
            print("Tried to unstuck top")
            ball.rect.center=(ball.rect.center[0],ball.rect.center[1]+4)
        elif ball.rect.bottom>field.rect.bottom:
            print("Tried to unstuck bottom")
            ball.rect.center=(ball.rect.center[0],ball.rect.center[1]-4)

    def updateposition(self,launched):
        if launched:
            self.velocity=slider.get_value()*0.2
            self.angle = arrow.angle
        acceleration = -0.1
        for bunker in bunkers:
            if pygame.Rect.colliderect(self.rect,bunker.rect):
                acceleration=-1

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
        self.slider_rect = pygame.Rect(self.X, self.Y, 30, 7)
        self.dragging = False

    def draw(self):
        pygame.draw.rect(screen, blue_efrei, self.rect.inflate(6, 6))
        pygame.draw.rect(screen, white, self.rect)
        pygame.draw.rect(screen, black, self.slider_rect)

    def handle_event(self, event):
        """Handles mouse events to move the slider."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.Y = max(self.rect.top, min(event.pos[1], self.rect.bottom - 7))
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
            if self.rect.collidepoint(event.pos) and ball.velocity==0:
                score.increment()
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

class Bunker(pygame.sprite.Sprite):
    def __init__(self,pos,width,height):
        pygame.sprite.Sprite.__init__(self,)
        self.width=width
        self.height=height
        self.rect=pygame.Rect(0,0,width,height)
        self.rect.center=pos
        bunkers.append(self)
    def draw(self):
        pygame.draw.rect(screen, bunker_yellow, self.rect)

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
        self.x,self.y=pos
        self.rect=self.image.get_rect()
        self.pos=(self.x-7,self.y-75)
        self.rect=pygame.Rect(self.x-self.rect[2]/2,self.y-self.rect[3],self.rect[2],self.rect[3])
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
        # Load the right level depending on the level number
        match self.number:
            case 1:  # Level 1
                wall1 = Wall(750, 212.5, 6, 200, walls, False)
            case 2:  # Level 2
                wall1 = Wall(150, 212.5, 6, 200, walls, False)
                wall2 = Wall(750, 212.5, 6, 200, walls, False)
            case 3:  # And so on
                self.hole = Hole(getrelativepos((850, 50)))
                self.flag = Flag(getrelativepos((850, 50)))
                wall1 = Wall(750, 150, 6, 300, walls, False)
                wall2 = Wall(150, 275, 6, 300, walls, False)
            case 4:
                self.hole = Hole(getrelativepos((850, 50)))
                self.flag = Flag(getrelativepos((850, 50)))
                wall1 = Wall(750, 150, 6, 300, walls, False)
                wall2 = Wall(150, 275, 6, 300, walls, False)
                wall3 = Wall(450, 212.5, 6, 300, walls, False)
            case 5:
                self.hole = Hole(getrelativepos((850, 75)))
                self.flag = Flag(getrelativepos((850, 75)))
                wall1 = Wall(750, 150, 6, 300, walls, False)
                wall2 = Wall(150, 275, 6, 300, walls, False)
                if len(bunkers) <= 1:
                    self.bunker = Bunker(getrelativepos((450, 75)), 300, 150)
                    self.bunker2 = Bunker(getrelativepos((450, 350)), 300, 150)
            case 6:
                self.hole = Hole(getrelativepos((850, 50)))
                self.flag = Flag(getrelativepos((850, 50)))

            case _:
                pass

        #draw walls
        for bunker in bunkers:
            bunker.draw()
        for wall in walls:
            wall.draw()
        self.hole.draw()
        if not pygame.Rect.colliderect(self.flag.rect, ball.rect) or ball.velocity != 0:
            self.flag.draw()

class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.score=0
        self.font = pygame.font.Font("assets/font.ttf", 28)
    def increment(self):
        if self.score<5:
            self.score+=1
    def reset(self):
        self.score=0
    def draw(self):
        text = self.font.render(f"Shots: {self.score}", True, blue_efrei)
        screen.blit(text, (10, 10))

class Message(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font("assets/font.ttf", 28)
        self.fontcolor=blue_efrei

        self.buttonwidth=150
        self.buttonheight=50
        self.buttonpos=(500-self.buttonwidth/2,275)
        self.buttoncolor=white
        self.buttonrect=pygame.Rect((self.buttonpos[0],self.buttonpos[1]),(self.buttonwidth,self.buttonheight))
    def draw(self,msgtype):
        msg="Text couldn't be loaded"
        buttonmsg="Text couldn't be loaded"
        if msgtype=="win":
            msg=f"You won in {score.score} shots!"
            buttonmsg="Next level"
        elif msgtype=="lose":
            msg = f"You didn't succeed to score in 5 shot. You lost!"
            buttonmsg="Try again"

        text = self.font.render(msg, True, blue_efrei)
        width,height=text.get_size()

        buttontext=self.font.render(buttonmsg, True, blue_efrei)

        screen.blit(text,(screen.get_width()/2-width/2,screen.get_height()/2-height/2))

        pygame.draw.rect(screen, blue_efrei, self.buttonrect.inflate(6, 6))
        pygame.draw.rect(screen, self.buttoncolor, self.buttonrect)
        screen.blit(buttontext,self.buttonpos)

    def clicked(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttonrect.collidepoint(event.pos):
                print("clicked")
                self.buttoncolor= grey
                updatelevel(level.number+1)
                end(walls)
                ball.updateposition(True)
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.buttoncolor= white

#Create field
field=Field()
walls=[]
bunkers=[]
bordertop=Wall(0,0,900,6,walls,True)
borderbottom=Wall(0,425,900,6,walls,True)
borderleft=Wall(0,0,6,425,walls,True)
borderright=Wall(900,0,6,431,walls,True)

#Create objects
ball=Ball()
slider=Slider()
button=Launch()
arrow=Arrow()
score=Score()
message=Message()
mouse_pressed = False
follow = True
won=False
displaymsg=False

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
                if displaymsg:
                    message.clicked(event)
                    displaymsg=False
                    won=False
            if event.type == pygame.MOUSEBUTTONUP:
                button.color=white
                message.buttoncolor=white

    #loop --> every action
    #bg

    screen.fill((240, 240, 240, 0.5))
    screen.blit(bg,(0,0))

    #field
    field.draw()

    #Objects
    # check for collisions
    ball.collision(walls)
    ball.unstuck()
    #Load Level
    level.draw()
    score.draw()

    if displaymsg:
        if won:
            message.draw("win")
        else:
            message.draw("lose")
    else:
        if ball.velocity>0:
            ball.updateposition(False)
        else:
            arrow.draw()
            slider.draw()
            button.draw()
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Update arrow direction if allowed
        arrow.update_direction((mouse_x, mouse_y))

        if pygame.Rect.colliderect(ball.rect, level.hole.collisionrect) and ball.velocity<10:
            won=True
            displaymsg=True
        else:
            if ball.velocity==0 and score.score==5:
                lose()
            else:
                ball.draw()



    # Update the display --> Update the new display with the new objects and positions
    pygame.display.flip()

    # Set the frame rate --> Don't change
    clock.tick(60)

# Quit the game
pygame.quit()