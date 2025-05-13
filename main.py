import pygame
import sys

from sprites import Body
from tilemap import Tilemap
from utils import load_images, load_image

WIDTH = 640

HEIGHT = 480


class Main():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('dead game')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.surface.Surface((WIDTH//2, HEIGHT//2))
        self.running = True
        self.clock = pygame.time.Clock()

        #player
        self.movement = [0,0,0,0]
        self.scroll = [0,0]
        self.player = Body(self,[0,0], [16,16])


        #game assets
        self.assets = {'ground/ground': load_images('tiles'),
                      }

        self.tilemap = Tilemap(self)
        self.load()

    def load(self):
        self.tilemap.load('map.json')
        self.scene = []
        for ground in self.tilemap.extract([('ground/ground')], keep = True):
            self.scene.append(pygame.Rect(ground['pos'][0], ground['pos'][1], 32.0,32.0))
    def run(self):

        #map
       
        while self.running:
            self.display.fill((255,255,255))
            self.tilemap.render(self.display, self.scroll)
         

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True

                    if event.key == pygame.K_d:
                        self.movement[1] = True

                    if event.key == pygame.K_w:
                        self.movement[2] = True

                    if event.key == pygame.K_s:
                        self.movement[3] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    
                    if event.key == pygame.K_d:
                        self.movement[1] = False

                    if event.key == pygame.K_w:
                        self.movement[2] = False

                    if event.key == pygame.K_s:
                        self.movement[3] = False

            
            #player movement
            self.scroll[0]+= (self.player.rect().centerx - self.display.get_width()/2 - self.scroll[0])
            self.scroll[1]+= (self.player.rect().centery - self.display.get_height()/2 - self.scroll[1])
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))


            self.player.update(self.tilemap, [self.movement[1] - self.movement[0] , self.movement[3] - self.movement[2]])
            self.player.render(self.display, render_scroll)
                    


            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),(0,0)) 
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Main()
    while game.running:
        game.run()

    pygame.quit()
    sys.exit()
