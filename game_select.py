import pygame

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

def run(screen, bg, font):
    pygame.display.set_caption("EfreiSport - Game select")
    play_button = pygame.image.load("assets/Common/play_button.png")
    golf_preview = pygame.transform.scale(pygame.image.load("assets/Menu/golf_preview.png"),(530,298))
    blue_efrei = (18, 121, 190)
    preview=None

    clock = pygame.time.Clock()

    # Button setup
    buttons = {
        "Basket": pygame.Rect(48, 48, 232, 78),
        "Golf": pygame.Rect(48, 156, 232, 78),
        "Foot": pygame.Rect(48, 264, 232, 78),
    }
    play_rect=pygame.Rect(772, 332, 160, 160)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for name, rect in buttons.items():
                    if rect.collidepoint(mouse_pos):
                        print(f"{name} button clicked!")
                        game=name
                        preview="golf"
                        # You can call corresponding game functions here
                        # Example: if name == "Golf": golf.run(screen, bg, font)
                if play_rect.collidepoint(mouse_pos):
                    if game=="Golf":
                        pass


        # Draw background
        screen.fill((240, 240, 240))
        screen.blit(bg, (0, 0))

        # Draw buttons
        for i, (name, rect) in enumerate(buttons.items()):
            pygame.draw.rect(screen, blue_efrei, rect, border_radius=44)
            pygame.draw.rect(screen, (255, 255, 255), rect.inflate(-8, -8), border_radius=44)
            text_surface = font.render(name, True, blue_efrei)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

        # Photo jeu section
        pygame.draw.rect(screen, blue_efrei, (398, 16, 534, 302), border_radius=24)
        if not preview:
            pygame.draw.rect(screen, (234, 234, 234), (400, 18, 530, 298), border_radius=24)
        elif preview=="golf":
            im_preview=round_image_corners(golf_preview, 24)
            screen.blit(im_preview, (400, 18))

        # Historic button
        pygame.draw.rect(screen, blue_efrei, (398, 332, 160, 160), border_radius=24)
        pygame.draw.rect(screen, (234, 234, 234), (400, 334, 156, 156), border_radius=24)

        # Play button
        pygame.draw.rect(screen, blue_efrei, (772, 332, 160, 160), border_radius=24)
        pygame.draw.rect(screen, (234, 234, 234), (774, 334, 156, 156), border_radius=24)
        screen.blit(play_button, (824, 376))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
