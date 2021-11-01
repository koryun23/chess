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
        self.turn = "W"
        self.load_data()
        self.load_pieces()

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
                            if piece.type=="KING":
                                print(piece.color+" "+str(piece.is_under_check))
                            # if not (piece.type=="KING" and piece.color=="W" and piece.is_under_check) and \
                            #     not(piece.type=="KING" and piece.color=="B" and piece.is_under_check):
                            if not self.w_king.is_under_check and not self.b_king.is_under_check:
                                if self.highlighted_cells:
                                    self.highlighted_cells=[]
                                self.selected_piece = piece
                                self.selected_piece.posisble_moves = self.selected_piece.get_possible_moves()
                                for p in self.pieces:
                                    p.possible_moves = p.get_possible_moves()
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
                                pass
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
                        self.selected_piece.pos = coord

                        self.highlighted_cells = []
                        for piece in self.pieces:
                            piece.possible_moves = piece.get_possible_moves()
                        for piece in self.pieces:
                            if piece.color=="W" and self.b_king.pos in piece.possible_moves:
                                self.b_king.is_under_check=True
                                print("CHECK")
                            elif piece.color=="B" and self.w_king.pos in piece.possible_moves:
                                self.w_king.is_under_check = True
                                print("CHECK")

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
                                print(self.b_king.moved)
                                if self.b_king.moved==False:
                                    print(coord)
                                    if coord=="g8":
                                        self.b_rook2.pos="f8"
                                        self.b_king.moved= True
                                    elif coord=="c8":
                                        self.b_rook1.pos = "d8"
                                        self.b_king.moved=True
                                            
                        elif self.selected_piece.type=="ROOK":
                            self.selected_piece.moved=True

                            
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

        #create knights
        self.w_knight1 = Knight(self, "W", "b1")
        self.w_knight2 = Knight(self, "W", "g1")
        self.b_knight1 = Knight(self, "B", "b8")
        self.b_knight2 = Knight(self, "B", "g8")
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