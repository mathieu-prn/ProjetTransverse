import pygame

# Initialize Pygame
print(pygame.init())

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
bg = pygame.image.load("assets/Common/Background.png") # Background
play_button = pygame.image.load("assets/Common/play_button.png") # Play button
font = pygame.font.Font("assets/Common/font.ttf", 36) # Main font

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

    width_rect, hight_rect, stroke, x_pos_rect, y_pos_rect= 232, 78,8, 48, 48

    # "Basket" Button
    pygame.draw.rect(screen, (blue_efrei), (x_pos_rect, y_pos_rect, width_rect, hight_rect), 0, 44)
    pygame.draw.rect(screen, ((255, 255, 255)), (x_pos_rect + stroke/2, y_pos_rect + stroke/2, width_rect-stroke, hight_rect-stroke), 0, 44)
    txt_basket = font.render("Basket", True, (blue_efrei))
    screen.blit(txt_basket, (x_pos_rect+56, y_pos_rect+12))

    # "Golf" Button
    s=108
    pygame.draw.rect(screen, (blue_efrei), (x_pos_rect, y_pos_rect+s, width_rect, hight_rect), 0, 44)
    pygame.draw.rect(screen, ((255, 255, 255)),(x_pos_rect + stroke / 2, (y_pos_rect + stroke / 2)+s, width_rect - stroke, hight_rect - stroke), 0,44)
    txt_golf = font.render("Golf", True, (blue_efrei))
    screen.blit(txt_golf, (x_pos_rect + 56, y_pos_rect + 12+s))

    # "Foot" Button
    s=216
    pygame.draw.rect(screen, (blue_efrei), (x_pos_rect, y_pos_rect + s, width_rect, hight_rect), 0, 44)
    pygame.draw.rect(screen, ((255, 255, 255)), (
    x_pos_rect + stroke / 2, (y_pos_rect + stroke / 2) + s, width_rect - stroke, hight_rect - stroke), 0, 44)
    txt_golf = font.render("Foot", True, (blue_efrei))
    screen.blit(txt_golf, (x_pos_rect + 56, y_pos_rect + 12 + s))

    # "Bowling" Button
    s=324
    pygame.draw.rect(screen, (blue_efrei), (x_pos_rect, y_pos_rect + s, width_rect, hight_rect), 0, 44)
    pygame.draw.rect(screen, ((255, 255, 255)), ( x_pos_rect + stroke / 2, (y_pos_rect + stroke / 2) + s, width_rect - stroke, hight_rect - stroke), 0, 44)
    txt_golf = font.render("Bowling", True, (blue_efrei))
    screen.blit(txt_golf, (x_pos_rect + 56, y_pos_rect + 12 + s))

    # Photo jeu
    pygame.draw.rect(screen, (blue_efrei), (398, 16, 534, 302), 0, 24)
    pygame.draw.rect(screen, ((234,234,234)), (400, 18, 530, 298), 0, 24)

    # Button historic
    pygame.draw.rect(screen, (blue_efrei), (398, 332, 160, 160), 0, 24)
    pygame.draw.rect(screen, ((234,234,234)), (400, 334, 156, 156), 0, 24)

    # Button play
    pygame.draw.rect(screen, (blue_efrei), (772, 332, 160, 160), 0, 24)
    pygame.draw.rect(screen, ((234, 234, 234)), (774, 334, 156, 156), 0, 24)
    screen.blit(play_button, (824, 376))



    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()