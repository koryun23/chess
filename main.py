import pygame as pg
from os import path
from chess_board import *
FPS = 30
board = get_board()
class Cell(pg.sprite.Sprite):
    def __init__(self, color, x, y):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.image = pg.Surface((60,60))
        self.image.fill(color)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.topleft = (self.x, self.y)
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((480,480))
        pg.display.set_caption("Chess")
        self.playing = True
        self.clock = pg.time.Clock()
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.cells = pg.sprite.Group()
        for i in range(8):
            for j in range(8):
                if board[i][j] == "W":
                    cur_color = (255, 255, 255)
                elif board[i][j] == "B":
                    cur_color =(0,0,0)
                cell = Cell(cur_color, i*60,j*60)
                self.all_sprites.add(cell)
                self.cells.add(cell)
        self.run()

    def update(self):
        self.all_sprites.update()
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                
    def draw(self):
        self.all_sprites.draw(self.screen)
        pg.display.flip()

g = Game()
while g.playing:
    g.new()
pg.quit()