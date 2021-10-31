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
        self.image.set_colorkey(WHITE)
        self.game.pieces.append(self)
        self.possible_moves = self.get_possible_moves()
    def get_possible_moves(self):
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
                if not (piece_on_coord and piece_on_coord.color == self.color):
                    possible_moves.append(coord)
        # print(possible_moves)
        return possible_moves
class Queen:
    def __init__(self, game, color, pos):
        self.type = "QUEEN"
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
        self.possible_moves = self.get_possible_moves()
    def get_possible_moves(self):
        pass
class Knight:
    def __init__(self, game, color, pos):
        self.type = "KNIGHT"
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
        self.possible_moves = self.get_possible_moves()
    def get_possible_moves(self):
        possible_moves = []
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        x = letters.index(self.pos[0])
        y = int(self.pos[1])
        directions = [
            [x-1, y+2],
            [x-1, y-2],
            [x+1, y+2],
            [x+1, y-2],
            [x+2,y+1],
            [x-2, y+1],
            [x+2, y-1],
            [x-2, y-1]
        ]
        for direction in directions:
            current_x = direction[0]
            current_y = direction[1]
            if current_x>=0 and current_x<=7 and current_y>=1 and current_y<=8:
                coord = str(letters[current_x])+str(current_y)
                piece = self.game.piece_on_coord(coord)
                if not (piece and piece.color == self.color):
                    possible_moves.append(coord)

        return possible_moves
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
        return []
class Rook:
    def __init__(self, game, color, pos):
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
        self.image.set_colorkey(WHITE)
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
                if not(piece and piece.color == self.color):
                    possible_moves.append(coord)
                else:
                    break
        for i in range(int(self.pos[1]),0,-1):
            coord = self.pos[0]+str(i)
            if coord != self.pos:

                piece = self.game.piece_on_coord(coord)
                if not(piece and piece.color == self.color):
                    possible_moves.append(coord)
                else:
                    break
        #horizontal
        for i in range(letters.index(self.pos[0]),8):
            coord = letters[i]+self.pos[1]
            if coord!= self.pos: 

                piece = self.game.piece_on_coord(coord)
                if not(piece and piece.color == self.color):

                    possible_moves.append(coord)
                else:
                    break
        for i in range(letters.index(self.pos[0]),-1, -1):
            coord = letters[i]+self.pos[1]
            if coord!= self.pos: 

                piece = self.game.piece_on_coord(coord)
                if not(piece and piece.color == self.color):

                    possible_moves.append(coord)
                else:
                    break

        return possible_moves
        

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
        self.image.set_colorkey(WHITE)
        self.game.pieces.append(self)
        self.possible_moves = self.get_possible_moves()
    def get_possible_moves(self):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        possible_moves = []
        if self.color == "W":
            if self.pos[1] == "2":
                coord = self.pos[0]+"3"
                if not self.game.piece_on_coord(coord):
                    possible_moves.append(coord)
                coord = self.pos[0]+"4"
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
                right_piece = self.game.piece_on_coord(right_pos)
                if right_piece:
                    possible_moves.append(right_pos)
            if left >= 0 and left<8:
                left_pos = letters[left]+str(int(self.pos[1])+1)

                left_piece = self.game.piece_on_coord(left_pos)
                if left_piece:
                    possible_moves.append(left_pos)

        else:
            if self.pos[1] == "7":
                coord = self.pos[0]+"6"
                if not self.game.piece_on_coord(coord):
                    possible_moves.append(coord)
                coord = self.pos[0]+"5"
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
                right_piece = self.game.piece_on_coord(right_pos)
                if right_piece:
                    possible_moves.append(right_pos)
            if left >= 0 and left<8:
                left_pos = letters[left]+str(int(self.pos[1])-1)

                left_piece = self.game.piece_on_coord(left_pos)
                if left_piece:
                    possible_moves.append(left_pos)
        return possible_moves
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

                        if piece:
                            # print(piece.type)
                            self.selected_piece = piece
                            self.selected_piece.posisble_moves = self.selected_piece.get_possible_moves()
                            print(self.selected_piece.possible_moves)
                            for move in piece.possible_moves:
                                # print(move)
                                possible_cell = self.coord_to_cell(move)
                                if possible_cell:
                                    self.highlighted_cells.append(possible_cell)
                # print(self.highlighted_cells)
                for cell in self.highlighted_cells:
                    # if cell:
                    rect = pg.Rect(cell.x, cell.y, 60,60)
                    if self.rect_collided_point(rect, mouse[0], mouse[1]):
                        coord = self.cell_to_coord(cell)
                        self.selected_piece.pos = coord
                        self.highlighted_cells = []
                        for piece in self.pieces:
                            piece.possible_moves = piece.get_possible_moves()
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
                    # if cell:
                        cell.image.fill((0,0,0))
                if len(self.coords)!= 64:
                    self.coords.append(self.d[j]+str(8-i))
                pg.draw.rect(self.screen, cur_color, pg.Rect(j*60,i*60,60,60))
                for cell in self.highlighted_cells:
                    # if cell:
                        if cell.x == j*60 and cell.y == i*60:
                            pg.draw.rect(self.screen, (0,0,0), pg.Rect(cell.x,cell.y, 60,60))
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