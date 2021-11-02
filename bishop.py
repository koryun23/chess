from os import path
import pygame as pg


class Bishop:
    def __init__(self, game, color, pos):
        self.type = "BISHOP"
        self.cell = None
        self.color = color
        self.pos = pos
        self.game = game
        self.images = [
            path.join(self.game.img_dir, "w_bishop.png"),
            path.join(self.game.img_dir, "b_bishop.png"),
        ]
        if self.color == "W":
            self.image = pg.image.load(self.images[0])
        else:
            self.image = pg.image.load(self.images[1])
        self.game.pieces.append(self)
        # self.image.set_colorkey(WHITE)
        self.possible_moves = self.get_possible_moves()
    def get_possible_moves(self):
        possible_moves =[]
        letters =["a", "b", "c", "d", "e", "f", "g", "h"]
        #pos = "c4"
        x = int(self.pos[1])
        y = letters.index(self.pos[0])
        while x>=1 and y >=0:
            coord = letters[y]+str(x)
            if coord!=self.pos:
                piece = self.game.piece_on_coord(coord)
                if piece and piece.color == self.color:
                    break
                elif piece:
                    possible_moves.append(coord)
                    break
                possible_moves.append(coord)
            x-=1
            y-=1
        x = int(self.pos[1])
        y = letters.index(self.pos[0])
        while x<=8 and y >=0:
            coord = letters[y]+str(x)
            if coord != self.pos:
                piece = self.game.piece_on_coord(coord)
                if piece and piece.color == self.color:
                    break
                elif piece:
                    possible_moves.append(coord)
                    break
                possible_moves.append(coord)
            x+=1
            y-=1
        x = int(self.pos[1])
        y = letters.index(self.pos[0])
        while x<=8 and y< len(letters):
            coord = letters[y]+str(x)
    
            if coord!=self.pos:
                piece = self.game.piece_on_coord(coord)
                if piece and piece.color == self.color:
                    break
                elif piece:
                    possible_moves.append(coord)
                    break
                possible_moves.append(coord)
            x+=1
            y+=1
        x = int(self.pos[1])
        y = letters.index(self.pos[0])
        while x>=1 and y<len(letters):
            coord = letters[y]+str(x)
            if coord!= self.pos:
                piece = self.game.piece_on_coord(coord)
                if piece and piece.color == self.color:
                    break
                elif piece:
                    possible_moves.append(coord)
                    break
                possible_moves.append(coord)

            x-=1
            y+=1
            

        return possible_moves
