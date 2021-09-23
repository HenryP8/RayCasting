import pygame
import math

game_map = [[1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1]]

WIDTH, HEIGHT = 1000, 400
SQUARE_SIZE = 50

turn_speed = 0.01
move_speed = 0.5

black = (0, 0, 0)
white = (255, 255, 255)
gray = (200, 200, 200)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
light_green = (50, 200, 80)
dark_green = (30, 160, 60)


def draw_map():
    for i in range(len(game_map)):
        for j in range(len(game_map[0])):
            if game_map[j][i] == 1:
                pygame.draw.rect(screen, black, (i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE - 1, SQUARE_SIZE - 1))
            else:
                pygame.draw.rect(screen, white, (i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE - 1, SQUARE_SIZE - 1))


class HorizontalArray:

    global game_map, turn_speed, move_speed

    def __init__(self, x, y, angle):
        self.angle = angle * math.pi/180
        self.x = x
        self.y = y
        self.speed = move_speed
        self.end_x = 0
        self.end_y = 0
        self.offset = SQUARE_SIZE

    def find_first_hor(self):
        if 0 < self.angle/(2*math.pi) < 1/2:
            self.end_y = 50 * math.floor(self.y / SQUARE_SIZE)
            self.end_x = ((self.y - self.end_y) / math.tan(self.angle)) + self.x
            self.offset = SQUARE_SIZE
        if 1/2 < self.angle/(2*math.pi) < 1:
            self.end_y = 50 * math.ceil(self.y / SQUARE_SIZE)
            self.end_x = ((self.y - self.end_y) / math.tan(self.angle)) + self.x
            self.offset = -SQUARE_SIZE
        #if abs(self.angle/(2*math.pi)) < 0.001 or abs(self.angle/(2*math.pi) - 1/2) < 0.001 or abs(self.angle/(2*math.pi) - 1) < 0.001:
            #self.end_y = self.y
            #self.end_x = 0

    def extend_ray(self):
        search_depth = 0
        while search_depth < 8:
            map_x = math.ceil(self.end_x / SQUARE_SIZE)
            map_y = math.ceil(self.end_y / SQUARE_SIZE)
            if 0 <= map_x <= len(game_map) and 0 <= map_y < len(game_map[0]) and \
                    (game_map[int(map_y) - 1][int(map_x) - 1] == 1 or game_map[int(map_y)][int(map_x) - 1] == 1):
                search_depth = 8
            else:
                self.end_y -= self.offset
                if math.tan(self.angle) != 0:
                    self.end_x = ((self.y - self.end_y) / math.tan(self.angle)) + self.x
                search_depth += 1

    def calc_ray(self):
        self.correct_angle()
        self.find_first_hor()
        self.extend_ray()

    def draw_ray(self):
        self.calc_ray()
        pygame.draw.circle(screen, blue, (int(self.x), int(self.y)), 5)
        pygame.draw.line(screen, green, (int(self.x), int(self.y)), (int(self.end_x), int(self.end_y)), 3)

    def get_distance(self):
        return math.sqrt((self.end_x - self.x) ** 2 + (self.end_y - self.y) ** 2)

    def correct_angle(self):
        if self.angle > 2 * math.pi:
            self.angle = 0
        if self.angle < 0:
            self.angle = 2 * math.pi

    def move_up(self):
        self.y -= self.speed

    def move_down(self):
        self.y += self.speed

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def turn_left(self):
        self.angle += turn_speed

    def turn_right(self):
        self.angle -= turn_speed


class VerticalArray:

    global game_map, turn_speed, move_speed

    def __init__(self, x, y, angle):
        self.angle = angle * math.pi/180
        self.x = x
        self.y = y
        self.speed = move_speed
        self.end_x = 0
        self.end_y = 0
        self.offset = SQUARE_SIZE

    def find_first_vert(self):
        if self.angle/(2*math.pi) < 1/4 or self.angle/(2*math.pi) > 3/4:
            self.end_x = 50 * math.ceil(self.x / SQUARE_SIZE)
            self.end_y = ((self.x - self.end_x) * math.tan(self.angle)) + self.y
            self.offset = SQUARE_SIZE
        if 1/4 < self.angle/(2*math.pi) < 3/4:
            self.end_x = 50 * math.floor(self.x / SQUARE_SIZE)
            self.end_y = ((self.x - self.end_x) * math.tan(self.angle)) + self.y
            self.offset = -SQUARE_SIZE
        #if abs(self.angle/(2*math.pi)) < 0.001 or abs(self.angle/(2*math.pi) - 1/2) < 0.001 or abs(self.angle/(2*math.pi) - 1) < 0.001:
            #self.end_y = self.y
            #self.end_x = 0

    def extend_ray(self):
        search_depth = 0
        while search_depth < 8:
            map_x = math.ceil(self.end_x / SQUARE_SIZE)
            map_y = math.ceil(self.end_y / SQUARE_SIZE)
            if 0 <= map_x < len(game_map) and 0 <= map_y <= len(game_map[0]) and \
                    (game_map[int(map_y) - 1][int(map_x) - 1] == 1 or game_map[int(map_y) - 1][int(map_x)] == 1):
                search_depth = 8
            else:
                self.end_x += self.offset
                self.end_y = ((self.x - self.end_x) * math.tan(self.angle)) + self.y
                search_depth += 1

    def calc_ray(self):
        self.correct_angle()
        self.find_first_vert()
        self.extend_ray()

    def draw_ray(self):
        self.calc_ray()
        pygame.draw.circle(screen, blue, (int(self.x), int(self.y)), 5)
        pygame.draw.line(screen, red, (int(self.x), int(self.y)), (int(self.end_x), int(self.end_y)))

    def get_distance(self):
        return math.sqrt((self.end_x - self.x) ** 2 + (self.end_y - self.y) ** 2)

    def correct_angle(self):
        if self.angle > 2 * math.pi:
            self.angle = 0
        if self.angle < 0:
            self.angle = 2 * math.pi

    def move_up(self):
        self.y -= self.speed

    def move_down(self):
        self.y += self.speed

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def turn_left(self):
        self.angle += turn_speed

    def turn_right(self):
        self.angle -= turn_speed


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = False


rays = []


def create_ray(a):
    global rays
    h = HorizontalArray(150, 250, a)
    v = VerticalArray(150, 250, a)
    rays.append([h, v])


def move_arrays(dir):
    global rays
    for ray in rays:
        if dir == "up":
            ray[0].move_up()
            ray[1].move_up()
        if dir == "down":
            ray[0].move_down()
            ray[1].move_down()
        if dir == "left":
            ray[0].move_left()
            ray[1].move_left()
        if dir == "right":
            ray[0].move_right()
            ray[1].move_right()
        if dir == "turn left":
            ray[0].turn_left()
            ray[1].turn_left()
        if dir == "turn right":
            ray[0].turn_right()
            ray[1].turn_right()


for i in range(60):
    create_ray(i)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        move_arrays("up")
    if keys[pygame.K_s]:
        move_arrays("down")
    if keys[pygame.K_a]:
        move_arrays("left")
    if keys[pygame.K_d]:
        move_arrays("right")
    if keys[pygame.K_q]:
        move_arrays("turn left")
    if keys[pygame.K_e]:
        move_arrays("turn right")

    screen.fill(gray)
    draw_map()

    for ray in rays:
        ray[0].calc_ray()
        ray[1].calc_ray()
        if ray[0].get_distance() > ray[1].get_distance():
            ray[1].draw_ray()
            distance = ray[1].get_distance()
            side = "vert"
        else:
            ray[0].draw_ray()
            distance = ray[0].get_distance()
            side = "hor"
        if distance != 0:
            height = 20000/distance
            if side == "vert":
                pygame.draw.rect(screen, light_green, (990 - (10 * rays.index(ray)), (400 - height) / 2, 10, height))
            elif side == "hor":
                pygame.draw.rect(screen, dark_green, (990 - (10 * rays.index(ray)), (400 - height) / 2, 10, height))

    pygame.display.flip()
