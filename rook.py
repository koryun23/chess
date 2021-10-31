from os import path
import pygame as pg
class Rook:
    def __init__(self, game, color, pos):
        self.type = "ROOK"
        self.cell = None
        self.color = color
        self.pos = pos
        self.game = game
        self.images = [
            path.join(self.game.img_dir, "w_rook.png"),
            path.join(self.game.img_dir, "b_rook.png"),
        ]
        if self.color == "W":
            self.image = pg.image.load(self.images[0])
        else:
            self.image = pg.image.load(self.images[1])
        self.image.set_colorkey((255, 255, 255))
        self.game.pieces.append(self)
        self.possible_moves = self.get_possible_moves()

    def get_possible_moves(self):
        letters =  ["a", "b", "c", "d", "e", "f", "g", "h"]
        possible_moves = []
        #vertical
        for i in range(int(self.pos[1]),9):
            coord = self.pos[0]+str(i)
            if coord != self.pos:

                piece = self.game.piece_on_coord(coord)
                if not(piece):
                    possible_moves.append(coord)
                
                elif piece and piece.color != self.color:
                    possible_moves.append(coord)
                    break
                else:
                    break
        for i in range(int(self.pos[1]),0,-1):
            coord = self.pos[0]+str(i)
            if coord != self.pos:

                piece = self.game.piece_on_coord(coord)
                if not(piece):
                    possible_moves.append(coord)
                elif piece and piece.color != self.color:
                    possible_moves.append(coord)
                    break
                else:
                    break
        #horizontal
        for i in range(letters.index(self.pos[0]),8):
            coord = letters[i]+self.pos[1]
            if coord!= self.pos: 

                piece = self.game.piece_on_coord(coord)
                if not(piece):

                    possible_moves.append(coord)
                elif piece and piece.color != self.color:
                    possible_moves.append(coord)
                    break
                else:
                    break
        for i in range(letters.index(self.pos[0]),-1, -1):
            coord = letters[i]+self.pos[1]
            if coord!= self.pos: 

                piece = self.game.piece_on_coord(coord)
                if not(piece):

                    possible_moves.append(coord)
                elif piece and piece.color != self.color:
                    possible_moves.append(coord)
                    break
                else:
                    break

        return possible_moves