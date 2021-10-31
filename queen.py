from os import path
import pygame as pg
from rook import Rook
from bishop import Bishop


class Queen:
    def __init__(self, game, color, pos):
        self.type = "QUEEN"
        self.cell = None
        self.color = color
        self.pos = pos
        self.game = game
        self.images = [
            path.join(self.game.img_dir, "w_queen.png"),
            path.join(self.game.img_dir, "b_queen.png"),
        ]
        if self.color == "W":
            self.image = pg.image.load(self.images[0])
        else:
            self.image = pg.image.load(self.images[1])
        self.image.set_colorkey((255,255,255))
        self.game.pieces.append(self)
        self.possible_moves = self.get_possible_moves()
    def get_possible_moves(self):
        r = Rook(self.game, self.color, self.pos)
        self.game.pieces.pop()
        b = Bishop(self.game, self.color, self.pos)
        self.game.pieces.pop()
        return r.get_possible_moves()+b.get_possible_moves()
