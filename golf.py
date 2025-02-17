import pygame, json, math

from game_select import width_rect
from utility import *

# ---------- Resource Caching ----------
IMAGE_CACHE = {}
def load_image(path):
    if path not in IMAGE_CACHE:
        IMAGE_CACHE[path] = pygame.image.load(path).convert_alpha()
    return IMAGE_CACHE[path]

# ---------- Initialization & Global Setup ----------
pygame.init()

WIDTH, HEIGHT = 1000, 500
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EfreiSport - Golf")
BG = load_image("assets/Background.png")
ICON = load_image("assets/logo.png")
pygame.display.set_icon(ICON)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE_EFREI = (18, 121, 190)
GREY = (211, 211, 211)
GREEN = (148, 186, 134)
BUNKER_YELLOW = (237, 225, 141)
WATER_BLUE = (0,167,250)

# Global game state variables
display_msg = False   # When True, a win/lose message is shown
won = False
arrow_follow = True   # Controls whether the arrow follows the mouse

# We'll keep border walls in a dedicated list.
border_walls = []

# ---------- Level Handling Functions ----------
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

def end_level():
    """Reset game state for a new level."""
    global arrow_follow
    ball.velocity = 0
    score.reset()
    ball.rect.center = getrelativepos((25, 212.5))
    arrow_follow = True

def lose():
    """Handle a losing condition."""
    global display_msg, won
    display_msg = True
    won = False
    message.draw("lose")
    end_level()

# ---------- Game Object Classes ----------
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(load_image("assets/Golf/GolfBall.png"), (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = getrelativepos((25, 212.5))
        self.velocity = 0
        self.angle = 0

    def draw(self):
        SCREEN.blit(self.image, self.rect)

    def collision(self, walls_list,water_list):
        # Check collision against each wall in the list.
        for water in water_list:
            if self.rect.colliderect(water.rect):
                ball.velocity = 0
                ball.rect.center = getrelativepos((25, 212.5))
        for wall in walls_list:
            if self.rect.inflate(5, 5).colliderect(wall.rect):
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
                return True
        return False

    def unstuck(self):
        if self.rect.left < field.rect.left:
            self.rect.center = (self.rect.center[0] + 4, self.rect.center[1])
        elif self.rect.right > field.rect.right:
            self.rect.center = (self.rect.center[0] - 4, self.rect.center[1])
        elif self.rect.top < field.rect.top:
            self.rect.center = (self.rect.center[0], self.rect.center[1] + 4)
        elif self.rect.bottom > field.rect.bottom:
            self.rect.center = (self.rect.center[0], self.rect.center[1] - 4)

    def update_position(self, launched):
        if launched:
            self.velocity = slider.get_value() * 0.2
            self.angle = arrow.angle
        acceleration = -0.1
        # Check if the ball is in contact with any bunker from the current level.
        for bunker in level.level_bunkers:
            if self.rect.colliderect(bunker.rect):
                acceleration = -1
        vx = self.velocity * math.cos(self.angle)
        vy = self.velocity * math.sin(self.angle)
        x, y = self.rect.center
        self.rect.center = (x + vx, y + vy)
        self.velocity += acceleration
        if self.velocity < 0:
            self.velocity = 0

class Slider(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(25, 150, 30, 200)
        self.slider_rect = pygame.Rect(25, 250, 30, 7)
        self.dragging = False

    def draw(self):
        pygame.draw.rect(SCREEN, BLUE_EFREI, self.rect.inflate(6, 6))
        pygame.draw.rect(SCREEN, WHITE, self.rect)
        pygame.draw.rect(SCREEN, BLACK, self.slider_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.slider_rect.y = max(self.rect.top, min(event.pos[1], self.rect.bottom - self.slider_rect.height))

    def get_value(self):
        min_y = self.rect.top
        max_y = self.rect.bottom - self.slider_rect.height
        return int(100 - ((self.slider_rect.y - min_y) / (max_y - min_y)) * 100)

class Launch(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(17, 396, 50, 80)
        self.color = WHITE

    def draw(self):
        pygame.draw.rect(SCREEN, BLUE_EFREI, self.rect.inflate(6, 6))
        pygame.draw.rect(SCREEN, self.color, self.rect)
        font = pygame.font.Font(None, 45)
        text = font.render("Go!", True, BLUE_EFREI)
        SCREEN.blit(text, (self.rect.x, self.rect.y + 30))

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and ball.velocity == 0:
                score.increment()
                self.color = GREY
                ball.update_position(True)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.color = WHITE

class Field(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(80, 55, 900, 425)

    def draw(self):
        pygame.draw.rect(SCREEN, GREEN, self.rect)

class Wall(pygame.sprite.Sprite):
    def __init__(self, relative_x, relative_y, width, height, is_border):
        super().__init__()
        self.color = BLUE_EFREI
        if is_border:
            self.rect = pygame.Rect(relative_x + 80, relative_y + 55, width, height)
        else:
            self.rect = pygame.Rect(relative_x + 80 - width / 2, relative_y + 55 - height / 2, width, height)

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)

class Bunker(pygame.sprite.Sprite):
    def __init__(self, pos, width, height):
        super().__init__()
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = pos

    def draw(self):
        pygame.draw.rect(SCREEN, BUNKER_YELLOW, self.rect)

class Water(pygame.sprite.Sprite):
    def __init__(self, pos, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center= pos

    def draw(self):
        pygame.draw.rect(SCREEN, WATER_BLUE, self.rect)

class Arrow(pygame.sprite.Sprite):
    def __init__(self, length=50):
        super().__init__()
        self.length = length
        self.direction = pygame.Vector2(1, 0)
        self.angle = 0

    def draw(self):
        arrow_end = pygame.Vector2(ball.rect.center) + self.direction * (20 + slider.get_value())
        pygame.draw.line(SCREEN, BLUE_EFREI, ball.rect.center, arrow_end, 3)
        self.angle = math.atan2(self.direction.y, self.direction.x)
        arrow_angle = math.atan2(-self.direction.y, -self.direction.x)
        arrow_size = 10
        left = (arrow_end.x + arrow_size * math.cos(arrow_angle + math.pi / 6),arrow_end.y + arrow_size * math.sin(arrow_angle + math.pi / 6))
        right = (arrow_end.x + arrow_size * math.cos(arrow_angle - math.pi / 6),arrow_end.y + arrow_size * math.sin(arrow_angle - math.pi / 6))
        pygame.draw.polygon(SCREEN, BLUE_EFREI, [arrow_end, left, right])

    def update_direction(self, mouse_pos):
        global arrow_follow
        if ball.velocity == 0 and arrow_follow:
            direction = pygame.Vector2(mouse_pos) - pygame.Vector2(ball.rect.center)
            if direction.length() > 0:
                self.direction = direction.normalize()
                self.angle = math.atan2(self.direction.y, self.direction.x)

class Flag(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image("assets/Golf/Flag.png")
        self.rect = self.image.get_rect()
        self.pos = (pos[0] - 7, pos[1] - 75)
        self.rect = pygame.Rect(pos[0] - self.rect.width / 2, pos[1] - self.rect.height,
                                self.rect.width, self.rect.height)
    def draw(self):
        SCREEN.blit(self.image, self.pos)

class Hole(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image("assets/Golf/Hole.png")
        self.rect = self.image.get_rect(center=pos)
        self.collision_rect = pygame.Rect(0, 0, 14, 14)
        self.collision_rect.center = self.rect.center

    def draw(self):
        pygame.draw.circle(SCREEN, WHITE, self.rect.center, 7)
        SCREEN.blit(self.image, self.rect)

class Level(pygame.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        self.number = number
        self.level_walls = []    # Level-specific walls
        self.level_bunkers = []  # Level-specific bunkers
        self.level_water = [] #Level-specific water elements
        self.hole = Hole(getrelativepos((850, 212.5)))
        self.flag = Flag(getrelativepos((850, 212.5)))

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
            self.level_walls.append(Wall(300, 212.5, 6, 300, False))
            self.level_walls.append(Wall(700, 212.5, 6, 200, False))
            self.level_water.append(Water(getrelativepos((500, 350)), 250, 100))

        elif self.number == 9:
            self.hole = Hole(getrelativepos((850, 50)))
            self.flag = Flag(getrelativepos((850, 50)))
            self.level_walls.append(Wall(400, 150, 6, 200, False))
            self.level_walls.append(Wall(600, 275, 6, 200, False))
            self.level_bunkers.append(Bunker(getrelativepos((500, 350)), 300, 150))
            self.level_water.append(Water(getrelativepos((700, 100)), 200, 100))

        elif self.number == 10:
            self.hole = Hole(getrelativepos((850, 300)))
            self.flag = Flag(getrelativepos((850, 300)))
            self.level_walls.append(Wall(300, 212.5, 6, 250, False))
            self.level_walls.append(Wall(600, 100, 6, 200, False))
            self.level_bunkers.append(Bunker(getrelativepos((450, 250)), 200, 100))
            self.level_water.append(Water(getrelativepos((700, 375)), 250, 125))

        elif self.number == 11:
            self.hole = Hole(getrelativepos((850, 75)))
            self.flag = Flag(getrelativepos((850, 75)))
            self.level_walls.append(Wall(500, 250, 6, 300, False))
            self.level_walls.append(Wall(250, 100, 6, 200, False))
            self.level_bunkers.append(Bunker(getrelativepos((600, 350)), 250, 100))
            self.level_water.append(Water(getrelativepos((400, 200)), 200, 100))

        elif self.number == 12:
            self.hole = Hole(getrelativepos((850, 400)))
            self.flag = Flag(getrelativepos((850, 400)))
            self.level_walls.append(Wall(300, 212.5, 6, 250, False))
            self.level_walls.append(Wall(700, 100, 6, 200, False))
            self.level_walls.append(Wall(500, 300, 6, 200, False))
            self.level_bunkers.append(Bunker(getrelativepos((400, 100)), 200, 100))
            self.level_water.append(Water(getrelativepos((600, 375)), 250, 125))

        elif self.number == 13:
            self.hole = Hole(getrelativepos((850, 50)))
            self.flag = Flag(getrelativepos((850, 50)))
            self.level_walls.append(Wall(500, 250, 6, 300, False))
            self.level_walls.append(Wall(250, 100, 6, 200, False))
            self.level_walls.append(Wall(750, 300, 6, 150, False))
            self.level_bunkers.append(Bunker(getrelativepos((600, 350)), 250, 100))
            self.level_water.append(Water(getrelativepos((400, 200)), 200, 100))

        elif self.number == 14:
            self.hole = Hole(getrelativepos((850, 250)))
            self.flag = Flag(getrelativepos((850, 250)))
            self.level_walls.append(Wall(500, 150, 6, 200, False))
            self.level_walls.append(Wall(700, 350, 6, 200, False))
            self.level_bunkers.append(Bunker(getrelativepos((350, 350)), 200, 100))
            self.level_water.append(Water(getrelativepos((600, 100)), 250, 100))

        elif self.number == 15:
            self.hole = Hole(getrelativepos((850, 75)))
            self.flag = Flag(getrelativepos((850, 75)))
            self.level_walls.append(Wall(250, 212.5, 6, 250, False))
            self.level_walls.append(Wall(600, 100, 6, 200, False))
            self.level_walls.append(Wall(700, 300, 6, 150, False))
            self.level_bunkers.append(Bunker(getrelativepos((450, 250)), 200, 100))
            self.level_water.append(Water(getrelativepos((750, 375)), 250, 125))

    def draw(self):
            for bunker in self.level_bunkers:
                bunker.draw()
            for water in self.level_water:
                water.draw()
            for wall in self.level_walls:
                wall.draw()
            for wall in border_walls:
                wall.draw()
            self.hole.draw()
            if not self.flag.rect.colliderect(ball.rect) or ball.velocity != 0:
                self.flag.draw()

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.font = pygame.font.Font("assets/font.ttf", 28)

    def increment(self):
        if self.score < 5:
            self.score += 1

    def reset(self):
        self.score = 0

    def draw(self):
        text = self.font.render(f"Shots: {self.score}", True, BLUE_EFREI)
        SCREEN.blit(text, (10, 10))

class Message(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font("assets/font.ttf", 28)
        self.fontcolor = BLUE_EFREI
        self.button_width = 150
        self.button_height = 50
        self.button_pos = (500 - self.button_width / 2, 275)
        self.button_color = WHITE
        self.button_rect = pygame.Rect(self.button_pos, (self.button_width, self.button_height))

    def draw(self, msg_type):
        if msg_type == "win":
            if score.score==1:
                msg = f"You scored a Hole-in-one! Congratulations!"
            else:
                msg = f"You won in {score.score} shots!"
            button_msg = "Next level"
        elif msg_type == "lose":
            msg = f"You didn't succeed to score in 5 shots. You lost!"
            button_msg = "Try again"
        else:
            msg = "Message not defined"
            button_msg = "OK"
        text = self.font.render(msg, True, BLACK)
        text_width, text_height = text.get_size()
        button_text = self.font.render(button_msg, True, BLACK)
        SCREEN.blit(text, (SCREEN.get_width() / 2 - text_width / 2,SCREEN.get_height() / 2 - text_height / 2))
        pygame.draw.rect(SCREEN, BLACK, self.button_rect.inflate(6, 6))
        pygame.draw.rect(SCREEN, self.button_color, self.button_rect)
        SCREEN.blit(button_text, self.button_pos)

    def clicked(self, event):
        global display_msg, level
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                if won:
                    self.button_color = GREY
                    new_level = level.number + 1
                    updatelevel(new_level)
                end_level()
                level = Level(getlevel())
                display_msg = False

        elif event.type == pygame.MOUSEBUTTONUP:
            self.button_color = WHITE
        return False

# ---------- Create Game Objects ----------
field = Field()

# Create border walls (these persist across levels)
bordertop = Wall(0, 0, 900, 6, True)
borderbottom = Wall(0, 425, 900, 6, True)
borderleft = Wall(0, 0, 6, 425, True)
borderright = Wall(900, 0, 6, 431, True)
# Store them in our dedicated list.
border_walls.extend([bordertop, borderbottom, borderleft, borderright])

ball = Ball()
slider = Slider()
launch_button = Launch()
arrow = Arrow()
score = Score()
message = Message()
level = Level(getlevel())

clock = pygame.time.Clock()
running = True

# ---------- Main Game Loop ----------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if display_msg:
            message.clicked(event)
        else:
            slider.handle_event(event)
            launch_button.clicked(event)
            if event.type == pygame.MOUSEBUTTONDOWN and ball.velocity == 0:
                if field.rect.collidepoint(event.pos):
                    arrow_follow = not arrow_follow
            if event.type == pygame.MOUSEBUTTONUP:
                launch_button.color = WHITE
                message.button_color = WHITE

    SCREEN.fill((240, 240, 240))
    SCREEN.blit(BG, (0, 0))
    field.draw()

    # Check collisions against border walls and level-specific walls.
    ball.collision(border_walls + level.level_walls,level.level_water)
    ball.unstuck()
    level.draw()
    score.draw()

    if display_msg:
        if won:
            message.draw("win")
        else:
            message.draw("lose")
    else:
        if ball.velocity > 0:
            ball.update_position(False)
        else:
            arrow.update_direction(pygame.mouse.get_pos())
            arrow.draw()
            slider.draw()
            launch_button.draw()

        if level.hole.collision_rect.colliderect(ball.rect) and ball.velocity < 10:
            won = True
            display_msg = True
        elif ball.velocity == 0 and score.score == 5:
            lose()
        else:
            ball.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
