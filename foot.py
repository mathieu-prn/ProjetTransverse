import pygame
from utility import *

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport - Football")
bg = pygame.image.load("assets/Common/Background.png")
pygame_icon = pygame.image.load('assets/Common/logo.png')
logo = pygame.image.load('assets/Football/Logo_Penalty.png')

pygame.display.set_icon(pygame_icon)


# Initialize Colors
black = (0, 0, 0)
white = (255, 255, 255)
red=(255,0,0)
blue_efrei=(18,121,190)
grey=(211,211,211)

#list of border walls
border_walls = []

class Launch(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(17, 396, 50, 80)
        self.color = white

    def draw(self, surface=screen):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 45)
        text = font.render("Go!", True, blue_efrei)
        surface.blit(text, (self.rect.x, self.rect.y ))

class Field(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(35, 50, 936, 430)
        self.image = pygame.transform.scale((pygame.image.load('assets/Football/Logo_Penalty.png')), (100, 50))

    def draw(self, surface=screen):
        pygame.draw.rect(surface, grey, self.rect)
        #surface.blit(self.image, self.rect)

class Wall(pygame.sprite.Sprite):
    def __init__(self, relative_x, relative_y, width, height, is_border):
        super().__init__()
        self.color = blue_efrei
        if is_border:
            self.rect = pygame.Rect(relative_x + 35, relative_y + 50, width, height)
        else:
            self.rect = pygame.Rect(relative_x + 35 - width / 2, relative_y + 50 - height / 2, width, height)

    def draw(self, surface=screen):
        pygame.draw.rect(surface, self.color, self.rect)

class Level(pygame.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        self.number = number
        self.level_walls = []    # Level-specific walls
        self.all_walls = border_walls + self.level_walls

def getlevel():
    """Read and return the level number from the save file."""
    filename = "saves/footlevel.json"
    dico = loadfile(filename)
    level_value = dico.get("level", 1)
    print("Returned level:", level_value)
    return level_value

def updatelevel(levelnumber):
    """Update the level number in the save file."""
    filename = "saves/footlevel.json"
    dico = loadfile(filename)
    dico["level"] = levelnumber
    with open(filename, "w") as file:
        json.dump(dico, file)
    print("Updated level",levelnumber)

def end_level():
    """Reset game state for a new level."""
    global static_background

# Render Static Background
def render_static_background(level):
    static_bg = pygame.Surface((WIDTH, HEIGHT))
    static_bg.fill((240, 240, 240))
    static_bg.blit(bg, (0, 0))
    field.draw(static_bg)
    screen.blit((pygame.image.load('assets/Football/Logo_Penalty.png')), (100,40.28))
    for wall in level.level_walls:
        wall.draw(static_bg)
    for wall in border_walls:
        wall.draw(static_bg)
    return static_bg

clock = pygame.time.Clock()

# Create Game Objects
field = Field()

# Create border walls (they don't change between levels)
bordertop = Wall(0, 0, 936, 6, True)
borderbottom = Wall(0, 430, 936, 6, True)
borderleft = Wall(0, 0, 6, 430, True)
borderright = Wall(936, 0, 6, 436, True)
border_walls.extend([bordertop, borderbottom, borderleft, borderright])

level = Level(getlevel())
static_background = render_static_background(level)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Blit the static background
    screen.blit(static_background, (0, 0))

    pygame.display.flip()
    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()