from utility import *
import config

# Load images only once
IMAGE_CACHE = {}
def load_image(path):
    if path not in IMAGE_CACHE:
        IMAGE_CACHE[path] = pygame.image.load(path).convert_alpha()
    return IMAGE_CACHE[path]

# ---- Initialize global variables
SCREEN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
BG = load_image(config.BG)

#Sounds
soundeffect_clicked=pygame.mixer.Sound("assets/Common/Sounds/clicked.mp3")

def run():

    def get_font(size): # Returns a pygame font of size "size"
        return pygame.font.Font(config.FONT, size)

    #Class
    class BackArrow(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.back_button = pygame.transform.scale(load_image("assets/Menu/arrow.png"), (40, 40))
            self.rect=self.back_button.get_rect()
        def draw(self):
            SCREEN.blit(self.back_button, self.rect)
            self.rect.center = (25, 30)
        def clicked(self):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                soundeffect_clicked.play()
                return True

    class Title(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.name = "Settings"
        def draw(self):
            font=get_font(40)
            text= font.render(self.name, True, config.BLUE_EFREI)
            rect=text.get_rect()
            SCREEN.blit(text, (500-rect[2]/2,10))

    class MusicToggle(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.rect=pygame.Rect(100, 50, 150, 150)
        def draw(self):
            pass


    #Game Objects Creation
    backarrow = BackArrow()
    title= Title()

    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        pygame.display.set_caption("EfreiSport - Settings")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if backarrow.clicked():
                    return "Exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #Back to the menu when escape is pressed
                    return "Exit"

        #background "efrei sport"
        SCREEN.fill((240, 240, 240, 0.5))
        SCREEN.blit(BG, (0, 0))

        # Design of the page
        backarrow.draw()
        title.draw()

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()