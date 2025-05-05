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
            #toggle
            self.onasset=""
            self.offasset=""
            self.state=False
            self.rect=pygame.Rect(100, 100, 100, 30)

            #text
            self.msg="Toggle Music"
            font=get_font(28)
            self.text=font.render(self.msg, True, config.BLACK)
        def draw(self):
            pygame.draw.rect(SCREEN,config.BLUE_EFREI,self.rect,0,48)
            SCREEN.blit(self.text, (215,94))
        def clicked(self):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.state:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                self.state = not self.state
                print("toggle state: "+str(self.state))

    class HelpSection(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.h1msg="How to play"
            self.h1=get_font(32).render(self.h1msg, True, config.BLUE_EFREI)
            self.end=250

    #Game Objects Creation
    backarrow = BackArrow()
    title= Title()
    mtoggle=MusicToggle()

    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        pygame.display.set_caption("EfreiSport - Settings")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mtoggle.clicked()
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
        mtoggle.draw()
        # Update the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()