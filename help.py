from utility import *
import config

# Load images only once
IMAGE_CACHE = {}
def load_image(path):
    if path not in IMAGE_CACHE:
        IMAGE_CACHE[path] = pygame.image.load(path).convert_alpha()
    return IMAGE_CACHE[path]

# ---- Initialize global variables
SCREEN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

#Sounds and files
soundeffect_clicked=pygame.mixer.Sound("assets/Common/Sounds/clicked.mp3")

def run(game):
    print("Help :",str(game),"is running")
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
        """Title of the window."""
        def __init__(self,game):
            super().__init__()
            self.name = "How to play: " + str(game) # Show for what game the help is
        def draw(self):
            font=get_font(40)
            text= font.render(self.name, True, config.BLUE_EFREI)
            rect=text.get_rect()
            SCREEN.blit(text, (500-rect[2]/2,10))

    class Text(pygame.sprite.Sprite):
        """Content of the help."""
        def __init__(self,game):
            super().__init__()
            self.h1font = get_font(27)
            self.textfont= get_font(17)
            self.blit_dest = [30,75] # The destination to blit the next chunk of text
            if game=="Golf":
                # self.text: list of tuples each composed of the font to be used and the text to be displayed
                self.text=[
                    ("h1font", "Goal of the game"),
                    ("textfont", "  The goal is to put the ball in the hole in the fewest shots possible."),
                    ("textfont", "  There are levels of increasing difficulty. Your progression is saved every 5 levels."),
                    ("textfont", "  You have 5 shots maximum to put the ball in the hole. If you don't succeed, you will"),
                    ("textfont", "  be back at the last checkpoint. There are different obstacles. In blue, the walls which block and reflect the ball."),
                    ("textfont", "  In yellow, the bunkers which slow down the ball."),
                    ("textfont", "  Finally, in blue there are the water elements which will reset your ball position if you go in them."),
                    ("h1font", "Controls"),
                    ("textfont", "  You can change the ball's direction by moving your mouse around. You can see in which direction the ball will go"),
                    ("textfont", "  thanks to the arrow. You can lock its direction by clicking. You can unlock it by clicking on the field again."),
                    ("textfont", "  You can adjust the force of the shot with the slider on the left."),
                    ("textfont", "  When you are ready, click on the \"Go!\" button to shoot the ball!")
                    ]
            elif game=="Basket":
                self.text=[
                    ("h1font", "WARNING"),
                    ("textfont", "   This is a 2 players game"),
                    ("h1font", "Goal of the game"),
                    ("textfont","   The goal is to score more points than your opponent by making basket with the fewest bounces possible."),
                    ("textfont","   There are 4 levels of increasing difficulty. The points are awarded immediately after you make a basket, and"),
                    ("textfont","   then the shot is given to your opponent. There are obstacles in the levels, they are blue walls that will block"),
                    ("textfont","   and reflect the ball."),
                    ("textfont","   The winner of the game is the player with the most points."),
                    ("h1font", "Controls"),
                    ("textfont","   You can change the ball's direction by moving your mouse around. You can see in which direction the ball will go"),
                    ("textfont","   thanks to the arrow. You can lock its direction by clicking. You can unlock it by clicking on the field again."),
                    ("textfont","   The force of the shot is random, so when you are ready, click on the \"Go!\" button to shoot the ball!")]
            elif game=="Penalty":
                self.text=[("textfont","nothing")]
        def draw(self):
            """Draw the text and handle the blit destination."""
            for tuple in self.text: # For each line
                if tuple[0]=="h1font": # If it is a title use the title font size, blit on the screen and accordingly move down the blit destination
                    text_to_blit=self.h1font.render(tuple[1], True, config.BLACK)
                    rect = text_to_blit.get_rect()
                    SCREEN.blit(text_to_blit, (self.blit_dest[0],self.blit_dest[1]+5)) # +5 to add some space between sections
                    self.blit_dest[1]+=rect.height
                elif tuple[0]=="textfont": # If it is a text content use the text font size, blit on the screen and accordingly move down the blit destination
                    text_to_blit = self.textfont.render(tuple[1], True, config.BLACK)
                    rect = text_to_blit.get_rect()
                    SCREEN.blit(text_to_blit, self.blit_dest)
                    self.blit_dest[1] += rect.height
        def reset_blit_dest(self):
            """Once everything is drawn, reset the destination for the next frame."""
            self.blit_dest = [30,75]


    #Game Objects Creation
    backarrow = BackArrow()
    title= Title(game)
    text= Text(game)

    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        pygame.display.set_caption("EfreiSport - Help")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if backarrow.clicked(): #Back to the menu when the back arrow is clicked
                    return "Exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #Back to the menu when escape is pressed
                    return "Exit"

        #fill with a white-grey (no background to improve readability)
        SCREEN.fill((240, 240, 240, 0.5))

        # Design of the page
        backarrow.draw()
        title.draw()
        text.draw()
        text.reset_blit_dest()
        # Update the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(60)

    # Quit the game
    pygame.quit()