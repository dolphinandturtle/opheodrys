import math
import pygame as pg
from dataclasses import dataclass
from typing import Callable


class Physical:

    def __init__(self, state: list[float], smoothness: int):
        self.__variations = [[x] + [0.0] * smoothness for x in state]

    def __str__(self):
        return str(self.__variations)

    @property
    def value(self):
        return [x[0] for x in self.__variations]

    """
    @value.setter
    def value(self, value: float):
        past, self.__variations[0] = self.__variations[0], value
        for i in range(1, len(self.__variations)):
            past, self.__variations[i] = self.__variations[i], past
            self.__variations[i] = self.__variations[i-1] - self.__variations[i]
    """

    def push(self, function: Callable[float, float]):
        function(self.__variations)
        for i in range(len(self.__variations)):
            for j in range(1, len(self.__variations[i])):
                self.__variations[i][j-1] += self.__variations[i][j]

def osc(v):
    ox = (v[0][0] - 700)
    oy = (v[1][0] - 360)
    d = (ox**2 + oy**2)**1.5
    v[0][2] = -16 / d * ox
    v[1][2] = -16 / d * oy


r = Physical([300.0, 300.0], 2)
r.__dict__["_Physical__variations"][1][1] = 0.1

WS = WW, WH = 1280, 720
pg.init()
screen = pg.display.set_mode(WS)
while True:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            exit()
    screen.fill("#222229")
    pg.draw.circle(screen, "#ffffff", r.value, 3)
    r.push(osc)
    pg.display.update()
