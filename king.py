from os import path
import pygame as pg


class King:

    def __init__(self,game, color, pos):
        self.moved = False
        self.castled = False
        self.is_under_check=False
        self.is_under_double_check=False
        self.is_checkmated = False
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
        checking_piece=None
        if self.is_under_check:
            checking_piece=None
            for p in self.game.pieces:
                if p.color!=self.color and p.type!="KING" and p.type!="KNIGHT" and self.pos in p.possible_moves:
                    checking_piece = p
                    break
                elif p.type=="PAWN":
                    p.get_possible_moves()
            if checking_piece and checking_piece.type!='PAWN':
                current_turn = self.game.turn
                index = self.game.pieces.index(self)
                self.game.pieces.remove(self)
                
                checking_piece.possible_moves = checking_piece.get_possible_moves()
                self.game.pieces.insert(index, self)
                # checking_piece.possible_moves = checking_piece.get_possible_moves()
                self.game.turn = current_turn
            elif checking_piece:
                checking_piece.possible_moves = checking_piece.get_possible_moves()
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
                if piece_on_coord:
                    if piece_on_coord.color != self.color:
                        if piece_on_coord.is_protected()==False:
                            possible_moves.append(coord)
                                
                else:
                    cell_under_attack=False
                    for p in self.game.pieces:
                        if self.color!= p.color and p.type!='KING':
                            if p.type=="PAWN":
                                p.get_possible_moves()

                            if (coord in p.possible_moves and p.type!="PAWN") or (p.type=="PAWN" and coord in p.attacked_cells):

                                cell_under_attack=True
                                break
                    if not cell_under_attack:
                        possible_moves.append(coord)
                    cell_under_attack=False
                                
                    #if not cell_under_attack:
                    # possible_moves.append(coord)

                            
        if self.color == "W" and self.pos=="e1" and not self.moved and not self.is_under_check:
            if not self.game.piece_on_coord("f1") and not self.game.piece_on_coord("g1"):
                piece = self.game.piece_on_coord("h1")
                if piece and piece.type=="ROOK" and piece.moved==False:
                    possible_moves.append("g1")

                    coords = ["f1","g1"]

                    for p in self.game.pieces:
                        if (coords[0] in p.possible_moves or coords[1] in p.possible_moves) and p.color=="B":


                            possible_moves.pop()
                            break

            if not self.game.piece_on_coord("d1") and not self.game.piece_on_coord("c1") and not self.game.piece_on_coord("b1"):
                piece = self.game.piece_on_coord("a1")
                if piece and piece.type=="ROOK" and not piece.moved:
                    possible_moves.append("c1")

                    coords = ["d1", "c1"]
                    for p in self.game.pieces:
                        if (coords[0] in p.possible_moves or coords[1] in p.possible_moves) and p.color=="B":

                            possible_moves.pop()
                            break


        if self.color=="B" and self.pos == "e8" and not self.moved and not self.is_under_check:
            if not self.game.piece_on_coord("f8") and not self.game.piece_on_coord("g8"):
                piece = self.game.piece_on_coord("h8")

                if piece and piece.type=="ROOK" and not piece.moved:
                    possible_moves.append("g8")
                    coords = ["f8", "g8"]
                    for p in self.game.pieces:
                        if(coords[0] in p.possible_moves or coords[1] in p.possible_moves) and p.color=="W":
                            possible_moves.pop()
                            break
            if not self.game.piece_on_coord("d8") and not self.game.piece_on_coord("c8") and not self.game.piece_on_coord("b8"):
                piece = self.game.piece_on_coord("a8")
                
                if piece and piece.type == "ROOK" and not piece.moved:
                    possible_moves.append("c8")
                    coords = ["d8", "c8"]
                    for p in self.game.pieces:
                        if(coords[0] in p.possible_moves or coords[1] in p.possible_moves) and p.color=="W":
                            possible_moves.pop()
                            break

        return possible_moves