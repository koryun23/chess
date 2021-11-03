from os import path
import pygame as pg
class Rook:
    def __init__(self, game, color, pos):
        self.moved=False
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
    def coords_to_king(self):
            # king_pos = king.pos
            coords = []
            letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
            if self.color=="W":
                king_pos=self.game.w_king.pos
            else:
                king_pos=self.game.b_king.pos
            piece = self
        # if piece.type=="ROOK":
            if piece.pos[0] == king_pos[0]:
                if int(piece.pos[1]) > int(king_pos[1]):
                    for i in range(int(king_pos[1]),int(piece.pos[1]),1):
                        coords.append(king_pos[0]+str(i))
                else:
                    for i in range(int(piece.pos[1]), int(king_pos[1]), 1):
                        coords.append(piece.pos+str(i))
            else:
                if letters.index(king_pos[0]) > letters.index(piece.pos[0]):
                    start = letters.index(piece.pos[0])
                    end = letters.index(king_pos[0])
                else:
                    start = letters.index(king_pos[0])
                    end = letters.index(piece.pos[0])
                for i in range(start+1,end):
                    coords.append(letters[i]+str(king_pos[1]))

            return coords
    