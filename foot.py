import pygame
from utility import *
import config

# Initialize Pygame
pygame.init()

# Load images only once
IMAGE_CACHE = {}
def load_image(path):
    if path not in IMAGE_CACHE:
        IMAGE_CACHE[path] = pygame.image.load(path).convert_alpha()
    return IMAGE_CACHE[path]

pygame.display.set_caption("EfreiSport - Football")

# Initialize global variables
SCREEN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
BG = pygame.image.load(config.BG)
LOGO = pygame.image.load('assets/Football/Logo_Penalty.png')

DISPLAY_MSG = False  # When True, a win/lose message is shown
WON = False
#list of border walls
BORDER_WALLS = []


def run():
    global BORDER_WALLS

    # Might move some of these to utility.py
    def getlevel():
        """Read and return the level number from the save file."""
        filename = "saves/golflevel.json"
        dico = loadfile(filename)
        level_value = dico.get("level", 1)
        print("Returned level:", level_value)
        return level_value

    def updatelevel(levelnumber): # Updates the saved level (called every 5 levels)
        """Update the level number in the save file."""
        filename = "saves/golflevel.json"
        dico = loadfile(filename)
        dico["level"] = levelnumber
        with open(filename, "w") as file:
            json.dump(dico, file)
        #soundeffect_save.play() -- Sound not added in files yet
        print("Updated level", levelnumber)

    def updatescore(levelnumber, score):
        """Update the score of the current level."""
        filename = "saves/golflevel.json"
        dico = loadfile(filename)
        dico[str(levelnumber)] = score
        with open(filename, "w") as file:
            json.dump(dico, file)

    # Game classes

    class Launch(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.rect = pygame.Rect(17, 396, 50, 80)
            self.color = config.WHITE

        def draw(self, surface=SCREEN):
            pygame.draw.rect(surface, self.color, self.rect)
            font = pygame.font.Font(None, 45)
            text = font.render("Go!", True, config.BLUE_EFREI)
            surface.blit(text, (self.rect.x, self.rect.y ))

    class Field(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.rect = pygame.Rect(35, 50, 936, 430)
    
        def draw(self, surface=SCREEN):
            pygame.draw.rect(surface, config.GREY, self.rect)
    
    class Wall(pygame.sprite.Sprite):
        def __init__(self, relative_x, relative_y, width, height, is_border):
            super().__init__()
            self.color = config.BLUE_EFREI
            if is_border:
                self.rect = pygame.Rect(relative_x + 35, relative_y + 50, width, height)
            else:
                self.rect = pygame.Rect(relative_x + 35 - width / 2, relative_y + 50 - height / 2, width, height)
    
        def draw(self, surface=SCREEN):
            pygame.draw.rect(surface, self.color, self.rect)
    
    class Level(pygame.sprite.Sprite):
        def __init__(self, number):
            super().__init__()
            self.number = number
            self.level_walls = []    # Level-specific walls
            self.all_walls = BORDER_WALLS + self.level_walls
    
    # Render Static Background
    def render_static_background(level):
        static_bg = pygame.Surface((config.WIDTH, config.HEIGHT))
        static_bg.fill((240, 240, 240))
        static_bg.blit(BG, (0, 0))
        field.draw(static_bg)
        for wall in level.level_walls:
            wall.draw(static_bg)
        for wall in BORDER_WALLS:
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
    BORDER_WALLS.extend([bordertop, borderbottom, borderleft, borderright])
    
    level = Level(getlevel())
    static_background = render_static_background(level)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        # Blit the static background
        SCREEN.blit(static_background, (0, 0))
    
        pygame.display.flip()
        # Set the frame rate
        clock.tick(60)
    
    # Quit the game
    pygame.quit()

run() # Needed for development, should be deleted later