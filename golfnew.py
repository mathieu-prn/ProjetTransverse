import pygame, math
from utility import *
import config

IMAGE_CACHE = {}
SCREEN = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
BG = pygame.image.load(config.BG) # Background

# Colors
COLORS   = {
"BLACK":config.BLACK,
"WHITE":config.WHITE,
"BLUE_EFREI":config.BLUE_EFREI,
"GREY":config.GREY,
"GREEN":(148, 186, 134),
"BUNKER_YELLOW":(237, 225, 141),
"WATER_BLUE":(0, 167, 250),
}

display_msg = False   # When True, a win/lose message is shown
won = False
arrow_follow = True   # Controls whether the arrow follows the mouse

def load_image(path):
    if path not in IMAGE_CACHE:
        IMAGE_CACHE[path] = pygame.image.load(path).convert_alpha()
    return IMAGE_CACHE[path]

# Level Handling Functions
def getlevel():
    """Read and return the level number from the save file."""
    filename = "saves/golflevel.json"
    dico = loadfile(filename)
    level_value = dico.get("level", 1)
    print("Returned level:", level_value)
    return level_value

def updatelevel(levelnumber,soundeffect_save):
    """Update the level number in the save file."""
    filename = "saves/golflevel.json"
    dico = loadfile(filename)
    dico["level"] = levelnumber
    with open(filename, "w") as file:
        json.dump(dico, file)
    soundeffect_save.play()
    print("Updated level",levelnumber)

def updatescore(levelnumber,score):
    """Update the score of the current level."""
    filename = "saves/golflevel.json"
    dico = loadfile(filename)
    dico[str(levelnumber)] = score
    with open(filename, "w") as file:
        json.dump(dico, file)

def end_level(ball,score):
    """Reset game state for a new level."""
    global arrow_follow, static_background
    ball.velocity = 0
    score.reset()
    ball.rect.center = getrelativepos((25, 212.5))
    arrow_follow = True

def lose(message,ball,score):
    """Handle a losing condition."""
    global display_msg, won
    display_msg = True
    won = False
    message.draw("lose")
    end_level(ball,score)

def reflect_velocity(vx, vy, x1, y1, x2, y2):
    # Wall vector
    wall_dx = x2 - x1
    wall_dy = y2 - y1
    wall_length = math.hypot(wall_dx, wall_dy)
    wall_dx /= wall_length
    wall_dy /= wall_length

    # Normal vector (perpendicular)
    normal_x = -wall_dy
    normal_y = wall_dx

    # Dot product of velocity and normal
    dot = vx * normal_x + vy * normal_y

    # Reflect velocity across the normal
    rvx = vx - 2 * dot * normal_x
    rvy = vy - 2 * dot * normal_y

    return rvx, rvy

def point_line_distance(px, py, x1, y1, x2, y2):
    # Closest point on line segment to (px, py)
    A = px - x1
    B = py - y1
    C = x2 - x1
    D = y2 - y1

    dot = A * C + B * D
    len_sq = C * C + D * D
    param = dot / len_sq if len_sq != 0 else -1

    if param < 0:
        xx, yy = x1, y1
    elif param > 1:
        xx, yy = x2, y2
    else:
        xx = x1 + param * C
        yy = y1 + param * D

    dx = px - xx
    dy = py - yy
    return math.hypot(dx, dy), (xx, yy)


# Render Static Background
def render_static_background(level,field):
    static_bg = pygame.Surface((config.WIDTH, config.HEIGHT))
    static_bg.fill((240, 240, 240))
    static_bg.blit(BG, (0, 0))
    field.draw(static_bg)
    for bunker in level.level_bunkers:
        bunker.draw(static_bg)
    for water in level.level_water:
        water.draw(static_bg)
    for wall in level.all_walls:
        wall.draw(static_bg)
    for dwall in level.level_dwalls:
        dwall.draw(static_bg)
    level.hole.draw(static_bg)
    return static_bg

# Game Object Classes
class DiagonalWall:
    def __init__(self, start_pos, end_pos):
        self.start = getrelativepos(start_pos)
        self.end = getrelativepos(end_pos)
        self.color = COLORS["BLUE_EFREI"]
        self.width = 7  # visual width for drawing

    def draw(self, surface=SCREEN):
        pygame.draw.line(surface, self.color, self.start, self.end, self.width)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(load_image("assets/Golf/GolfBall.png"), (15, 15))
        self.rect = self.image.get_rect()
        self.rect.center = getrelativepos((25, 212.5))
        self.velocity = 0
        self.angle = 0

    def draw(self, surface=SCREEN):
        surface.blit(self.image, self.rect)

    def collision(self, walls_list, water_list, dwalls_list,soundeffect_water,soundeffect_collisions):
        # Check collision with water first.
        for water in water_list:
            if self.rect.colliderect(water.rect):
                soundeffect_water.play()
                self.velocity = 0
                self.rect.center = getrelativepos((25, 212.5))
        # Then check collision with walls.
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
                soundeffect_collisions.play()
                return True
        for wall in dwalls_list:
            dist, closest_point = point_line_distance(self.rect.centerx, self.rect.centery,*wall.start, *wall.end)
            if dist < 10:
                vx = self.velocity * math.cos(self.angle)
                vy = self.velocity * math.sin(self.angle)

                rvx, rvy = reflect_velocity(vx, vy, *wall.start, *wall.end)

                self.angle = math.atan2(rvy, rvx)
                self.rect.centerx += rvx * 0.5
                self.rect.centery += rvy * 0.5
                self.velocity *= 0.9
                soundeffect_collisions.play()
                return True

        return False

    def unstuck(self,field):
        if self.rect.left < field.rect.left:
            self.rect.center = (self.rect.center[0] + 4, self.rect.center[1])
        elif self.rect.right > field.rect.right:
            self.rect.center = (self.rect.center[0] - 4, self.rect.center[1])
        elif self.rect.top < field.rect.top:
            self.rect.center = (self.rect.center[0], self.rect.center[1] + 4)
        elif self.rect.bottom > field.rect.bottom:
            self.rect.center = (self.rect.center[0], self.rect.center[1] - 4)

    def update_position(self, launched,slider,arrow,level):
        if launched:
            self.velocity = slider.get_value() * 0.2
            self.angle = arrow.angle
        acceleration = -0.1
        # Check if ball is in a bunker for extra deceleration.
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

    def draw(self, surface=SCREEN):
        pygame.draw.rect(surface, COLORS["BLUE_EFREI"], self.rect.inflate(6, 6))
        pygame.draw.rect(surface, COLORS["WHITE"], self.rect)
        pygame.draw.rect(surface, COLORS["BLACK"], self.slider_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider_rect.collidepoint(event.pos):
                self.dragging = True
            elif self.rect.collidepoint(event.pos):
                self.slider_rect.y = max(self.rect.top, min(event.pos[1], self.rect.bottom - self.slider_rect.height))
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.slider_rect.y = max(self.rect.top, min(event.pos[1], self.rect.bottom - self.slider_rect.height))

    def get_value(self):
        min_y = self.rect.top
        max_y = self.rect.bottom - self.slider_rect.height
        return int(100 - (((self.slider_rect.y - min_y) / (max_y - min_y)) * 100)) + int(10 * ((self.slider_rect.y - min_y) / (max_y - min_y)))

class Launch(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(17, 396, 50, 80)
        self.color = COLORS["WHITE"]

    def draw(self, surface=SCREEN):
        pygame.draw.rect(surface, COLORS["BLUE_EFREI"], self.rect.inflate(6, 6))
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 45)
        text = font.render("Go!", True, COLORS["BLUE_EFREI"])
        surface.blit(text, (self.rect.x, self.rect.y + 30))

    def clicked(self, event,ball,score,soundeffect_swing,slider,arrow,level):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and ball.velocity == 0:
                score.increment()
                self.color = COLORS["GREY"]
                soundeffect_swing.play()
                ball.update_position(True,slider,arrow,level)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.color = COLORS["WHITE"]

class Field(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(80, 55, 900, 425)

    def draw(self, surface=SCREEN):
        pygame.draw.rect(surface, COLORS["GREEN"], self.rect)

class Wall(pygame.sprite.Sprite):
    def __init__(self, relative_x, relative_y, width, height, is_border):
        super().__init__()
        self.color = COLORS["BLUE_EFREI"]
        if is_border:
            self.rect = pygame.Rect(relative_x + 80, relative_y + 55, width, height)
        else:
            self.rect = pygame.Rect(relative_x + 80 - width / 2, relative_y + 55 - height / 2, width, height)

    def draw(self, surface=SCREEN):
        pygame.draw.rect(surface, self.color, self.rect)

class Bunker(pygame.sprite.Sprite):
    def __init__(self, pos, width, height):
        super().__init__()
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = pos

    def draw(self, surface=SCREEN):
        pygame.draw.rect(surface, COLORS["BUNKER_YELLOW"], self.rect)

class Water(pygame.sprite.Sprite):
    def __init__(self, pos, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = pos

    def draw(self, surface=SCREEN):
        pygame.draw.rect(surface, COLORS["WATER_BLUE"], self.rect)

class Arrow(pygame.sprite.Sprite):
    def __init__(self, length=50):
        super().__init__()
        self.length = length
        self.direction = pygame.Vector2(1, 0)
        self.angle = 0

    def draw(self, ball,slider,surface=SCREEN):
        arrow_end = pygame.Vector2(ball.rect.center) + self.direction * (20 + slider.get_value())
        pygame.draw.line(surface, COLORS["BLUE_EFREI"], ball.rect.center, arrow_end, 3)
        self.angle = math.atan2(self.direction.y, self.direction.x)
        arrow_angle = math.atan2(-self.direction.y, -self.direction.x)
        arrow_size = 10
        left = (arrow_end.x + arrow_size * math.cos(arrow_angle + math.pi / 6),
                arrow_end.y + arrow_size * math.sin(arrow_angle + math.pi / 6))
        right = (arrow_end.x + arrow_size * math.cos(arrow_angle - math.pi / 6),
                 arrow_end.y + arrow_size * math.sin(arrow_angle - math.pi / 6))
        pygame.draw.polygon(surface, COLORS["BLUE_EFREI"], [arrow_end, left, right])

    def update_direction(self, mouse_pos,ball):
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
    def draw(self, surface=SCREEN):
        surface.blit(self.image, self.pos)

class Hole(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image("assets/Golf/Hole.png")
        self.rect = self.image.get_rect(center=pos)
        self.collision_rect = pygame.Rect(0, 0, 14, 14)
        self.collision_rect.center = self.rect.center

    def draw(self, surface=SCREEN):
        pygame.draw.circle(surface, COLORS["WHITE"], self.rect.center, 7)
        surface.blit(self.image, self.rect)

class Level(pygame.sprite.Sprite):
    def __init__(self, number,border_walls):
        super().__init__()
        self.number = number
        self.level_walls = []    # Level-specific walls
        self.level_bunkers = []  # Level-specific bunkers
        self.level_water = []  # Level-specific water elements
        self.level_dwalls= []
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
            self.level_bunkers.append(Bunker(getrelativepos((250,275)), 100, 300))
            self.level_bunkers.append(Bunker(getrelativepos((650,150)), 100, 300))
            self.level_bunkers.append(Bunker(getrelativepos((250,37.5)), 100, 75))
            self.level_bunkers.append(Bunker(getrelativepos((650,386.5)), 100, 75))

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
            self.level_bunkers.append(Bunker(getrelativepos((600,325)), 250, 100))

        elif self.number == 11:
            self.hole = Hole(getrelativepos((850,375)))
            self.flag = Flag(getrelativepos((850,375)))
            self.level_walls.append(Wall(200, 75/2, 6, 75, False))
            self.level_walls.append(Wall(200, 425 - 275/2, 6, 275, False))
            self.level_walls.append(Wall(450, 175/2, 6, 175, False))
            self.level_walls.append(Wall(450, 425-175/2, 6, 175, False))
            self.level_walls.append(Wall(700, 275/2, 6, 275, False))
            self.level_walls.append(Wall(700, 425-75/2, 6, 75, False))

        elif self.number == 12:
            self.hole = Hole(getrelativepos((850, 212.5)))
            self.flag = Flag(getrelativepos((850, 212.5)))
            self.level_water.append(Water(getrelativepos((450,212)), 450, 212))

        elif self.number == 13:
            self.level_bunkers.append(Bunker(getrelativepos((300,125)), 200, 100))
            self.level_bunkers.append(Bunker(getrelativepos((300, 300)), 200, 100))
            self.level_water.append(Water(getrelativepos((600,212)), 200, 100))

        elif self.number == 14:
            self.level_walls.append(Wall(200, 212.5, 6, 300, False))
            self.level_water.append(Water(getrelativepos((500, 75)), 250, 150))
            self.level_water.append(Water(getrelativepos((500, 350)), 250, 150))

        elif self.number == 15:
            self.level_walls.append(Wall(200, 150, 6, 300, False))
            self.level_dwalls.append(DiagonalWall((350, 425), (375, 375)))
            self.level_walls.append(Wall(375, 302, 6, 150, False))
            self.level_water.append(Water(getrelativepos((250, 75)), 100, 150))
            self.level_dwalls.append(DiagonalWall((375, 227), (400, 177)))
            self.level_dwalls.append(DiagonalWall((375, 2), (475, 200)))
            self.level_walls.append(Wall(650, 212, 6, 150, False))
            self.level_bunkers.append(Bunker(getrelativepos((600,375)), 200, 100))
        elif self.number == 16:
            self.level_walls.append(Wall(150,125,6,250,False))
            self.level_dwalls.append(DiagonalWall((150, 425), (250, 335)))
            self.level_walls.append(Wall(250, 264, 6, 325, False))
            self.level_dwalls.append(DiagonalWall((300, 0), (400, 100)))
            self.level_walls.append(Wall(350, 300, 6, 250, False))
        # Combine border walls with level-specific walls
        self.all_walls = border_walls + self.level_walls

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.shots=0
        self.font = pygame.font.Font("assets/Common/font.ttf", 28)

    def increment(self):
        if self.shots < 5:
            self.shots += 1
        self.score=6-self.shots
    def reset(self):
        self.shots = 0
        self.score = 0

    def draw(self, surface=SCREEN):
        text = self.font.render(f"Shots: {self.shots}", True, COLORS["BLUE_EFREI"])
        surface.blit(text, (10, 10))

class Message(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font("assets/Common/font.ttf", 28)
        self.fontcolor = COLORS["BLUE_EFREI"]
        self.button_width = 150
        self.button_height = 50
        self.button_pos = (500 - self.button_width / 2, 275)
        self.button_color = COLORS["WHITE"]
        self.button_rect = pygame.Rect(self.button_pos, (self.button_width, self.button_height))

    def draw(self, msg_type, score,surface=SCREEN):
        if msg_type == "win":
            if score.shots == 1:
                msg = f"You scored a Hole-in-one! Congratulations! You scored {score.score}/5 points."
            else:
                msg = f"You won in {score.shots} shots! You scored {score.score}/5 points."
            button_msg = "Next level"
        elif msg_type == "lose":
            msg = "You didn't succeed to score in 5 shots. You lost!"
            button_msg = "Try again"
        else:
            msg = "Message not defined"
            button_msg = "OK"

        #Draw
        text = self.font.render(msg, True, COLORS["BLACK"])
        text_width, text_height = text.get_size()
        surface.blit(text, (surface.get_width() / 2 - text_width / 2, surface.get_height() / 2 - text_height / 2))
        pygame.draw.rect(surface, COLORS["BLACK"], self.button_rect.inflate(6, 6))
        pygame.draw.rect(surface, self.button_color, self.button_rect)

        button_text = self.font.render(button_msg, True, COLORS["BLACK"])

        #Below is to center the text in the button
        tbutton_width, tbutton_height = button_text.get_size()
        tbuttonx=self.button_pos[0]+((self.button_width-tbutton_width)/2)
        tbuttony=self.button_pos[1]+((self.button_height-tbutton_height)/2)
        surface.blit(button_text,(tbuttonx, tbuttony)) #Draw the text

    def clicked(self, event,soundeffect_clicked,score,soundeffect_save,ball,border_walls,field,level):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                soundeffect_clicked.play()
                if won:
                    self.button_color = COLORS["GREY"]
                    updatescore(level.number,score.score)
                    new_level = level.number + 1
                    print(new_level)
                    if new_level%5==0: # Save every 5 levels
                        updatelevel(new_level,soundeffect_save)
                    level.number = new_level
                    end_level(ball,score)
                    level = Level(level.number,border_walls)
                else:
                    end_level(ball,score)
                    level.number=getlevel()
                    level = Level(level.number,border_walls)
                static_background = render_static_background(level,field)
                return display_msg = False
        elif event.type == pygame.MOUSEBUTTONUP:
            self.button_color = COLORS["WHITE"]

class Resetbutton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font("assets/Common/font.ttf", 24)
        self.fontcolor = COLORS["BLUE_EFREI"]
        self.text = self.font.render("Go back to checkpoint", True, self.fontcolor)
        self.width, self.height = self.text.get_size()
        self.pos = (1000 - 100 - self.width, 10)
        self.color = COLORS["WHITE"]
        self.rect = pygame.Rect(self.pos, (self.width, self.height))
        self.screen=SCREEN

    def draw(self):
        pygame.draw.rect(SCREEN, self.fontcolor, self.rect.inflate(6, 6))
        pygame.draw.rect(SCREEN, self.color, self.rect)
        SCREEN.blit(self.text, self.pos)

    def clicked(self, event,soundeffect_clicked,ball,score,border_walls,field):
        global level, static_background
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                soundeffect_clicked.play()
                self.color = COLORS["GREY"]
                end_level(ball,score)
                level = Level(getlevel(),border_walls)
                static_background = render_static_background(level,field)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.color = COLORS["WHITE"]

def run():
    global display_msg, won, arrow_follow
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("EfreiSport - Golf")

    # list of borders
    border_walls = []

    # Create Game Objects
    field = Field()

    # Create border walls (they don't change between levels)
    bordertop = Wall(0, 0, 900, 6, True)
    borderbottom = Wall(0, 425, 900, 6, True)
    borderleft = Wall(0, 0, 6, 425, True)
    borderright = Wall(900, 0, 6, 431, True)
    border_walls.extend([bordertop, borderbottom, borderleft, borderright])

    ball = Ball()
    slider = Slider()
    launch_button = Launch()
    arrow = Arrow()
    score = Score()
    message = Message()
    level = Level(getlevel(),border_walls)
    static_background = render_static_background(level,field)
    resetbutton = Resetbutton()



    #Define sound effects
    soundeffect_hole=pygame.mixer.Sound("assets/Golf/Sounds/hole.mp3")
    soundeffect_swing=pygame.mixer.Sound("assets/Golf/Sounds/swing.mp3")
    soundeffect_collisions=pygame.mixer.Sound("assets/Golf/Sounds/collisions.mp3")
    soundeffect_water=pygame.mixer.Sound("assets/Golf/Sounds/water.mp3")
    soundeffect_save=pygame.mixer.Sound("assets/Golf/Sounds/save.mp3")
    soundeffect_clicked=pygame.mixer.Sound("assets/Common/Sounds/clicked.mp3")

    clock = pygame.time.Clock()
    running = True

    # Main Game Loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if display_msg:
                message.clicked(event,soundeffect_clicked,score,soundeffect_save,ball,border_walls,field)
            else:
                slider.handle_event(event)
                launch_button.clicked(event,ball,score,soundeffect_swing,slider,arrow,level)
                resetbutton.clicked(event,soundeffect_clicked,ball,score,border_walls,field)
                if event.type == pygame.MOUSEBUTTONDOWN and ball.velocity == 0:
                    if arrow_follow:
                        arrow_follow = False
                    else:
                        if field.rect.collidepoint(event.pos):
                            arrow_follow = True
                if event.type == pygame.MOUSEBUTTONUP:
                    launch_button.color = COLORS["WHITE"]
                    message.button_color = COLORS["WHITE"]
                    resetbutton.color = COLORS["WHITE"]

        # Blit the static background
        SCREEN.blit(static_background, (0, 0))
        score.draw()
        if not level.flag.rect.colliderect(ball.rect) or ball.velocity != 0:
            level.flag.draw(SCREEN)

        if display_msg:
            if won:
                message.draw("win",score)
            else:
                message.draw("lose",score)
        else:
            if ball.velocity > 0:
                ball.collision(level.all_walls, level.level_water,level.level_dwalls,soundeffect_water,soundeffect_collisions)
                ball.unstuck(field)
                ball.update_position(False,slider,arrow,level)
            else:
                arrow.update_direction(pygame.mouse.get_pos(),ball)
                arrow.draw(ball,slider)
                slider.draw()
                launch_button.draw()
                resetbutton.draw()

            if level.hole.collision_rect.colliderect(ball.rect) and ball.velocity < 10:
                soundeffect_hole.play()
                won = True
                display_msg = True
            elif ball.velocity == 0 and score.shots == 5:
                lose(message,ball,score)
            else:
                ball.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
