import pygame
print("menu.py ran")
import game_select as gameselect

# Initialize Pygame
pygame.init()
# Set up the game window
# Size
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("EfreiSport - Menu") # Title
# Top left icon
pygame_icon = pygame.image.load('assets/Common/logo.png')
pygame.display.set_icon(pygame_icon)


# Assets loads
BG = pygame.image.load("assets/Common/Background.png") # Background
logo_long = pygame.image.load("assets/Common/Logo long EFREI sport.png") # Logo
font = pygame.font.Font("assets/Common/font.ttf", 48) # Main font

# Initialize Colors
red=(255,0,0)
green=(0,255,0)
blue_efrei=(18,121,190)


clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Design of the page

    # Overlay "efrei sport"
    screen.fill((240,240,240, 0.5))
    screen.blit(BG,(0, 0))

    # Logo top right
    screen.blit(logo_long, (345, 32))

    # Blue Lines
    pygame.draw.line(screen, blue_efrei, (0,172), (1000,172), width=16)
    pygame.draw.line(screen, blue_efrei, (0, 172+32), (1000, 172+32), width=16)

    # 2/3 bottom grey rect
    pygame.draw.rect(screen,(201,201,201),(0,330,1000,176))

    # "Menu" Button
    pygame.draw.rect(screen,(blue_efrei),(90,360,348,98 ),0,48) # Blue border of the button
    pygame.draw.rect(screen, ((255, 255, 255)), (90+6, 360+6, 348-12, 98-12), 0, 48) #Fill
    txt_menu = font.render("Settings", True, (blue_efrei)) # Load text
    screen.blit(txt_menu, (167, 372)) # Display text at (202,372)

    # "Start" Button
    pygame.draw.rect(screen, (blue_efrei), (564, 360, 348, 98), 0, 48) # Blue border of the button
    pygame.draw.rect(screen, ((255, 255, 255)), (564 + 6, 360 + 6, 348 - 12, 98 - 12), 0, 48) #Fill
    txt_start = font.render("Start", True, (blue_efrei)) # Load text
    screen.blit(txt_start, (676, 372)) # Display text at (202,372)

    # Usability of the page
    mouse_x, mouse_y = pygame.mouse.get_pos()
    clicked = 0

    # "Menu button"
    if (90 <= mouse_x <= 90 + 348 and 360 <= mouse_y <= 360 + 98 and clicked == 0):
        if pygame.mouse.get_pressed()[0]:
            clicked = 1
            print("click")
            screen.fill((0, 0, 0, 0.5))
            pygame.display.flip()
        if clicked > 0:
            screen.fill((0, 0, 0, 0.5))
            pygame.display.flip()


    # "Start button"
    if (564 <= mouse_x <= 564 + 348 and 360 <= mouse_y <= 360 + 98 and clicked == 0):
        if pygame.mouse.get_pressed()[0]:
            print("Start button clicked")
            pygame.time.wait(200)  # Avoid multiple clicks
            gameselect.run(screen,BG,font) #RUN GAME_SELECT
            # Re-initialize the menu display after returning from game_select
        if clicked > 0:
            screen.fill((240, 240, 240, 0.5))
            pygame.display.flip()

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()