# Selection of the game by the user
import pygame
# Initialize Pygame
print(pygame.init())

# Set up the game window
WIDTH = 1000
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport - Menu")
bg = pygame.image.load("assets/Background.png")

font = pygame.font.Font("../ProjetTransverse/assets/font.ttf", 36)

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


    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit the game
pygame.quit()