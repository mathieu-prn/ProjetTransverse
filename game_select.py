import pygame, config, golf as golf

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

def run(FONT,BG): #Main function, called in the menu (menu.py)
    pygame.display.set_caption("EfreiSport - Game select")
    play_button = pygame.image.load("assets/Common/play_button.png")
    lb_button_image = pygame.transform.scale(pygame.image.load("assets/Common/lb_button.png"),(100,100))  # leaderboard button
    #previews
    golf_preview = pygame.transform.scale(pygame.image.load("assets/Menu/golf_preview.png"),(530,298))
    basket_preview = pygame.transform.scale(pygame.image.load("assets/Menu/basket_preview.png"),(530,298))

    game=None
    preview=None

    GREY = (234, 234, 234)

    class button():
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


    class Play_button():
        def __init__(self):
            self.rect = pygame.Rect(772, 332, 160, 160)

    play_rect = pygame.Rect(772, 332, 160, 160)

    class Lb_button():
        def __init__(self):
            super().__init__()
            self.borderrect = pygame.rect.Rect(398, 332, 160, 160)
            self.rect = pygame.rect.Rect(400, 334, 156, 156)
        def draw(self):
            pygame.draw.rect(SCREEN, config.BLUE_EFREI, self.borderrect, border_radius=24)
            pygame.draw.rect(SCREEN, GREY, self.rect, border_radius=24)
            if preview == "golf":
                SCREEN.blit(lb_button_image, (430, 365))

    #Define game objects
    lb_button = Lb_button()

    basket_b = button("Basket")
    penalty_b = button("Penalty")
    golf_b = button("Golf")
    exit_b = button("Exit")
    game_buttons=[basket_b,penalty_b,golf_b,exit_b]

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button in game_buttons:
                    if button.rect.collidepoint(mouse_pos):
                        print(f"{button.name} button clicked!")
                        game=button.name
                        if game == "Golf":
                            preview="golf"
                        elif game == "Foot":
                            preview="foot"
                        elif game=="Basket":
                            preview="basket"
                        elif game=="Exit":
                            return "Exit"
                if play_rect.collidepoint(mouse_pos):
                    if game=="Golf":
                        if golf.run()=="Exit":
                            pygame.event.clear()
                    if game=="Basket":
                        pass
                    if game=="Penalty":
                        pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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
            elif preview=="foot":
                pass
            SCREEN.blit(im_preview, (400, 18))

        # Historic button
        lb_button.draw()

        # Play button
        pygame.draw.rect(SCREEN, config.BLUE_EFREI, (772, 332, 160, 160), border_radius=24)
        pygame.draw.rect(SCREEN, GREY, (774, 334, 156, 156), border_radius=24)
        SCREEN.blit(play_button, (824, 376))

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
