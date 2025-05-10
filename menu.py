import pygame
import config
print("menu.py ran")
import game_select as gameselect, settings as settings

# Initialize Pygame
pygame.init()
pygame.mixer.init()
# Set up the game window
SCREEN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

# Top left icon
pygame_icon = pygame.image.load('assets/Common/logo.png')
pygame.display.set_icon(pygame_icon)


# Assets loads
BG = pygame.image.load(config.BG) # Background
logo_long = pygame.image.load("assets/Common/Logo long EFREI sport.png") # Logo
FONT = pygame.font.Font(config.FONT, 48) # Main FONT

#sounds
soundeffect_clicked=pygame.mixer.Sound("assets/Common/Sounds/clicked.mp3")
pygame.mixer.music.load("assets/Common/Sounds/music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

class SettingsButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bordercolor=config.BLUE_EFREI
        self.borderrect=pygame.Rect(90,360,348,98)
        self.buttoncolor=config.WHITE
        self.buttonrect=pygame.Rect(90+6, 360+6, 348-12, 98-12)
    def draw(self):
        pygame.draw.rect(SCREEN, self.bordercolor, self.borderrect,0,48)
        pygame.draw.rect(SCREEN, self.buttoncolor, self.buttonrect,0,48)
        txt = FONT.render("Settings", True, self.bordercolor)  # Load text
        SCREEN.blit(txt, (167, 372))  # Display text at (202,372)
    def clicked(self):
        if self.borderrect.collidepoint(pygame.mouse.get_pos()):
            soundeffect_clicked.play()
            if settings.run()=="Exit":
                pygame.event.clear()


#create game objects
settings_b=SettingsButton()


clock = pygame.time.Clock()

# Game loop
running = True
while running:
    pygame.display.set_caption("EfreiSport - Menu")  # Title
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            settings_b.clicked()
            # "Start button"
            if (564 <= mouse_x <= 564 + 348 and 360 <= mouse_y <= 360 + 98):
                print("Start button clicked")
                soundeffect_clicked.play()
                pygame.time.wait(200)  # Avoid multiple clicks
                if gameselect.run(FONT, BG) == "Exit":  # run game_select and handle the exit
                    pygame.event.clear()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Back to the menu when escape is pressed
                pygame.quit()
    # Design of the page

    # Overlay "efrei sport"
    SCREEN.fill((240,240,240, 0.5))
    SCREEN.blit(BG,(0, 0))

    # Logo top right
    SCREEN.blit(logo_long, (345, 32))

    # Blue Lines
    pygame.draw.line(SCREEN, config.BLUE_EFREI, (0,172), (1000,172), width=16)
    pygame.draw.line(SCREEN, config.BLUE_EFREI, (0, 172+32), (1000, 172+32), width=16)

    # 2/3 bottom grey rect
    pygame.draw.rect(SCREEN,(201,201,201),(0,330,1000,176))

    # "Settings" Button
    settings_b.draw()

    # "Start" Button
    pygame.draw.rect(SCREEN, (config.BLUE_EFREI), (564, 360, 348, 98), 0, 48) # Blue border of the button
    pygame.draw.rect(SCREEN, ((255, 255, 255)), (564 + 6, 360 + 6, 348 - 12, 98 - 12), 0, 48) #Fill
    txt_start = FONT.render("Start", True, (config.BLUE_EFREI)) # Load text
    SCREEN.blit(txt_start, (676, 372)) # Display text at (202,372)

    # Usability of the page
    mouse_x, mouse_y = pygame.mouse.get_pos()
    clicked = 0

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()