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

        self.possible_moves = self.get_possible_moves()
    def get_possible_moves(self):
        if not self.is_pinned():
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
                        b_coords.append(p.pos)
                        for bc in b_coords:
                            coords.append(bc)
                        
        number_of_pieces = 0
        for p in self.game.pieces:
            for coord in coords:
                if coord==p.pos and p.color==self.color:
                    number_of_pieces+=1
        if number_of_pieces==1:
            return True
        return False
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
    