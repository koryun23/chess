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
    def is_pinned(self):
        coords=[]
        for p in self.game.pieces:
            if p.color!=self.color:

                if p.type!='KNIGHT' and p.type!="KING" and p.type!="PAWN":
                    if self.pos in p.get_possible_moves():
                        b_coords = p.coords_to_king()
                        for bc in b_coords:
                            coords.append(bc)
        for coord in coords:
            piece = self.game.piece_on_coord(coord)
            if piece:
                if self.type==piece.type and self.pos==piece.pos and self.color==piece.color:
                    return True
        return False
    def coords_to_king(self):
        r = Rook(self.game, self.color, self.pos)
        self.game.pieces.pop()
        b = Bishop(self.game, self.color, self.pos)
        self.game.pieces.pop()
        return r.coords_to_king()+b.coords_to_king()
    def is_protected(self):
        self.game.pieces.remove(self)
        for p in self.game.pieces:
            if p.color==self.color:
                p.get_possible_moves()

                if (p.type!="PAWN" and self.pos in p.get_possible_moves()) or (p.type=="PAWN" and self.pos in p.attacked_cells):
                    self.game.pieces.append(self)
                    return True
        self.game.pieces.append(self)
        return False
        