import pygame as pg
from os import path
from pygame.constants import MOUSEBUTTONDOWN
from chess_board import *
from king import King
from queen import Queen
from rook import Rook
from bishop import Bishop
from knight import Knight
from pawn import Pawn
FPS = 30
WHITE = (255, 255, 255)
board = get_board()
class Cell:
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.image = pg.Surface((60,60))
        self.image.fill(color)
        self.rect =self.image.get_rect()
    def update(self):
        self.rect.topleft = (self.x, self.y)
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((480,480))
        pg.display.set_caption("Chess")
        self.playing = True
        self.clock = pg.time.Clock()
        self.d = {0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}
        self.cells = []
        self.coords = []
        self.pieces=[]
        self.rects = []
        self.highlighted_cells = []
        self.selected_piece = None
        self.selected_pieces = [] #stack of the selected pieces
        self.turn = "W"
        self.last_moved_piece = None
        self.load_data()
        self.load_pieces()
        self.king_attack_cells = []
    def load_data(self):
        self.dir = path.dirname(__file__)
        self.img_dir = path.join(self.dir, "img")
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    def new(self):
        self.run()
    def update(self):
        pass
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if (event.type == pg.MOUSEBUTTONDOWN and event.button==1):
                mouse = pg.mouse.get_pos()
                for cell in self.cells:
                    rect = pg.Rect(cell.x, cell.y, 60,60)
                    if self.rect_collided_point(rect, mouse[0], mouse[1]):
                        coord = self.cell_to_coord(cell)
                        piece = self.piece_on_coord(coord)

                        if piece and piece.color==self.turn:
                            if (not self.w_king.is_under_check and not self.b_king.is_under_check): #or \
                                # (self.w_king.is_under_check and piece.type=="KING" and piece.color=="W") or \
                                #     (self.b_king.is_under_check and piece.type=="KING" and piece.color=="B"):
                                if self.highlighted_cells:
                                    self.highlighted_cells=[]

                                self.selected_piece = piece
                                self.selected_pieces.append(self.selected_piece)
                                if self.selected_piece.type=="PAWN":
                                    self.selected_piece.last_pos = self.selected_piece.pos
                                

                                if self.selected_piece.type!="KING" and self.selected_piece.is_pinned():

                                    coords=[]
                                    for p in self.pieces:
                                        if p.color!=self.selected_piece.color:
                                            if p.type!='KNIGHT' and p.type!="KING" and p.type!="PAWN":
                                                if self.selected_piece.pos in p.get_possible_moves():
                                                    b_coords = p.coords_to_king()
                                                    coords+=b_coords
                                                    coords.append(p.pos)
                                            

                                    new_possible_moves=[]
                                    for coord in coords:
                                        if coord in self.selected_piece.get_possible_moves():
                                            new_possible_moves.append(coord)
                                
                                    self.selected_piece.possible_moves = new_possible_moves

                                    for coord in coords:
                                        for p in self.pieces:
                                            if p.pos==coord and p.color==self.selected_piece.color and p.pos!=self.selected_piece.pos:
                                                p.possible_moves = p.get_possible_moves()
                                                self.selected_piece.possible_moves = self.selected_piece.get_possible_moves()
                                else:
                                    self.selected_piece.posisble_moves = self.selected_piece.get_possible_moves()
                                for p in self.pieces:
                                    if p.color=="W" and self.b_king.pos in p.possible_moves:
                                        self.b_king.is_under_check=True
                                    elif p.color=="B" and self.w_king.pos in p.possible_moves:
                                        self.w_king.is_under_check=True
                                
                                for move in piece.possible_moves:
                                    possible_cell = self.coord_to_cell(move)
                                    if possible_cell:
                                        self.highlighted_cells.append(possible_cell)

                            else:
                                self.selected_piece = piece
                                if self.selected_piece.type=="KING":
                                    self.selected_piece.possible_moves = self.selected_piece.get_possible_moves()
                                self.selected_pieces.append(self.selected_piece)
                                if self.highlighted_cells:
                                    self.highlighted_cells=[]
                                if self.w_king.is_under_check:
                                    king = self.w_king #e1

                                elif self.b_king.is_under_check:
                                    king = self.b_king



                                checking_pieces = 0
                                for p in self.pieces:
                                    if p.color!=king.color:
                                        if king.pos in p.get_possible_moves():
                                            p.possible_moves = p.get_possible_moves()
                                        if (p.type!="PAWN" and king.pos in p.get_possible_moves()) or (p.type=="PAWN" and king.pos in p.attacked_cells):
                                            checking_pieces+=1


                                coords = []
                                for p in self.pieces:
                                    if p.color!=king.color:
                                        if (p.type!="PAWN" and king.pos in p.get_possible_moves()):
                                            if p.type=="BISHOP" or p.type=="ROOK" or p.type=="QUEEN":
                                                coords+=p.coords_to_king()
                                                coords.append(p.pos)
                                            elif p.type=="KNIGHT":
                                                coords.append(p.pos)
                                        elif p.type=="PAWN" and king.pos in p.attacked_cells:
                                            if p.is_protected()==False:
                                                coords.append(p.pos)
                                            
                                        elif p.type=="KNIGHT":
                                            if king.pos in p.get_possible_moves():
                                                coords.append(p.pos)

                                for p in self.pieces:
                                    if p.color==king.color:
                                        if checking_pieces==1:
                                            new_possible_moves = []
                                            if p.type!="KING":
                                                for c in coords:
                                                    if c in p.get_possible_moves():
                                                        new_possible_moves.append(c)
                                                p.possible_moves = new_possible_moves
                                            else:

                                                for c in p.get_possible_moves():
                                                    piece_on_coord = self.piece_on_coord(c)
                                                    if piece_on_coord:
                                                        if piece_on_coord.color!=king.color and piece_on_coord.is_protected()==False:
                                                            new_possible_moves.append(c)
                                                    else:
                                                        for p in self.pieces:
                                                            if not (p.type!="PAWN" and c in p.possible_moves) and not (p.type=="PAWN" and c in p.attacked_cells):
                                                                new_possible_moves.append(c)
                                                p.possible_moves = new_possible_moves
                                        else:
                                            if p.type!="KING":
                                                p.possible_moves = []
                                            else:
                                                p.possible_moves = p.get_possible_moves()
                                # checking_pieces=0
                                for move in piece.possible_moves:
                                    possible_cell = self.coord_to_cell(move)
                                    if possible_cell:
                                        self.highlighted_cells.append(possible_cell)
                        else:
                            if cell not in self.highlighted_cells:
                                if self.highlighted_cells:
                                    self.highlighted_cells=[] 
 
                for cell in self.highlighted_cells:
                    rect = pg.Rect(cell.x, cell.y, 60,60)
                    if self.rect_collided_point(rect, mouse[0], mouse[1]):
                        if self.turn=="W":
                            self.turn="B"
                        else:
                            self.turn="W"
                        coord = self.cell_to_coord(cell)
                        captured_piece = self.piece_on_coord(coord)
                        if captured_piece and captured_piece.color!=self.selected_piece.color:
                            self.pieces.remove(captured_piece)
                            captured_piece = None
                            if self.selected_piece.type=="PAWN":
                                self.selected_piece.attacked_cells = set()

                        elif not captured_piece:
                            
                            if self.selected_piece.type=="PAWN":
                                if coord[0] != self.selected_piece.pos[0]:
                                    captured_piece=self.piece_on_coord(coord[0]+self.selected_piece.pos[1])
                                    self.pieces.remove(captured_piece)
                                    captured_piece=None
                                self.selected_piece.attacked_cells = set()
                        self.selected_piece.pos = coord
                        self.last_moved_piece = self.selected_piece
                        self.highlighted_cells = []
                        w_king_under_check = False
                        b_king_under_check = False
                        if self.w_king.is_under_check:
                            for p in self.pieces:
                                if p.color=="B" and self.w_king.pos in p.get_possible_moves():
                                    w_king_under_check=True
                                    break
                        self.w_king.is_under_check=w_king_under_check
                        if self.b_king.is_under_check:
                            for p in self.pieces:
                                if p.color=="W" and self.b_king.pos in p.get_possible_moves():
                                    b_king_under_check=True
                                    break
                        self.b_king.is_under_check=b_king_under_check
                        for piece in self.pieces:
                            piece.possible_moves = piece.get_possible_moves()

                        for piece in self.pieces:
                            # if piece.color=="W" and self.b_king.pos in piece.possible_moves:
                            #     piece.possible_moves = piece.get_possible_moves()
                            if piece.color=="W" and ((piece.type!="PAWN" and self.b_king.pos in piece.possible_moves) or (piece.type=="PAWN" and self.b_king.pos in piece.attacked_cells)):
                                self.b_king.is_under_check=True

                            #elif piece.color=="B" and self.w_king.pos in piece.possible_moves:
                            elif piece.color=="B" and ((piece.type!="PAWN" and self.w_king.pos in piece.possible_moves) or (piece.type=="PAWN" and self.w_king.pos in piece.attacked_cells)):
                                self.w_king.is_under_check = True


                        if self.selected_piece.type=="KING":
                            if self.selected_piece.color=="W":
                                if self.w_king.moved==False:
                                    if coord=="g1":
                                        self.w_rook2.pos="f1"
                                        self.w_king.moved=True
                                    elif coord=="c1":
                                        self.w_rook1.pos="d1"
                                        self.w_king.moved=True
                                    else:
                                        self.w_king.moved=True
                            else:
                                if self.b_king.moved==False:
                                    if coord=="g8":
                                        self.b_rook2.pos="f8"
                                        self.b_king.moved= True
                                    elif coord=="c8":
                                        self.b_rook1.pos = "d8"
                                        self.b_king.moved=True
                                    else:
                                        self.b_king.moved=True
                        elif self.selected_piece.type=="ROOK":
                            self.selected_piece.moved=True





    def rook_to_king(self, king, piece):
            king_pos = king.pos
            coords = []
            letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
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
    
    def bishop_to_king(self, king, piece):

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
            while coord[0]!=king_pos[0] and coord[1] !=king_pos[1]:
                coord =letters[y]+str(x)
                if coord==king_pos:
                    return coords
                if coord!=piece.pos:
                    coords.append(coord)
                x+=diff_x
                y+=diff_y
            return []
    def queen_to_king(self, king, piece):
        r = Rook(self, piece.color, piece.pos)
        self.pieces.pop()
        b = Bishop(self, piece.color, piece.pos)
        self.pieces.pop()
        return self.rook_to_king(king, r)+self.bishop_to_king(king, b)
        
    def rect_collided_point(self,rect, x, y):
        if x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom:
            return True
        return False
    
    def draw(self):
        for i in range(8):
            for j in range(8):
                if board[i][j] == "W":
                    cur_color = (255, 255, 255)
                elif board[i][j] == "B":
                    cur_color =(165, 42, 42)
                if len(self.cells)!=64:
                    cell = Cell(cur_color, j*60,i*60)
                    self.cells.append(cell)
                for cell in self.highlighted_cells:
                    cell.image.fill((0,0,0))
                if len(self.coords)!= 64:
                    self.coords.append(self.d[j]+str(8-i))
                pg.draw.rect(self.screen, cur_color, pg.Rect(j*60,i*60,60,60))
                for cell in self.highlighted_cells:
                    if cell.x == j*60 and cell.y == i*60:
                        pg.draw.rect(self.screen, (255,200,0), pg.Rect(cell.x,cell.y, 60,60))
                            
                if len(self.rects)!=64:
                    self.rects.append(pg.Rect(self.cells[-1].rect))
        for piece in self.pieces:
            pos = piece.pos
            index = self.coords.index(pos)
            cell = self.cells[index]
            rect = piece.image.get_rect()
            rect.topleft = (cell.x, cell.y)
            piece.cell = cell
            rect.x +=10
            rect.y+=10
            self.screen.blit(piece.image, rect)
        pg.display.flip()
        
    def load_pieces(self):
        #create kings
        self.w_king = King(self, "W","e1")
        self.b_king = King(self, "B", "e8")
        #create knights
        self.w_knight1 = Knight(self, "W", "b1")
        self.w_knight2 = Knight(self, "W", "g1")
        self.b_knight1 = Knight(self, "B", "b8")
        self.b_knight2 = Knight(self, "B", "g8")
        #create queens
        self.w_queen = Queen(self, "W", "d1")
        self.b_queen = Queen(self, "B", "d8")
        #create rooks
        self.w_rook1 = Rook(self, "W", "a1")
        self.w_rook2 = Rook(self, "W", "h1")
        self.b_rook1 = Rook(self, "B", "a8")
        self.b_rook2 = Rook(self, "B", "h8")
        #create bishops
        self.w_bishop1 = Bishop(self, "W", "c1")
        self.w_bishop2 = Bishop(self, "W", "f1")
        self.b_bishop1 = Bishop(self, "B", "c8")
        self.b_bishop2 = Bishop(self, "B", "f8")
        #create pawns
        for i in range(8):
            self.w_pawn = Pawn(self, "W", self.d[i]+"2")
        for j in range(8):
            self.b_pawn = Pawn(self, "B", self.d[j]+"7")
    def coord_to_cell(self,coord):
        d = {"a":0,"b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
        x = d[coord[0]]*60
        y = (8-int(coord[1]))*60
        for cell in self.cells:
            if cell.x == x and cell.y == y:
                return cell
    def cell_to_coord(self, cell):
        d = {0:"a",1:"b", 2:"c",3:"d", 4:"e",5:"f", 6:"g", 7:"h"}
        y = d[cell.x//60]
        x = str(8-cell.y//60)
        coord = y+x
        return coord
    def piece_on_coord(self, coord):
        for piece in self.pieces:
            if piece.pos == coord:
                return piece
        
g = Game()
while g.playing:
    g.new()
pg.quit()