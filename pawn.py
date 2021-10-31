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

                
                
            else:
                coord =self.pos[0]+str(int(self.pos[1])+1)
                if not self.game.piece_on_coord(coord):
                    possible_moves.append(coord)
            current_index = letters.index(self.pos[0])
            right = current_index+1
            left = current_index-1
            if right >= 0 and right <8:
                right_pos = letters[right]+str(int(self.pos[1])+1)
                right_piece = self.game.piece_on_coord(right_pos)
                if right_piece and right_piece.color!=self.color:
                    possible_moves.append(right_pos)
            if left >= 0 and left<8:
                left_pos = letters[left]+str(int(self.pos[1])+1)

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
            else:
                coord = self.pos[0]+str(int(self.pos[1])-1)
                if not self.game.piece_on_coord(coord):
                    possible_moves.append(coord)
            current_index = letters.index(self.pos[0])
            right = current_index+1
            left = current_index-1
            if right >= 0 and right <8:
                right_pos = letters[right]+str(int(self.pos[1])-1)
                right_piece = self.game.piece_on_coord(right_pos)
                if right_piece and right_piece.color!=self.color:
                    possible_moves.append(right_pos)
            if left >= 0 and left<8:
                left_pos = letters[left]+str(int(self.pos[1])-1)

                left_piece = self.game.piece_on_coord(left_pos)
                if left_piece and left_piece.color!=self.color:
                    possible_moves.append(left_pos)
        return possible_moves
