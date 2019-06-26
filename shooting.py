import pyxel
import math
import random


class App:
    def __init__(self):
        pyxel.init(256, 256)
        pyxel.load("my_resource.pyxres")
        self.running = False
        self.characters = []
        self.beams = []
        self.enemies = []
        self.player = Player(self.characters, self.beams, self.enemies,
                             position=Vector(pyxel.width / 2, pyxel.height / 2))
        Enemy(self.characters, self.beams, self.enemies, position=Vector(pyxel.width - 20, pyxel.height / 2),
              rad=math.pi / 3)

    def run(self):
        self.running = True
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.running:
            if pyxel.frame_count % 60 == 0:
                radius = random.uniform(pyxel.width, pyxel.width * 1.5)
                radian = random.uniform(0, 2 * math.pi)
                Enemy(self.characters, self.beams, self.enemies,
                      Vector(radius * math.cos(radian) + pyxel.width / 2, radius * math.sin(radian) + pyxel.height / 2),
                      random.uniform(math.pi / 6, math.pi / 2) * (random.uniform(-1, 1) < 0 if 1 else -1))
            for c in self.characters:
                c.update()

    def draw(self):
        if self.running:
            pyxel.cls(0)
            for c in self.characters:
                c.draw()


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def squared_length(self):
        return self.x ** 2 + self.y ** 2

    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float):
        return Vector(self.x * other, self.y * other)

    def __neg__(self):
        return Vector(-self.x, -self.y)


class Rectangle:
    def __init__(self, position, size):
        self.position = position
        self.size = size


class Character:
    def __init__(self, characters: [], image_rect: Rectangle, position: Vector = Vector(0, 0),
                 speed: Vector = Vector(0, 0), friction_ratio=0.25):
        self.characters = characters
        self.image_rect = image_rect
        self.position = position
        self.speed = speed
        self.friction_ratio = friction_ratio
        self.characters.append(self)

    def __del__(self):
        if self in self.characters:
            self.characters.remove(self)

    def update(self):
        friction = -self.speed
        f_len = friction.length()
        if f_len > 1:
            friction *= 1 / f_len
        friction *= f_len * self.friction_ratio
        self.speed += friction
        self.position += self.speed

    def draw(self):
        pyxel.blt(self.position.x - self.image_rect.size.x / 2,
                  self.position.y - self.image_rect.size.y / 2,
                  0,
                  self.image_rect.position.x,
                  self.image_rect.position.y,
                  self.image_rect.size.x,
                  self.image_rect.size.y,
                  0)


class Player(Character):
    def __init__(self, characters: [], beams: [], enemies: [], position: Vector = Vector(0, 0)):
        super().__init__(characters, image_rect=Rectangle(Vector(0, 0), Vector(16, 16)), position=position)
        self.lr = 0
        self.beams = beams
        self.enemies = enemies

    def update(self):
        pow_vec = Vector(pyxel.btn(pyxel.KEY_RIGHT) - pyxel.btn(pyxel.KEY_LEFT),
                         pyxel.btn(pyxel.KEY_DOWN) - pyxel.btn(pyxel.KEY_UP))
        s_len = pow_vec.squared_length()
        if s_len != 0:
            pow_vec *= 1 / math.sqrt(s_len)
        self.speed += pow_vec * 2

        if pyxel.btnp(pyxel.KEY_SPACE, 0, 5):

            if self.lr == 1:
                Beam(self.characters, self.beams, self.position + Vector(8, 5))
                self.lr = 0
            else:
                Beam(self.characters, self.beams, self.position + Vector(8, -5))
                self.lr = 1

        super().update()
        if self.position.x < self.image_rect.size.x / 2:
            self.position.x = self.image_rect.size.x / 2
        if self.position.y < self.image_rect.size.y / 2:
            self.position.y = self.image_rect.size.y / 2
        if self.position.x > pyxel.width - self.image_rect.size.x / 2:
            self.position.x = pyxel.width - self.image_rect.size.x
        if self.position.y > pyxel.height - self.image_rect.size.y / 2:
            self.position.y = pyxel.height - self.image_rect.size.y

        pos = self.position
        radius = max(self.image_rect.size.x, self.image_rect.size.y) / 2
        for enemy in self.enemies:
            enemy_pos = enemy.position
            enemy_radius = max(enemy.image_rect.size.x, enemy.image_rect.size.y) / 2
            if (enemy_pos - pos).length() < radius + enemy_radius:
                self.__del__()
                app.running = False
                break


class Beam(Character):
    def __init__(self, characters: [], beams: [], position: Vector):
        super().__init__(characters, Rectangle(Vector(0, 16), Vector(8, 2)), position, speed=Vector(0, 0),
                         friction_ratio=0)
        beams.append(self)
        self.beams = beams

    def update(self):
        self.speed.x += 1
        super().update()
        if self.position.x > pyxel.width + self.image_rect.size.x / 2:
            self.__del__()

    def __del__(self):
        if self in self.beams:
            self.beams.remove(self)
        super().__del__()


class Enemy(Character):
    def __init__(self, characters: [], beams: [], enemies: [], position: Vector, rad: float):
        super().__init__(characters, image_rect=Rectangle(Vector(16, 0), Vector(16, 16)), position=position)
        enemies.append(self)
        self.enemies = enemies
        self.beams = beams
        self.rad = rad
        cos = math.cos(rad)
        sin = math.sin(rad)
        self.rotate = [cos, -sin, sin, cos]

    def __del__(self):
        if self in self.enemies:
            self.enemies.remove(self)
        super().__del__()

    def update(self):
        pos = self.position
        direct = app.player.position - pos
        direct = direct * (1 / direct.length()) * 3
        self.speed = Vector(direct.x * self.rotate[0] + direct.y * self.rotate[1],
                            direct.x * self.rotate[2] + direct.y * self.rotate[3])
        super().update()
        radius = max(self.image_rect.size.x, self.image_rect.size.y) / 2
        for beam in self.beams:
            beam_rect = Rectangle(beam.position - beam.image_rect.size * 0.5, beam.image_rect.size)
            beam_corners = [beam_rect.position - pos,
                            beam_rect.position + Vector(beam_rect.size.x, 0) - pos,
                            beam_rect.position + Vector(0, beam_rect.size.y) - pos,
                            beam_rect.position + beam_rect.size - pos]
            for i in range(4):
                for j in range(i + 1, 4):
                    a = beam_corners[i].x
                    b = beam_corners[i].y
                    c = beam_corners[j].x
                    d = beam_corners[j].y
                    x = (a * d ** 2 + ((-b * c) - a * b) * d + b ** 2 * c) / \
                        (d ** 2 - 2 * b * d + c ** 2 - 2 * a * c + b ** 2 + a ** 2)
                    y = -((a * c - a ** 2) * d - b * c ** 2 + a * b * c) / \
                        (d ** 2 - 2 * b * d + c ** 2 - 2 * a * c + b ** 2 + a ** 2)
                    if math.sqrt(x ** 2 + y ** 2) < radius and (a * y - x * b) * (x * d - c * y) >= 0:
                        self.__del__()
                        return


app = App()
app.run()
