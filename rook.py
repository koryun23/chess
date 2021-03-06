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
    def coords_to_king(self):
            # king_pos = king.pos
            coords = []
            letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
            if self.color=="W":
                king_pos=self.game.b_king.pos
            else:
                king_pos=self.game.w_king.pos
            piece = self
        # if piece.type=="ROOK":
            if piece.pos[0] == king_pos[0]:
                if int(piece.pos[1]) > int(king_pos[1]):
                    for i in range(int(king_pos[1])+1,int(piece.pos[1]),1):
                        coords.append(king_pos[0]+str(i))
                else:
                    for i in range(int(piece.pos[1])+1, int(king_pos[1]), 1):
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

            for i in range(len(coords)):
                if len(coords[i])>2:
                    coords[i] = coords[i][0]+coords[i][2]
            print(coords)
            return coords
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
        