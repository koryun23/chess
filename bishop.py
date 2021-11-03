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

    def coords_to_king(self):
        # print(king.pos, piece.pos)
        if self.color=="W":
            king = self.game.b_king

        else:
            king=self.game.w_king
        piece = self
        king_pos = king.pos
        #bishop - b4
        #king - e1
        coords = []
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        bishop_y = letters.index(piece.pos[0])
        bishop_x = int(piece.pos[1])
        king_y = letters.index(king_pos[0])
        king_x = int(king_pos[1])
        if bishop_y< king_y:
            diff_y=1
        else:
            diff_y=-1
        if bishop_x<king_x:
            diff_x=1
        else:
            diff_x=-1
        coord = piece.pos
        y=bishop_y#4
        x = bishop_x#1
        while coord!=king_pos:
            coord =letters[y]+str(x)
            if coord==king_pos:
                return coords
            if coord!=piece.pos:
                coords.append(coord)
            x+=diff_x
            y+=diff_y