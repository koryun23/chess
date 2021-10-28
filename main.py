import pygame as pg
from os import path
FPS = 30
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((500,500))
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
        pass

g = Game()
while g.playing:
    g.new()
pg.quit()