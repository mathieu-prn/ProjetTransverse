
import pygame, config, golf as golf, basket as basket, penalty as penalty, help as help

SCREEN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

def round_image_corners(image, radius):
    size = image.get_size()

    # Create a new surface with per-pixel alpha (transparent)
    rounded_image = pygame.Surface(size, pygame.SRCALPHA)

    # Create a mask surface with rounded corners
    mask = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, *size), border_radius=radius)

    # Blit the image onto the rounded surface using the mask
    rounded_image.blit(image, (0, 0))
    rounded_image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    return rounded_image

def run(FONT,BG): #Main function, called in the menu (main.py)
    # Previews assets
    golf_preview = pygame.transform.scale(pygame.image.load("assets/Menu/golf_preview.png"),(530,298))
    basket_preview = pygame.transform.scale(pygame.image.load("assets/Menu/basket_preview.png"),(530,298))
    penalty_preview = pygame.transform.scale(pygame.image.load("assets/Menu/penalty_preview.png"),(530,298))

    game=None
    preview=None

    soundeffect_clicked = pygame.mixer.Sound("assets/Common/Sounds/clicked.mp3")

    # Handle the sound effects enabled or disabled
    if config.TOGGLESTATE_SOUND:
        soundeffect_clicked.set_volume(0.5)
    else:
        soundeffect_clicked.set_volume(0)

    GREY = (234, 234, 234) #different grey from the one in config.py

    class Button():
        def __init__(self,name):
            self.name = name
            if self.name =="Basket":
                self.rect = pygame.Rect(48, 48, 232, 78)
            elif self.name == "Golf":
                self.rect = pygame.Rect(48, 156, 232, 78)
            elif self.name == "Penalty":
                self.rect = pygame.Rect(48, 264, 232, 78)
            elif self.name == "Exit":
                self.rect = pygame.Rect(48, 372, 232, 78)
        def draw(self):
            pygame.draw.rect(SCREEN, config.BLUE_EFREI, self.rect, border_radius=44)
            pygame.draw.rect(SCREEN, (255, 255, 255), self.rect.inflate(-8, -8), border_radius=44)
            text_surface = FONT.render(self.name, True, config.BLUE_EFREI)
            text_rect = text_surface.get_rect(center=self.rect.center)
            SCREEN.blit(text_surface, text_rect)


    class PlayButton():
        def __init__(self):
            self.borderrect = pygame.Rect(772, 332, 160, 160)
            self.button_rect = pygame.Rect(774, 334, 156, 156)
            self.play_button_img = pygame.image.load("assets/Common/play_button.png")
        def draw(self):
            pygame.draw.rect(SCREEN, config.BLUE_EFREI, self.borderrect, border_radius=24)
            pygame.draw.rect(SCREEN, GREY, self.button_rect, border_radius=24)
            SCREEN.blit(self.play_button_img, (824, 376))
        def clicked(self,game):
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                soundeffect_clicked.play()
                if game == "Golf":
                    if golf.run() == "Exit":
                        pygame.event.clear()
                if game == "Basket":
                    if basket.run() == "Exit":
                        pygame.event.clear()
                if game == "Penalty":
                    if penalty.run() == "Exit":
                        pygame.event.clear()

    class HelpButton():
        def __init__(self):
            super().__init__()
            self.borderrect = pygame.rect.Rect(398, 332, 160, 160)
            self.rect = pygame.rect.Rect(400, 334, 156, 156)
            self.help_button_image = pygame.transform.scale(pygame.image.load("assets/Common/help_button.png"),(100,100))  # help button
        def draw(self):
            pygame.draw.rect(SCREEN, config.BLUE_EFREI, self.borderrect, border_radius=24)
            pygame.draw.rect(SCREEN, GREY, self.rect, border_radius=24)
            SCREEN.blit(self.help_button_image, (430, 365))
        def clicked(self,game):
            if self.rect.collidepoint(pygame.mouse.get_pos()): # If the click was on the button
                soundeffect_clicked.play()
                if game=="Golf":
                    if help.run(game)=="Exit":
                        pygame.event.clear()
                elif game=="Basket":
                    if help.run(game)=="Exit":
                        pygame.event.clear()
                elif game=="Penalty":
                    if help.run(game)=="Exit":
                        pygame.event.clear()



    #Define game objects
    help_button = HelpButton()
    play_button = PlayButton()

    basket_b = Button("Basket")
    penalty_b = Button("Penalty")
    golf_b = Button("Golf")
    exit_b = Button("Exit")
    game_buttons=[basket_b,penalty_b,golf_b,exit_b]

    clock = pygame.time.Clock()

    running = True
    while running:
        pygame.display.set_caption("EfreiSport - Game select")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                help_button.clicked(game)
                play_button.clicked(game)
                mouse_pos = event.pos
                for button in game_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        print(f"{button.name} button clicked!")
                        soundeffect_clicked.play()
                        game=button.name
                        if game == "Golf":
                            preview="golf"
                        elif game == "Penalty":
                            preview="penalty"
                        elif game=="Basket":
                            preview="basket"
                        elif game=="Exit":
                            return "Exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #Back to the menu when escape is pressed
                    return "Exit"


        # Draw background
        SCREEN.fill((240, 240, 240))
        SCREEN.blit(BG, (0, 0))

        # Draw buttons
        for button in game_buttons:
            button.draw()

        # Photo jeu section
        pygame.draw.rect(SCREEN, config.BLUE_EFREI, (398, 16, 534, 302), border_radius=24)
        if not preview:
            pygame.draw.rect(SCREEN, GREY, (400, 18, 530, 298), border_radius=24)
        else:
            im_preview=round_image_corners(BG, 24)
            if preview=="golf":
                im_preview=round_image_corners(golf_preview, 24)
            elif preview=="basket":
                im_preview=round_image_corners(basket_preview, 24)
            elif preview=="penalty":
                im_preview=round_image_corners(penalty_preview,24)
            SCREEN.blit(im_preview, (400, 18))

        # Play and help buttons
        help_button.draw()
        play_button.draw()


        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
