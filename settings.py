from utility import *
import config
from utility import get_font

# Load images only once
IMAGE_CACHE = {}
def load_image(path):
    if path not in IMAGE_CACHE:
        IMAGE_CACHE[path] = pygame.image.load(path).convert_alpha()
    return IMAGE_CACHE[path]

# ---- Initialize global variables
SCREEN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
BG = load_image(config.BG)
TOGGLESTATE_MUSIC=True

#Sounds and files
soundeffect_clicked=pygame.mixer.Sound("assets/Common/Sounds/clicked.mp3")

# Handle the sound effects enabled or disabled
if config.TOGGLESTATE_SOUND:
    soundeffect_clicked.set_volume(0.5)
else:
    soundeffect_clicked.set_volume(0)

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
        """Title of the window."""
        def __init__(self):
            super().__init__()
            self.name = "Settings"
        def draw(self):
            font=get_font(40)
            text= font.render(self.name, True, config.BLUE_EFREI)
            rect=text.get_rect()
            SCREEN.blit(text, (500-rect[2]/2,10))

    class SoundToggle(pygame.sprite.Sprite):
        """Toggle of both sound effects and music."""
        def __init__(self,use):
            super().__init__()
            # Toggle assets
            self.onasset=pygame.transform.scale(load_image("assets/Menu/Toggle_On.png"),(80,40))
            self.offasset=pygame.transform.scale(load_image("assets/Menu/Toggle_Off.png"),(80,40))
            # Define the use: music or sound effects
            self.use=use

            # Text and position depending on the use
            if self.use=="Music":
                self.rect = pygame.Rect(100, 100, 100, 30)
                self.dest = (100, 95)
                self.msg="Toggle music"
                self.state = TOGGLESTATE_MUSIC  # Initial state of the toggle - TOGGLESTATE global variable is used to save this state when leaving the settings window
            elif self.use=="Sound":
                self.rect = pygame.Rect(100, 160, 100, 30)
                self.dest = (100, 155)
                self.msg="Toggle sound effects"
                self.state = config.TOGGLESTATE_SOUND  # Initial state of the toggle - it is stored in config to be used in other files
            else:
                self.rect = pygame.Rect(100, 160, 100, 30)
                self.dest = (100, 155)
                self.msg="Unknown text" # Handle errors
            font=get_font(28)
            self.text=font.render(self.msg, True, config.BLACK)
        def draw(self):
            if self.state:
                SCREEN.blit(self.onasset,self.dest)
            else:
                SCREEN.blit(self.offasset,self.dest)
            SCREEN.blit(self.text, (self.dest[0]+100, self.dest[1]))
        def clicked(self):
            global TOGGLESTATE_MUSIC
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.use=="Music":
                    if self.state:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    TOGGLESTATE_MUSIC = not TOGGLESTATE_MUSIC
                    self.state = TOGGLESTATE_MUSIC
                elif self.use=="Sound":
                    if self.state:
                        soundeffect_clicked.set_volume(0)
                    else:
                        soundeffect_clicked.set_volume(0.5)
                    config.TOGGLESTATE_SOUND = not config.TOGGLESTATE_SOUND
                    self.state = config.TOGGLESTATE_SOUND
                soundeffect_clicked.play()
                print("toggle state: "+str(self.state))
        def getstate(self):
            return self.state


    class ResetButton(pygame.sprite.Sprite):
        """Button to reset progress. It resets every value in the save files to 0."""

        def __init__(self):
            super().__init__()
            # Initialize button characteristics
            self.msg="Reset progress"
            self.text = get_font(35).render(self.msg, True, config.BLUE_EFREI)
            self.text_rect = self.text.get_rect()
            self.text_rect.center=(500,300)
            self.button_rect=self.text_rect.inflate(20,20)
            self.buttoncolor=config.WHITE

        def draw(self):
            pygame.draw.rect(SCREEN, config.BLUE_EFREI, self.button_rect, border_radius=44)
            pygame.draw.rect(SCREEN, self.buttoncolor, self.button_rect.inflate(-8,-8), border_radius=44)
            SCREEN.blit(self.text, (self.text_rect.center[0]-self.text_rect.width/2, self.text_rect.center[1]-self.text_rect.height/2))

        def clicked(self):
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                self.buttoncolor=config.GREY
                soundeffect_clicked.play()
                # Reset saved values to 0
                filename="saves/golflevel.json"
                dico = loadfile(filename)
                for key in dico.keys():
                    dico[key]=0
                with open(filename, "w") as file:
                    json.dump(dico, file)
                print("Progress has been reset")


    #Game Objects Creation
    backarrow = BackArrow()
    title= Title()
    mtoggle=SoundToggle("Music")
    stoggle=SoundToggle("Sound")
    rbutton=ResetButton()

    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        pygame.display.set_caption("EfreiSport - Settings")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: #all events if mouse is pressed
                mtoggle.clicked()
                stoggle.clicked()
                rbutton.clicked()
                if backarrow.clicked(): #Back to the menu when the back arrow is clicked
                    return "Exit"
            elif event.type == pygame.MOUSEBUTTONUP:  # Reset buttons color when the mouse button is released
                rbutton.buttoncolor = config.WHITE
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #Back to the menu when escape is pressed
                    return "Exit"

        #background "efrei sport"
        SCREEN.fill((240, 240, 240, 0.5))
        SCREEN.blit(BG, (0, 0))

        # Design of the page
        backarrow.draw()
        title.draw()
        mtoggle.draw()
        stoggle.draw()
        rbutton.draw()
        # Update the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()