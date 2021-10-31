from os import path
import pygame as pg


class King:
    def __init__(self,game, color, pos):
        self.type = "KING"
        self.cell = None
        self.color = color
        self.pos = pos
        self.game = game
        self.images = [
            path.join(self.game.img_dir, "w_king.png"),
            path.join(self.game.img_dir, "b_king.png"),
        ]
        if self.color == "W":
            self.image=pg.image.load(self.images[0])

        else:
            self.image = pg.image.load(self.images[1])
        self.image.set_colorkey((255, 255,255))
        self.game.pieces.append(self)
        self.possible_moves = self.get_possible_moves()
    def get_possible_moves(self):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        possible_moves = []
        x = letters.index(self.pos[0])
        y = int(self.pos[1])
        directions = [
            [x-1, y-1],
            [x-1, y],
            [x-1, y+1],
            [x, y-1],
            [x, y+1],
            [x+1, y-1],
            [x+1, y],
            [x+1, y+1],
        ]
        for direction in directions:
            current_x = direction[0]
            current_y=  direction[1]
            if current_x>=0 and current_x <= 7 and current_y >=1 and current_y<=8:
                coord = str(letters[current_x])+str(current_y)
                piece_on_coord = self.game.piece_on_coord(coord)
                if not (piece_on_coord and piece_on_coord.color == self.color):
                    possible_moves.append(coord)
        # print(possible_moves)
        return possible_moves
