import pyxel
import math

SIZE = 256
BLOCK_SIZE = 64


class Mandel:
    def __init__(self):
        self.r = [0.0] * SIZE * SIZE
        self.i = [0.0] * SIZE * SIZE
        self.block_index = 0
        self.block_width = math.ceil(SIZE / BLOCK_SIZE)
        self.color = 0
        pyxel.init(SIZE, SIZE)
        pyxel.run(self.update, self.draw)
        pyxel.cls(0)
        pyxel.rect(0, 0, 64, 64, 1)

    def update(self):
        x_base = (self.block_index // self.block_width) * BLOCK_SIZE
        y_base = (self.block_index % self.block_width) * BLOCK_SIZE
        for _x in range(BLOCK_SIZE):
            for _y in range(BLOCK_SIZE):
                x = x_base + _x
                y = y_base + _y
                if x >= SIZE or y >= SIZE:
                    break
                r = self.r[x * SIZE + y]
                i = self.i[x * SIZE + y]
                if r ** 2 + i ** 2 > 4:
                    continue
                cr = x * 4 / SIZE - 2
                ci = y * 4 / SIZE - 2
                nr = self.r[x * SIZE + y] = r * r - i * i + cr
                ni = self.i[x * SIZE + y] = 2 * r * i + ci
                if nr ** 2 + ni ** 2 > 4:
                    pyxel.pix(x, y, (self.color + 1) % 16)
        self.block_index += 1
        if self.block_index >= self.block_width * self.block_width:
            self.color += 1
            self.block_index -= (self.block_width * self.block_width)

    def draw(self):
        pass


Mandel()
