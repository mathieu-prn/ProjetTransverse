import math
from utility import *
import config

# Load images only once
IMAGE_CACHE = {}


def load_image(path):
    if path not in IMAGE_CACHE:
        IMAGE_CACHE[path] = pygame.image.load(path).convert_alpha()
    return IMAGE_CACHE[path]


# ---- Initialize global variables
SCREEN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))  # Initialize the screen
BG = load_image(config.BG)  # Load background image
# Colors
GREEN_GOLF = (148, 186, 134)
BUNKER_YELLOW = (237, 225, 141)
WATER_BLUE = (0, 167, 250)

DISPLAY_MSG = False  # When True, a win/lose message is shown
WON = False  # Win variable
ARROW_FOLLOW = True  # Controls whether the arrow follows the mouse or not

# list of borders
BORDER_WALLS = []


# --- Main Game Function
def run():
    """Main function for the golf game. Contains all classes and game logic.
        Called from game_select.py. Returns "Exit" to go back to the menu."""
    global DISPLAY_MSG, WON, ARROW_FOLLOW, BORDER_WALLS  # Allow to modify global variables
    pygame.display.set_caption("EfreiSport - Golf")

    # Level Handling Functions

    def get_font(size):
        """Returns a pygame font of size 'size'."""
        return pygame.font.Font(config.FONT, size)

    def getlevel():
        """Read and return the level number from the save file."""
        filename = "saves/golflevel.json"
        dico = loadfile(filename)
        level_value = dico.get("level", 1)
        print("Returned level:", level_value)
        return level_value

    def updatelevel(levelnumber):
        """Update the level number in the save file."""
        filename = "saves/golflevel.json"
        dico = loadfile(filename)
        dico["level"] = levelnumber
        with open(filename, "w") as file:
            json.dump(dico, file)
        soundeffect_save.play()
        print("Updated level", levelnumber)

    def updatescore(levelnumber, score):
        """Update the score of the current level only if it is better than the one already saved"""
        filename = "saves/golflevel.json"
        dico = loadfile(filename)
        if score > dico[str(levelnumber)]:
            dico[str(levelnumber)] = score
        with open(filename, "w") as file:
            json.dump(dico, file)

    def end_level():
        """Reset game state for a new level."""
        global ARROW_FOLLOW
        ball.velocity = 0
        score.reset()
        ball.rect.center = getrelativepos((25, 212.5))
        ARROW_FOLLOW = True

    def lose():
        """Handle a losing condition."""
        global DISPLAY_MSG, WON
        DISPLAY_MSG = True
        WON = False
        message.draw("lose")
        end_level()

    # Render Static Background
    def render_static_background(level):
        """Pre-renders static background with static elements."""
        static_bg = pygame.Surface((config.WIDTH, config.HEIGHT))
        static_bg.fill((240, 240, 240))
        static_bg.blit(BG, (0, 0))
        field.draw(static_bg)
        level.draw(static_bg)
        for bunker in level.level_bunkers:  # Level bunkers
            bunker.draw(static_bg)
        for water in level.level_water:  # Level water elements
            water.draw(static_bg)
        for wall in level.level_walls:  # Level walls
            wall.draw(static_bg)
        for wall in BORDER_WALLS:  # Border walls
            wall.draw(static_bg)
        level.hole.draw(static_bg)
        return static_bg

    # Game Object Classes
    class Ball(pygame.sprite.Sprite):
        """Represents the golf ball."""

        def __init__(self):
            super().__init__()
            self.image = pygame.transform.scale(load_image("assets/Golf/GolfBall.png"), (15, 15))  # Load the ball asset
            self.rect = self.image.get_rect()
            self.rect.center = getrelativepos((25, 212.5))
            self.velocity = 0  # Define the ball's velocity
            self.angle = 0  # Define the ball's trajectory angle

        def draw(self, surface=SCREEN):
            surface.blit(self.image, self.rect)

        def collision(self, walls_list, water_list):
            """Checks and handles collisions with obstacles."""
            # Water collision (resets ball)
            for water in water_list:
                if self.rect.colliderect(water.rect):
                    soundeffect_water.play()
                    self.velocity = 0  # Set the ball's velocity to 0
                    self.rect.center = getrelativepos((25, 212.5))  # Put the ball at its start position

            # Wall collision
            for wall in walls_list:
                if self.rect.inflate(5, 5).colliderect(wall.rect):  # Inflate for better detection
                    dx = min(abs(self.rect.right - wall.rect.left), abs(self.rect.left - wall.rect.right))
                    dy = min(abs(self.rect.bottom - wall.rect.top), abs(self.rect.top - wall.rect.bottom))
                    if dx < dy:  # Vertical collision
                        self.angle = math.pi - self.angle
                        self.rect.x += 2 * math.cos(self.angle)
                    elif dy < dx:  # Horizontal collision
                        self.angle = -self.angle
                        self.rect.y += 2 * math.sin(self.angle)
                    else:  # Corner collision
                        self.angle += math.pi
                        self.rect.x += 2 * math.cos(self.angle)
                        self.rect.y += 2 * math.sin(self.angle)
                    self.velocity *= 0.9  # Energy loss on bounce
                    soundeffect_collisions.play()
                    return True
            return False

        def unstuck(self):
            """Avoid as mush as possible getting the ball stucked in a wall"""
            if self.rect.left < field.rect.left:
                self.rect.center = (self.rect.center[0] + 4, self.rect.center[1])
            elif self.rect.right > field.rect.right:
                self.rect.center = (self.rect.center[0] - 4, self.rect.center[1])
            elif self.rect.top < field.rect.top:
                self.rect.center = (self.rect.center[0], self.rect.center[1] + 4)
            elif self.rect.bottom > field.rect.bottom:
                self.rect.center = (self.rect.center[0], self.rect.center[1] - 4)

        def update_position(self, launched):
            """Updates ball's position, velocity, and applies friction."""
            if launched:  # Check if the ball got launched, if True then it applies the velocity from the slider and the angle from the arrow
                self.velocity = slider.get_value() * 0.2
                self.angle = arrow.angle
            acceleration = -0.1  # Friction
            # Check if ball is in a bunker for extra deceleration.
            for bunker in game_state.level.level_bunkers:
                if self.rect.colliderect(bunker.rect):
                    acceleration = -0.7  # Bunker friction

            # Update trajectory
            vx = self.velocity * math.cos(self.angle)
            vy = self.velocity * math.sin(self.angle)
            x, y = self.rect.center
            self.rect.center = (x + vx, y + vy)
            self.velocity += acceleration  # Apply the friction
            if self.velocity < 0:  # No negative velocity possible
                self.velocity = 0

    class Slider(pygame.sprite.Sprite):
        """Slider used to adjust the ball's power"""

        def __init__(self):
            super().__init__()
            self.rect = pygame.Rect(25, 150, 30, 200)  # Rect of the slider
            self.slider_rect = pygame.Rect(25, 250, 30, 7)  # Rect of the slider handle
            self.dragging = False  # Boolean to control if the slider is being dragged

        def draw(self, surface=SCREEN):
            pygame.draw.rect(surface, config.BLUE_EFREI, self.rect.inflate(6, 6))
            pygame.draw.rect(surface, config.WHITE, self.rect)
            pygame.draw.rect(surface, config.BLACK, self.slider_rect)

        def handle_event(self, event):
            """Handle event for the slider."""
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.slider_rect.collidepoint(event.pos):  # If player clicks on the slider handle
                    self.dragging = True
                elif self.rect.collidepoint(event.pos):  # If player clicks somewhere in the slider area
                    self.slider_rect.y = max(self.rect.top, min(event.pos[1],
                                                                self.rect.bottom - self.slider_rect.height))  # Teleports the handle to the click position
                    self.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.slider_rect.y = max(self.rect.top, min(event.pos[1], self.rect.bottom - self.slider_rect.height))

        def get_value(self):
            min_y = self.rect.top
            max_y = self.rect.bottom - self.slider_rect.height
            return int(100 - (((self.slider_rect.y - min_y) / (max_y - min_y)) * 100)) + int(
                10 * ((self.slider_rect.y - min_y) / (max_y - min_y)))

    class Launch(pygame.sprite.Sprite):
        """The "Go!" button to launch the ball."""

        def __init__(self):
            super().__init__()
            self.rect = pygame.Rect(17, 396, 50, 80)
            self.color = config.WHITE

        def draw(self, surface=SCREEN):
            pygame.draw.rect(surface, config.BLUE_EFREI, self.rect.inflate(6, 6))  # Border
            pygame.draw.rect(surface, self.color, self.rect)
            font = get_font(30)
            text = font.render("Go!", True, config.BLUE_EFREI)
            surface.blit(text, (self.rect.x, self.rect.y + 25))

        def clicked(self, event):
            """Launch the ball when the button Go is clicked."""
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos) and ball.velocity == 0:
                    score.increment()  # Increment the score
                    self.color = config.GREY  # Change button color
                    soundeffect_swing.play()
                    ball.update_position(True)

    class Field(pygame.sprite.Sprite):
        """The green area corresponding to the field."""

        def __init__(self):
            super().__init__()
            # These are absolute screen coordinates
            self.rect = pygame.Rect(80, 55, 900, 425)

        def draw(self, surface=SCREEN):
            pygame.draw.rect(surface, GREEN_GOLF, self.rect)

    class Wall(pygame.sprite.Sprite):
        """A wall obstacle. They are either vertical or horizontal."""

        def __init__(self, relative_x, relative_y, width, height, is_border):
            super().__init__()
            self.color = config.BLUE_EFREI
            if is_border:  # When writing the code, it was easier to place borders using top-left coordinates
                self.rect = pygame.Rect(relative_x + 80, relative_y + 55, width, height)
            else:  # When writing the code, it was easier to place internal walls using center coordinates
                self.rect = pygame.Rect(relative_x + 80 - width / 2, relative_y + 55 - height / 2, width, height)

        def draw(self, surface=SCREEN):
            pygame.draw.rect(surface, self.color, self.rect)

    class Bunker(pygame.sprite.Sprite):
        """A sand bunker obstacle. It slows down the ball."""

        def __init__(self, pos, width, height):
            super().__init__()
            self.rect = pygame.Rect(0, 0, width, height)
            self.rect.center = pos

        def draw(self, surface=SCREEN):
            pygame.draw.rect(surface, BUNKER_YELLOW, self.rect)

    class Water(pygame.sprite.Sprite):
        """A water obstacle. It resets the ball to its starting position."""

        def __init__(self, pos, width, height):
            super().__init__()
            self.width = width
            self.height = height
            self.rect = pygame.Rect(0, 0, width, height)
            self.rect.center = pos

        def draw(self, surface=SCREEN):
            pygame.draw.rect(surface, WATER_BLUE, self.rect)

    class Arrow(pygame.sprite.Sprite):
        """Arrow showing ball trajectory direction and power."""

        def __init__(self, length=50):
            super().__init__()
            self.length = length
            self.direction = pygame.Vector2(1, 0)  # Initial direction (to the right)
            self.angle = 0

        def draw(self, surface=SCREEN):
            arrow_end = pygame.Vector2(ball.rect.center) + self.direction * (20 + slider.get_value())
            pygame.draw.line(surface, config.BLUE_EFREI, ball.rect.center, arrow_end,
                             3)  # The arrow starts from the ball center and ends at arrow_end

            # Compute and draw the arrowhead
            arrow_angle = math.atan2(-self.direction.y, -self.direction.x)
            arrow_size = 10
            left = (arrow_end.x + arrow_size * math.cos(arrow_angle + math.pi / 6),
                    arrow_end.y + arrow_size * math.sin(arrow_angle + math.pi / 6))
            right = (arrow_end.x + arrow_size * math.cos(arrow_angle - math.pi / 6),
                     arrow_end.y + arrow_size * math.sin(arrow_angle - math.pi / 6))
            pygame.draw.polygon(surface, config.BLUE_EFREI, [arrow_end, left, right])

        def update_direction(self, mouse_pos):
            """Updates the direction of the arrow when the global variable ARROW_FOLLOW is true."""
            global ARROW_FOLLOW
            if ball.velocity == 0 and ARROW_FOLLOW:  # If the ball's velocity is 0 and ARROW_FOLLOW is True
                direction = pygame.Vector2(mouse_pos) - pygame.Vector2(
                    ball.rect.center)  # Point the arrow towards the mouse position
                if direction.length() > 0:  # If the vector is not null
                    self.direction = direction.normalize()
                    self.angle = math.atan2(self.direction.y, self.direction.x)

    class Flag(pygame.sprite.Sprite):
        """The flag marking the hole."""

        def __init__(self, pos):
            super().__init__()
            self.image = load_image("assets/Golf/Flag.png")
            self.rect = self.image.get_rect()
            self.pos = (pos[0] - 7, pos[1] - 75)
            self.rect = pygame.Rect(pos[0] - self.rect.width / 2, pos[1] - self.rect.height, self.rect.width,
                                    self.rect.height)

        def draw(self, surface=SCREEN):
            surface.blit(self.image, self.pos)

    class Hole(pygame.sprite.Sprite):
        """The hole where the player has to put the ball."""

        def __init__(self, pos):
            super().__init__()
            self.image = load_image("assets/Golf/Hole.png")
            self.rect = self.image.get_rect(center=pos)
            # Smaller rect for collision (if the ball collides with the side of the hole, it won't go in).
            self.collision_rect = pygame.Rect(0, 0, 14, 14)
            self.collision_rect.center = self.rect.center

        def draw(self, surface=SCREEN):
            pygame.draw.circle(surface, config.WHITE, self.rect.center, 7)
            surface.blit(self.image, self.rect)

    class Level(pygame.sprite.Sprite):
        """Manages obstacles and layout for a specific level."""

        def __init__(self, number):
            super().__init__()
            self.number = number  # The number of the level
            self.level_walls = []  # List containing the walls of the level
            self.level_bunkers = []  # List containing the bunkers of the level
            self.level_water = []  # List containing the water elements of the level

            # Default hole position if not changed
            self.hole = Hole(getrelativepos((850, 212.5)))
            self.flag = Flag(getrelativepos((850, 212.5)))

            # Level definitions, each self.number block configures obstacles and potentially hole position
            if self.number == 1:
                self.level_walls.append(Wall(750, 212.5, 6, 200, False))

            elif self.number == 2:
                self.level_walls.append(Wall(150, 212.5, 6, 200, False))
                self.level_walls.append(Wall(750, 212.5, 6, 200, False))

            elif self.number == 3:
                self.hole = Hole(getrelativepos((850, 50)))
                self.flag = Flag(getrelativepos((850, 50)))
                self.level_walls.append(Wall(750, 150, 6, 300, False))
                self.level_walls.append(Wall(150, 275, 6, 300, False))

            elif self.number == 4:
                self.hole = Hole(getrelativepos((850, 50)))
                self.flag = Flag(getrelativepos((850, 50)))
                self.level_walls.append(Wall(750, 150, 6, 300, False))
                self.level_walls.append(Wall(150, 275, 6, 300, False))
                self.level_walls.append(Wall(450, 212.5, 6, 300, False))
            elif self.number == 5:
                self.hole = Hole(getrelativepos((850, 75)))
                self.flag = Flag(getrelativepos((850, 75)))
                self.level_walls.append(Wall(750, 150, 6, 300, False))
                self.level_walls.append(Wall(150, 275, 6, 300, False))
                self.level_bunkers.append(Bunker(getrelativepos((450, 75)), 300, 150))
                self.level_bunkers.append(Bunker(getrelativepos((450, 350)), 300, 150))

            elif self.number == 6:
                self.hole = Hole(getrelativepos((850, 212.5)))
                self.flag = Flag(getrelativepos((850, 212.5)))
                self.level_bunkers.append(Bunker(getrelativepos((450, 212.5)), 600, 250))

            elif self.number == 7:
                self.hole = Hole(getrelativepos((850, 400)))
                self.flag = Flag(getrelativepos((850, 400)))
                self.level_walls.append(Wall(400, 275, 6, 300, False))
                self.level_walls.append(Wall(650, 100, 6, 200, False))
                self.level_bunkers.append(Bunker(getrelativepos((600, 325)), 200, 100))

            elif self.number == 8:
                self.hole = Hole(getrelativepos((850, 75)))
                self.flag = Flag(getrelativepos((850, 75)))
                self.level_bunkers.append(Bunker(getrelativepos((250, 275)), 100, 300))
                self.level_bunkers.append(Bunker(getrelativepos((650, 150)), 100, 300))
                self.level_bunkers.append(Bunker(getrelativepos((250, 37.5)), 100, 75))
                self.level_bunkers.append(Bunker(getrelativepos((650, 386.5)), 100, 75))

            elif self.number == 9:
                self.hole = Hole(getrelativepos((850, 50)))
                self.flag = Flag(getrelativepos((850, 50)))
                self.level_walls.append(Wall(150, 325, 6, 200, False))
                self.level_walls.append(Wall(750, 325, 6, 200, False))
                self.level_walls.append(Wall(450, 160, 6, 280, False))
                self.level_walls.append(Wall(450, 300, 300, 6, False))

            elif self.number == 10:
                self.hole = Hole(getrelativepos((850, 300)))
                self.flag = Flag(getrelativepos((850, 300)))
                self.level_walls.append(Wall(300, 212.5, 6, 250, False))
                self.level_walls.append(Wall(600, 100, 6, 200, False))
                self.level_bunkers.append(Bunker(getrelativepos((600, 325)), 250, 100))

            elif self.number == 11:
                self.hole = Hole(getrelativepos((850, 375)))
                self.flag = Flag(getrelativepos((850, 375)))
                self.level_walls.append(Wall(200, 75 / 2, 6, 75, False))
                self.level_walls.append(Wall(200, 425 - 275 / 2, 6, 275, False))
                self.level_walls.append(Wall(450, 175 / 2, 6, 175, False))
                self.level_walls.append(Wall(450, 425 - 175 / 2, 6, 175, False))
                self.level_walls.append(Wall(700, 275 / 2, 6, 275, False))
                self.level_walls.append(Wall(700, 425 - 75 / 2, 6, 75, False))

            elif self.number == 12:
                self.hole = Hole(getrelativepos((850, 212.5)))
                self.flag = Flag(getrelativepos((850, 212.5)))
                self.level_water.append(Water(getrelativepos((450, 212)), 450, 212))

            elif self.number == 13:
                self.level_bunkers.append(Bunker(getrelativepos((300, 125)), 200, 100))
                self.level_bunkers.append(Bunker(getrelativepos((300, 300)), 200, 100))
                self.level_water.append(Water(getrelativepos((600, 212)), 200, 100))

            elif self.number == 14:
                self.level_walls.append(Wall(200, 212.5, 6, 300, False))
                self.level_water.append(Water(getrelativepos((500, 75)), 250, 150))
                self.level_water.append(Water(getrelativepos((500, 350)), 250, 150))

            # Combine border walls with level-specific walls
            self.all_walls = BORDER_WALLS + self.level_walls

            # level number display:
            self.font = get_font(28)
            self.fontcolor = config.BLUE_EFREI

        def draw(self, surface):
            # Blit the level number display
            msg = "Level " + str(self.number)
            text = self.font.render(msg, True, self.fontcolor)
            surface.blit(text, (300, 10))

    class Score(pygame.sprite.Sprite):
        """Manages and displays player's score (shots and points)."""

        def __init__(self):
            super().__init__()
            self.score = 0  # Points for current level (max 5)
            self.shots = 0  # Number of shots taken (max 5)
            self.font = get_font(28)

        def increment(self):
            if self.shots < 5:  # Max 5 shots
                self.shots += 1
            self.score = 6 - self.shots  # 5 points for hole-in-one, 1 for 5 shots

        def reset(self):  # Reset shots number
            self.shots = 0
            self.score = 0

        def draw(self, surface=SCREEN):
            text = self.font.render(f"Shots: {self.shots}", True, config.BLUE_EFREI)
            surface.blit(text, (10, 10))

    class Message(pygame.sprite.Sprite):
        """Displays win/lose messages and handles interaction."""

        def __init__(self):
            super().__init__()
            self.font = get_font(28)
            self.fontcolor = config.BLUE_EFREI
            self.button_width, self.button_height = 150, 50  # Dimensions of the confirm button
            self.button_pos = (500 - self.button_width / 2, 275)
            self.button_color = config.WHITE
            self.button_rect = pygame.Rect(self.button_pos, (self.button_width, self.button_height))

        def draw(self, msg_type, surface=SCREEN):
            """Prepares the text renders for the message and button and draw them."""
            if msg_type == "win":
                if score.shots == 1:
                    msg = f"Hole-in-one! Score: {score.score}/5"
                else:
                    msg = f"Won in {score.shots} shots! Score: {score.score}/5."
                button_msg = "Next level"
            elif msg_type == "lose":
                msg = "Max shots reached. Try again!"
                button_msg = "Try again"
            else:
                msg = "Message not defined"  # Handle error (should not happen but it's here)
                button_msg = "OK"

            # Draw
            text = self.font.render(msg, True, config.BLACK)
            text_width, text_height = text.get_size()
            surface.blit(text, (surface.get_width() / 2 - text_width / 2, surface.get_height() / 2 - text_height / 2))
            pygame.draw.rect(surface, config.BLACK, self.button_rect.inflate(6, 6))
            pygame.draw.rect(surface, self.button_color, self.button_rect)

            button_text = self.font.render(button_msg, True, config.BLACK)

            # Below is to center the text in the button
            tbutton_width, tbutton_height = button_text.get_size()
            tbuttonx = self.button_pos[0] + ((self.button_width - tbutton_width) / 2)
            tbuttony = self.button_pos[1] + ((self.button_height - tbutton_height) / 2)
            surface.blit(button_text, (tbuttonx, tbuttony))  # Draw the text

        def clicked(self, event):
            """Handles clicks on the message button. Updates the static bg if needed."""
            global DISPLAY_MSG
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    soundeffect_clicked.play()
                    if WON:  # Player won
                        self.button_color = config.GREY
                        updatescore(game_state.level.number, score.score)
                        new_level = game_state.level.number + 1
                        print(new_level)
                        if new_level % 5 == 0:  # Save every 5 levels
                            updatelevel(new_level)
                        game_state.level.number = new_level
                        end_level()
                        game_state.level = Level(game_state.level.number)
                    else:  # Player lost
                        end_level()
                        game_state.level.number = getlevel()  # Reload the checkpoint (saved level)
                        game_state.level = Level(game_state.level.number)
                    game_state.static_background = render_static_background(game_state.level)
                    DISPLAY_MSG = False  # Make the message disappear

    class Resetbutton(pygame.sprite.Sprite):
        """Button to reset to the last saved checkpoint."""

        def __init__(self):
            super().__init__()
            # Defining needed attributes
            self.font = get_font(24)
            self.fontcolor = config.BLUE_EFREI
            self.text = self.font.render("Go back to checkpoint", True, self.fontcolor)
            self.width, self.height = self.text.get_size()
            self.pos = (1000 - 100 - self.width, 10)
            self.color = config.WHITE
            self.rect = pygame.Rect(self.pos, (self.width, self.height))

        def draw(self, surface=SCREEN):
            pygame.draw.rect(surface, self.fontcolor, self.rect.inflate(6, 6))
            pygame.draw.rect(surface, self.color, self.rect)
            surface.blit(self.text, self.pos)

        def clicked(self, event):
            """Reload checkpoint and updates static bg."""
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    print("Clicked")
                    soundeffect_clicked.play()
                    self.color = config.GREY
                    end_level()  # Resets game state
                    game_state.level = Level(getlevel())  # Loads last saved checkpoint
                    game_state.static_background = render_static_background(game_state.level)  # Loads level

            elif event.type == pygame.MOUSEBUTTONUP:
                self.color = config.WHITE

    class GameState:
        """Contains the current level and the pre-rendered static background."""

        def __init__(self, level):
            self.level = level
            self.static_background = render_static_background(level)

    # Create Game Objects
    field = Field()

    # Create border walls (they don't change between levels)
    bordertop = Wall(0, 0, 900, 6, True)
    borderbottom = Wall(0, 425, 900, 6, True)
    borderleft = Wall(0, 0, 6, 425, True)
    borderright = Wall(900, 0, 6, 431, True)
    BORDER_WALLS.extend([bordertop, borderbottom, borderleft, borderright])

    ball = Ball()  # The ball
    slider = Slider()  # The slider
    launch_button = Launch()  # The "Go!" button
    arrow = Arrow()  # The arrow
    score = Score()  # The score, shots counter and display for them
    message = Message()  # The win/lose message
    game_state = GameState(Level(getlevel()))  # General game state, initalized with the saved level
    resetbutton = Resetbutton()  # The button to reset to the checkpoint

    # Define sound effects
    soundeffect_hole = pygame.mixer.Sound("assets/Golf/Sounds/hole.mp3")
    soundeffect_swing = pygame.mixer.Sound("assets/Golf/Sounds/swing.mp3")
    soundeffect_collisions = pygame.mixer.Sound("assets/Golf/Sounds/collisions.mp3")
    soundeffect_water = pygame.mixer.Sound("assets/Golf/Sounds/water.mp3")
    soundeffect_save = pygame.mixer.Sound("assets/Golf/Sounds/save.mp3")
    soundeffect_clicked = pygame.mixer.Sound("assets/Common/Sounds/clicked.mp3")

    clock = pygame.time.Clock()
    running = True

    # Main Game Loop
    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if DISPLAY_MSG:  # If a win/lose message is active
                message.clicked(event)

            else:  # Normal gameplay event handling
                slider.handle_event(event)  # Event handling for slider
                launch_button.clicked(event)  # Event handling for launch button
                resetbutton.clicked(event)  # Event handling for reset button

                if event.type == pygame.MOUSEBUTTONDOWN and ball.velocity == 0:
                    # Toggle arrow follow
                    if ARROW_FOLLOW:
                        ARROW_FOLLOW = False  # Lock arrow
                    else:
                        if field.rect.collidepoint(event.pos):  # Click on field to re-enable it
                            ARROW_FOLLOW = True

                if event.type == pygame.MOUSEBUTTONUP:  # Reset buttons color when the mouse button is released
                    launch_button.color = config.WHITE
                    message.button_color = config.WHITE
                    resetbutton.color = config.WHITE

                if event.type == pygame.KEYDOWN:  # Keys detection
                    if event.key == pygame.K_ESCAPE:  # Go back to menu if escape is pressed
                        return "Exit"

                    keys = pygame.key.get_pressed()  # For shortcuts (multiple keys pressed at the time)
                    # Cheats
                    if keys[pygame.K_LCTRL] and keys[pygame.K_LALT] and (
                            keys[pygame.K_KP_PLUS] or keys[pygame.K_KP_MINUS] or keys[pygame.K_KP_DIVIDE]):
                        if keys[pygame.K_KP_PLUS]:  # jump to next level with LCTRL+LALT+"+"
                            newlvl = game_state.level.number + 1
                        elif keys[pygame.K_KP_MINUS]:  # jump to previous level with LCTRL+LALT+"-"
                            newlvl = game_state.level.number - 1
                        elif keys[pygame.K_KP_DIVIDE]:  # reset level number to 0 with LCTRL+LALT+"/"
                            newlvl = 0
                        end_level()  # Reset level

                        # Load the new level newlvl
                        game_state.level.number = newlvl
                        game_state.level = Level(game_state.level.number)
                        game_state.static_background = render_static_background(game_state.level)

                        print("gamestate loaded with level" + str(game_state.level.number))

        # Game logic
        # Blit the static background
        SCREEN.blit(game_state.static_background, (0, 0))
        score.draw()
        if not game_state.level.flag.rect.colliderect(ball.rect) or ball.velocity != 0:
            game_state.level.flag.draw(SCREEN)

        if DISPLAY_MSG:  # If a win/lose message is active
            if WON:
                message.draw("win")  # Draw the win message
            else:
                message.draw("lose")  # Draw the loss message
        else:  # If no win/lose message is active
            if ball.velocity > 0:  # If the ball is moving, handle the collision
                ball.collision(game_state.level.all_walls, game_state.level.level_water)

            else:  # Ball isn't moving - we handle the arrow and draw the buttons
                arrow.update_direction(pygame.mouse.get_pos())
                arrow.draw()
                slider.draw()
                launch_button.draw()
                resetbutton.draw()

            ball.unstuck()  # Avoid getting the ball stucked somewhere
            ball.update_position(False)  # Update ball's position (False because it's not being launched)

            if game_state.level.hole.collision_rect.colliderect(
                    ball.rect) and ball.velocity < 10:  # Win condition --> If the ball collides with the colliderect of the hole and it isn't too fast
                soundeffect_hole.play()
                WON = True  # Player Won
                DISPLAY_MSG = True  # Display the message
            elif ball.velocity == 0 and score.shots == 5:  # If the ball isn't in the hole after 5 shots
                lose()  # Player Lose
            else:  # If player didn't win nor lose, draw the ball as the player is still playing
                ball.draw()

        pygame.display.flip()  # Update the display once all changes done
        clock.tick(60)  # 60 FPS

    pygame.quit()