import pygame

# Initialize Pygame
print(pygame.init())

# Set up the game window
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport - Menu")
bg = pygame.image.load("assets/Background.png")
pygame_icon = pygame.image.load('assets/logo.png')
pygame.display.set_icon(pygame_icon)

font = pygame.font.Font("../ProjetTransverse/assets/font.ttf", 48)

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
    # Overlay "efrei sport"
    screen.fill((240,240,240, 0.5))
    screen.blit(bg,(0, 0))

    # Logo top right
    logo_long = pygame.image.load("assets/Logo long EFREI sport.png")
    screen.blit(logo_long, (345, 32))

    # Blue Lines
    pygame.draw.line(screen, blue_efrei, (0,172), (1000,172), width=16)
    pygame.draw.line(screen, blue_efrei, (0, 172+32), (1000, 172+32), width=16)

    # 2/3 bottom rect
    pygame.draw.rect(screen,(201,201,201),(0,330,1000,176))

    # "Menu" Button
    pygame.draw.rect(screen,(blue_efrei),(90,360,348,98 ),0,48) # Blue border of the button
    pygame.draw.rect(screen, ((255, 255, 255)), (90+6, 360+6, 348-12, 98-12), 0, 48) #Fill
    txt_menu = font.render("Menu", True, (blue_efrei))
    screen.blit(txt_menu, (202, 372))

    # "Start" Button
    pygame.draw.rect(screen, (blue_efrei), (564, 360, 348, 98), 0, 48)
    pygame.draw.rect(screen, ((255, 255, 255)), (564 + 6, 360 + 6, 348 - 12, 98 - 12), 0, 48)
    txt_start = font.render("Start", True, (blue_efrei))
    screen.blit(txt_start, (676, 372))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    clicked = 0
    if (564 <= mouse_x <= 564 + 348 and 360 <= mouse_y <= 360 + 98 and clicked == 0):
        if pygame.mouse.get_pressed()[0]:
            clicked += 1
            print("click")
            screen.fill((240, 240, 240, 0.5))
            pygame.display.flip()
            break

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()