import pyxel

SIZE = 256


class Mandel:
    def __init__(self):
        self.r = [0.0] * SIZE * SIZE
        self.i = [0.0] * SIZE * SIZE
        pyxel.init(SIZE, SIZE)
        pyxel.run(self.update, self.draw)
        pyxel.cls(0)
        pyxel.rect(0, 0, 64, 64, 1)

    def update(self):
        for x in range(SIZE):
            for y in range(SIZE):
                r = self.r[x * SIZE + y]
                i = self.i[x * SIZE + y]
                if r ** 2 + i ** 2 > 4:
                    continue
                cr = x * 4 / SIZE - 2
                ci = y * 4 / SIZE - 2
                nr = self.r[x * SIZE + y] = r * r - i * i + cr
                ni = self.i[x * SIZE + y] = 2 * r * i + ci
                if nr ** 2 + ni ** 2 > 4:
                    pyxel.pix(x, y, (pyxel.frame_count + 1) % 16)

    def draw(self):
        pass


Mandel()
