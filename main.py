import pygame as pg
from os import path
from chess_board import *
FPS = 30
WHITE = (255, 255, 255)
board = get_board()
class Cell:
    def __init__(self, color, x, y):
        # pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pg.Surface((60,60))
        self.image.fill(color)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.topleft = (self.x, self.y)
class King:
    def __init__(self,game, color, pos):
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
class Queen:
    def __init__(self, game, color, pos):
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
class Knight:
    def __init__(self, game, color, pos):
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
class Bishop:
    def __init__(self, game, color, pos):
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
        # self.image.set_colorkey(WHITE)
class Rook:
    def __init__(self, game, color, pos):
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
class Pawn:
    def __init__(self, game, color, pos):
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
                
    def draw(self):

        for i in range(8):
            for j in range(8):
                if board[i][j] == "W":
                    cur_color = (255, 255, 255)
                elif board[i][j] == "B":
                    cur_color =(165, 42, 42)
                cell = Cell(cur_color, j*60,i*60)
                self.cells.append(cell)
                self.coords.append(self.d[j]+str(8-i))
                pg.draw.rect(self.screen, cur_color, pg.Rect(cell.x,cell.y,60,60))
        for piece in self.pieces:
            pos = piece.pos
            index = self.coords.index(pos)
            cell = self.cells[index]

            color = (0,0,0) if piece.color=="B" else (255,255,255)
            rect = piece.image.get_rect()
            rect.topleft = (cell.x, cell.y)
            rect.x +=10
            rect.y+=10
            self.screen.blit(piece.image, rect)

        pg.display.flip()
        
    def load_pieces(self):
        self.w_king = King(self, "W","e1")
        self.b_king = King(self, "B", "e8")
        self.w_queen = Queen(self, "W", "d1")
        self.b_queen = Queen(self, "B", "d8")
        self.w_rook1 = Rook(self, "W", "a1")
        self.w_rook2 = Rook(self, "W", "h1")
        self.b_rook1 = Rook(self, "B", "a8")
        self.b_rook2 = Rook(self, "B", "h8")
        self.w_bishop1 = Bishop(self, "W", "c1")
        self.w_bishop2 = Bishop(self, "W", "f1")
        self.b_bishop1 = Bishop(self, "B", "c8")
        self.b_bishop2 = Bishop(self, "B", "f8")
        self.w_knight1 = Knight(self, "W", "b1")
        self.w_knight2 = Knight(self, "W", "g1")
        self.b_knight1 = Knight(self, "B", "b8")
        self.b_knight2 = Knight(self, "B", "g8")
        for i in range(8):
            self.w_pawn = Pawn(self, "W", self.d[i]+"2")
            self.pieces.append(self.w_pawn)
        for j in range(8):
            self.b_pawn = Pawn(self, "B", self.d[j]+"7")
            self.pieces.append(self.b_pawn)    
        self.pieces.append(self.w_king)
        self.pieces.append(self.b_king)
        self.pieces.append(self.w_queen)
        self.pieces.append(self.b_queen)
        self.pieces.append(self.w_rook1)
        self.pieces.append(self.w_rook2)
        self.pieces.append(self.b_rook1)
        self.pieces.append(self.b_rook2)
        self.pieces.append(self.w_bishop1)
        self.pieces.append(self.w_bishop2)
        self.pieces.append(self.b_bishop1)
        self.pieces.append(self.b_bishop2)
        self.pieces.append(self.w_knight1)
        self.pieces.append(self.w_knight2)
        self.pieces.append(self.b_knight1)
        self.pieces.append(self.b_knight2)
    
        # self.pieces.append(self.w_king)
    
g = Game()
while g.playing:
    g.new()
pg.quit()