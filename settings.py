from utility import *
import config
import help as help

# Load images only once
IMAGE_CACHE = {}
def load_image(path):
    if path not in IMAGE_CACHE:
        IMAGE_CACHE[path] = pygame.image.load(path).convert_alpha()
    return IMAGE_CACHE[path]

# ---- Initialize global variables
SCREEN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
BG = load_image(config.BG)
TOGGLESTATE=True

#Sounds and files
soundeffect_clicked=pygame.mixer.Sound("assets/Common/Sounds/clicked.mp3")

def run():
    global TOGGLESTATE
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

    class SoundToggle(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            #toggle
            self.onasset=pygame.transform.scale(load_image("assets/Menu/Toggle_On.png"),(80,40))
            self.offasset=pygame.transform.scale(load_image("assets/Menu/Toggle_Off.png"),(80,40))
            self.state=TOGGLESTATE #Initial state of the toggle - TOGGLESTATE global variable is used to save this state when leaving the settings window
            self.rect=pygame.Rect(100, 100, 100, 30)
            self.dest=(100,95)

            #text
            self.msg="Toggle Music"
            font=get_font(28)
            self.text=font.render(self.msg, True, config.BLACK)
        def draw(self):
            if self.state:
                SCREEN.blit(self.onasset,self.dest)
            else:
                SCREEN.blit(self.offasset,self.dest)
            SCREEN.blit(self.text, (210,94))
        def clicked(self):
            global TOGGLESTATE
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                soundeffect_clicked.play()
                if self.state:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                TOGGLESTATE = not TOGGLESTATE
                self.state = TOGGLESTATE
                print("toggle state: "+str(self.state))

    class HelpButton(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.msg="How to play"
            self.text = get_font(35).render(self.msg, True, config.BLUE_EFREI)
            self.text_rect = self.text.get_rect()
            self.text_rect.center=(500,300)
            self.button_rect=self.text_rect.inflate(20,20)

        def draw(self):
            pygame.draw.rect(SCREEN, config.BLUE_EFREI, self.button_rect, border_radius=44)
            pygame.draw.rect(SCREEN, (255, 255, 255), self.button_rect.inflate(-8,-8), border_radius=44)
            SCREEN.blit(self.text, (self.text_rect.center[0]-self.text_rect.width/2, self.text_rect.center[1]-self.text_rect.height/2))
        def clicked(self):
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                soundeffect_clicked.play()
                if help.run() == "Exit": #Run the help.py file and handle the exit
                    pygame.event.clear()
                    print("cleared events")



    #Game Objects Creation
    backarrow = BackArrow()
    title= Title()
    stoggle=SoundToggle()
    hbutton=HelpButton()

    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        pygame.display.set_caption("EfreiSport - Settings")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: #all events if mouse is pressed
                stoggle.clicked()
                hbutton.clicked()
                if backarrow.clicked(): #Back to the menu when the back arrow is clicked
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
        stoggle.draw()
        hbutton.draw()
        # Update the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()