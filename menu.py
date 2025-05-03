import pygame
import config
print("menu.py ran")
import game_select as gameselect

# Initialize Pygame
pygame.init()
pygame.mixer.init()
# Set up the game window
SCREEN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

pygame.display.set_caption("EfreiSport - Menu") # Title
# Top left icon
pygame_icon = pygame.image.load('assets/Common/logo.png')
pygame.display.set_icon(pygame_icon)


# Assets loads
BG = pygame.image.load(config.BG) # Background
logo_long = pygame.image.load("assets/Common/Logo long EFREI sport.png") # Logo
FONT = pygame.font.Font(config.FONT, 48) # Main FONT
soundeffect_clicked=pygame.mixer.Sound("assets/Common/Sounds/clicked.mp3")


clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # "Start button"
            if (564 <= mouse_x <= 564 + 348 and 360 <= mouse_y <= 360 + 98):
                print("Start button clicked")
                soundeffect_clicked.play()
                pygame.time.wait(200)  # Avoid multiple clicks
                if gameselect.run(FONT, BG) == "Exit":  # run game_select and handle the exit
                    pygame.event.clear()

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

    # "Menu" Button
    pygame.draw.rect(SCREEN,(config.BLUE_EFREI),(90,360,348,98 ),0,48) # Blue border of the button
    pygame.draw.rect(SCREEN, ((255, 255, 255)), (90+6, 360+6, 348-12, 98-12), 0, 48) #Fill
    txt_menu = FONT.render("Settings", True, (config.BLUE_EFREI)) # Load text
    SCREEN.blit(txt_menu, (167, 372)) # Display text at (202,372)

    # "Start" Button
    pygame.draw.rect(SCREEN, (config.BLUE_EFREI), (564, 360, 348, 98), 0, 48) # Blue border of the button
    pygame.draw.rect(SCREEN, ((255, 255, 255)), (564 + 6, 360 + 6, 348 - 12, 98 - 12), 0, 48) #Fill
    txt_start = FONT.render("Start", True, (config.BLUE_EFREI)) # Load text
    SCREEN.blit(txt_start, (676, 372)) # Display text at (202,372)

    # Usability of the page
    mouse_x, mouse_y = pygame.mouse.get_pos()
    clicked = 0

    # "Menu button"
    if (90 <= mouse_x <= 90 + 348 and 360 <= mouse_y <= 360 + 98 and clicked == 0):
        if pygame.mouse.get_pressed()[0]:
            clicked = 1
            print("click")
            SCREEN.fill((0, 0, 0, 0.5))
            pygame.display.flip()
        if clicked > 0:
            SCREEN.fill((0, 0, 0, 0.5))
            pygame.display.flip()
        if clicked > 0:
            SCREEN.fill((240, 240, 240, 0.5))
            pygame.display.flip()

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()