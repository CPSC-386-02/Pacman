import pygame as pg
from vector import Vector
import game_functions as gf


class Grid_Pnt:
    def __init__(self, settings, screen, row, column):
        self.settings = settings
        self.screen = screen
        self.row, self.column = row, column
        self.position = Vector(column * self.settings.tile_width, row * self.settings.tile_height)
        self.neighbors = {gf.direction["UP"]: None, gf.direction["DOWN"]: None,
                          gf.direction["LEFT"]: None, gf.direction["RIGHT"]: None}

    def draw(self):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pg.draw.line(self.screen, (255, 255, 255), line_start, line_end, 4)
                pg.draw.circle(self.screen, (255, 0, 0), self.position.asInt(), 12)


class Grid_Pnts_Group:
    def __init__(self, settings, screen):
        self.settings = settings
        self.screen = screen
        self.li = []

    def setupTestNodes(self):
        nodeA = Grid_Pnt(self.settings, self.screen, 5, 5)
        nodeB = Grid_Pnt(self.settings, self.screen, 5, 10)
        nodeC = Grid_Pnt(self.settings, self.screen, 10, 5)
        nodeD = Grid_Pnt(self.settings, self.screen, 10, 10)
        nodeE = Grid_Pnt(self.settings, self.screen, 10, 13)
        nodeF = Grid_Pnt(self.settings, self.screen, 20, 5)
        nodeG = Grid_Pnt(self.settings, self.screen, 20, 13)
        nodeA.neighbors[gf.direction["RIGHT"]] = nodeB
        nodeA.neighbors[gf.direction["DOWN"]] = nodeC
        nodeB.neighbors[gf.direction["LEFT"]] = nodeA
        nodeB.neighbors[gf.direction["DOWN"]] = nodeD
        nodeC.neighbors[gf.direction["UP"]] = nodeA
        nodeC.neighbors[gf.direction["RIGHT"]] = nodeD
        nodeC.neighbors[gf.direction["DOWN"]] = nodeF
        nodeD.neighbors[gf.direction["UP"]] = nodeB
        nodeD.neighbors[gf.direction["LEFT"]] = nodeC
        nodeD.neighbors[gf.direction["RIGHT"]] = nodeE
        nodeE.neighbors[gf.direction["LEFT"]] = nodeD
        nodeE.neighbors[gf.direction["DOWN"]] = nodeG
        nodeF.neighbors[gf.direction["UP"]] = nodeC
        nodeF.neighbors[gf.direction["RIGHT"]] = nodeG
        nodeG.neighbors[gf.direction["UP"]] = nodeE
        nodeG.neighbors[gf.direction["LEFT"]] = nodeF
        self.li = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG]

    def render(self, screen):
        for node in self.li:
            node.draw()
