from os import path
import pygame as pg
class Pawn:
    def __init__(self, game, color, pos):
        self.type = "PAWN"
        self.cell = None
        self.color = color
        self.pos = pos
        self.game = game
        self.images = [
            path.join(self.game.img_dir, "w_pawn.png"),
            path.join(self.game.img_dir, "b_pawn.png"),
        ]
        if self.color == "W":
            self.image = pg.image.load(self.images[0])
        else:
            self.image = pg.image.load(self.images[1])
        self.image.set_colorkey((255, 255, 255))
        self.game.pieces.append(self)
        self.attacked_cells = set()
        self.last_pos=self.pos
        self.possible_moves = self.get_possible_moves()

    def get_possible_moves(self):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        possible_moves = []
        if self.color == "W":
            if self.pos[1] == "2":

                coord = self.pos[0]+'4'
                if not self.game.piece_on_coord(coord):
                    possible_moves.append(coord)
                coord = self.pos[0]+"3"
                if not self.game.piece_on_coord(coord):
                    possible_moves.append(coord)
                else:
                    if possible_moves:
                        possible_moves.pop()
            elif self.pos[1] == "5":
                for piece in self.game.pieces:
                    if piece.type=="PAWN" and piece.color=="B" and piece.pos[1]=="5":
                        index = letters.index(self.pos[0])
                        right=-1
                        left=-1
                        if index ==0:
                            right=index+1
                        if index==len(letters)-1:
                            left = index-1
                        elif index >0 and index < len(letters):
                            left = index-1
                            right=index+1
                        if right>0:
                            if piece.pos[0] == letters[right] and (self.game.last_moved_piece.pos==piece.pos and self.game.last_moved_piece.color==piece.color and self.game.last_moved_piece.type==piece.type):
                                if piece.last_pos==piece.pos[0]+"7":

                                    possible_moves.append(piece.pos[0]+"6")
                        if left > 0:
                            if piece.pos[0] == letters[left] and (self.game.last_moved_piece.pos==piece.pos and self.game.last_moved_piece.color==piece.color and self.game.last_moved_piece.type==piece.type):
                                if piece.last_pos == piece.pos[0]+"7":

                                    possible_moves.append(piece.pos[0]+"6")
                coord =self.pos[0]+str(int(self.pos[1])+1)
                if not self.game.piece_on_coord(coord):
                    possible_moves.append(coord)
            else:
                coord =self.pos[0]+str(int(self.pos[1])+1)
                if not self.game.piece_on_coord(coord):
                    possible_moves.append(coord)
            current_index = letters.index(self.pos[0])
            right = current_index+1
            left = current_index-1
            if right >= 0 and right <8:
                right_pos = letters[right]+str(int(self.pos[1])+1)
                self.attacked_cells.add(right_pos)
                right_piece = self.game.piece_on_coord(right_pos)
                if right_piece and right_piece.color!=self.color:
                    possible_moves.append(right_pos)
            if left >= 0 and left<8:
                left_pos = letters[left]+str(int(self.pos[1])+1)
                self.attacked_cells.add(left_pos)
                left_piece = self.game.piece_on_coord(left_pos)
                if left_piece and left_piece.color!= self.color:
                    possible_moves.append(left_pos)

        else:
            if self.pos[1] == "7":

                coord = self.pos[0]+"5"
                if not self.game.piece_on_coord(coord): 
                    possible_moves.append(coord)
                coord = self.pos[0]+"6"
                if not self.game.piece_on_coord(coord):
                    possible_moves.append(coord)
                else:
                    if possible_moves:
                        possible_moves.pop()
            elif self.pos[1] == "4":
                for piece in self.game.pieces:
                    if piece.type=="PAWN" and piece.color=="W" and piece.pos[1] == "4":
                        index = letters.index(self.pos[0])
                        right=-1
                        left=-1
                        if index ==0:
                            right=index+1
                        if index==len(letters)-1:
                            left = index-1
                        elif index >0 and index < len(letters):
                            left = index-1
                            right=index+1
                        if right>0:
                            if piece.pos[0] == letters[right] and (self.game.last_moved_piece.pos==piece.pos and self.game.last_moved_piece.color==piece.color and self.game.last_moved_piece.type==piece.type):
                                if piece.last_pos == piece.pos[0]+"2":
                                    possible_moves.append(piece.pos[0]+"3")
                        if left >0:
                            if piece.pos[0] == letters[left] and (self.game.last_moved_piece.pos==piece.pos and self.game.last_moved_piece.color==piece.color and self.game.last_moved_piece.type==piece.type):
                                if piece.last_pos == piece.pos[0]+"2":
                                    possible_moves.append(piece.pos[0]+"3")
                coord = self.pos[0]+str(int(self.pos[1])-1)
                if not self.game.piece_on_coord(coord):
                    possible_moves.append(coord)
            else:
                coord = self.pos[0]+str(int(self.pos[1])-1)
                if not self.game.piece_on_coord(coord):
                    possible_moves.append(coord)
            current_index = letters.index(self.pos[0])
            right = current_index+1
            left = current_index-1
            if right >= 0 and right <8:
                right_pos = letters[right]+str(int(self.pos[1])-1)
                self.attacked_cells.add(right_pos)
                right_piece = self.game.piece_on_coord(right_pos)
                if right_piece and right_piece.color!=self.color:
                    possible_moves.append(right_pos)
            if left >= 0 and left<8:
                left_pos = letters[left]+str(int(self.pos[1])-1)
                self.attacked_cells.add(left_pos)
                left_piece = self.game.piece_on_coord(left_pos)
                if left_piece and left_piece.color!=self.color:
                    possible_moves.append(left_pos)
        return possible_moves
    def is_pinned(self):
        coords=[]
        for p in self.game.pieces:
            if p.color!=self.color:

                if p.type!='KNIGHT' and p.type!="KING" and p.type!="PAWN":
                    if self.pos in p.get_possible_moves():

                        b_coords = p.coords_to_king()
                        b_coords.append(p.pos)
                        if (p.type=="QUEEN" or p.type=="ROOK") and p.pos[0] == self.pos[0]:
                            print("YEEES")
                            continue
                        for bc in b_coords:
                            if len(bc)==3:
                                bc = bc[0]+bc[2]
                            coords.append(bc)

        number_of_pieces = 0
        for p in self.game.pieces:
            for coord in coords:
                if coord==p.pos and p.color==self.color:
                    number_of_pieces+=1
                    print(p.type, p.pos)
        if number_of_pieces==1:

            return True
        if self.pos[0]=="e":
            print(coords)
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
        