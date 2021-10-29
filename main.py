import pygame as pg
from os import path

from pygame.constants import MOUSEBUTTONDOWN
from chess_board import *
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

class King:
    def __init__(self,game, color, pos):
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
        self.image.set_colorkey(WHITE)
        self.game.pieces.append(self)

class Queen:
    def __init__(self, game, color, pos):
        self.cell = None
        self.color = color
        self.pos = pos
        self.game = game
        self.images = [
            path.join(self.game.img_dir, "w_queen.png"),
            path.join(self.game.img_dir, "b_queen.png"),
        ]
        if self.color == "W":
            self.image = pg.image.load(self.images[0])
        else:
            self.image = pg.image.load(self.images[1])
        self.image.set_colorkey(WHITE)
        self.game.pieces.append(self)

class Knight:
    def __init__(self, game, color, pos):
        self.cell = None
        self.color = color
        self.pos = pos
        self.game = game
        self.images = [
            path.join(self.game.img_dir, "w_knight.png"),
            path.join(self.game.img_dir, "b_knight.png"),
        ]
        if self.color == "W":
            self.image = pg.image.load(self.images[0])
        else:
            self.image = pg.image.load(self.images[1])
        self.image.set_colorkey(WHITE)
        self.game.pieces.append(self)

class Bishop:
    def __init__(self, game, color, pos):
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
class Rook:
    def __init__(self, game, color, pos):
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
        self.image.set_colorkey(WHITE)
        self.game.pieces.append(self)

class Pawn:
    def __init__(self, game, color, pos):
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
        self.image.set_colorkey(WHITE)
        self.game.pieces.append(self)

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
                print(mouse)

                for cell in self.cells:
                    rect = pg.Rect(cell.x, cell.y, 60,60)
                    if self.rect_collided_point(rect, mouse[0], mouse[1]):
                        print("collided")
                        break
    def rect_collided_point(self,rect, x, y):
        if x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom:
            print(f"rect coords:{rect.x, rect.y}" )
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
                    self.cells.append(Cell(cur_color, j*60,i*60))
                if len(self.coords)!= 64:
                    self.coords.append(self.d[j]+str(8-i))
                pg.draw.rect(self.screen, cur_color, pg.Rect(j*60,i*60,60,60))
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
            self.pieces.append(self.w_pawn)
        for j in range(8):
            self.b_pawn = Pawn(self, "B", self.d[j]+"7")
            self.pieces.append(self.b_pawn)    
    def coord_to_cell(self,coord):
        d = {"a":0,"b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
        x = d[coord[0]]*60
        y = int(coord[1])*60
        for cell in self.cells:
            if cell.x == x and cell.y == y:
                return cell
    def cell_to_coord(self, cell):
        d = {0:"a",1:"b", 2:"c",3:"d", 4:"e",5:"f", 6:"g", 7:"h"}
        x = d[cell.x//60]
        y = str(cell.y//60)
        coord = x+y
        return coord
    def piece_on_coord(self, coord):
        d = {"a":0,"b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
        x = d[coord[0]]*60
        y = int(coord[1])*60
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece
    # def highlight(self, cell):
    #     cell.image.fill((0, 255, 255))
g = Game()
while g.playing:
    g.new()
pg.quit()