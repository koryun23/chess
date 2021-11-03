from os import path
import pygame as pg

class Knight:
    def __init__(self, game, color, pos):
        self.type = "KNIGHT"
        self.cell = None

        self.color = color
        self.pos = pos
        self.game = game
        self.images = [
            path.join(self.game.img_dir, "w_knight.png"),
            path.join(self.game.img_dir, "b_knight.png"),
        ]
        if self.color == "W":
            self.image = pg.image.load(self.images[0])
        else:
            self.image = pg.image.load(self.images[1])
        self.image.set_colorkey((255, 255, 255))
        self.game.pieces.append(self)
        self.pinned=self.is_pinned()
        self.possible_moves = self.get_possible_moves()
    def get_possible_moves(self):
        if not self.pinned:
            possible_moves = []
            letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
            x = letters.index(self.pos[0])
            y = int(self.pos[1])
            directions = [
                [x-1, y+2],
                [x-1, y-2],
                [x+1, y+2],
                [x+1, y-2],
                [x+2,y+1],
                [x-2, y+1],
                [x+2, y-1],
                [x-2, y-1]
            ]
            for direction in directions:
                current_x = direction[0]
                current_y = direction[1]
                if current_x>=0 and current_x<=7 and current_y>=1 and current_y<=8:
                    coord = str(letters[current_x])+str(current_y)
                    piece = self.game.piece_on_coord(coord)
                    if not (piece and piece.color == self.color):
                        possible_moves.append(coord)
        else:
            return []

        return possible_moves
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
            if self.type==piece.type and self.pos==piece.pos and self.color==piece.color:
                return True
        return False