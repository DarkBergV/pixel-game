import pygame 

class Body(pygame.sprite.Sprite):
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = pos
        self.size = size 
        self.display = pygame.surface.Surface((self.size))
        self.velocity = [0,0]

    def update(self,tilemap, movement):
        print(movement)
        self.pos[0]+=movement[0]
        self.pos[1]+=movement[1]


    def render(self, surf, offset = (0,0)):
        self.display.fill((255,70,10))
        surf.blit(self.display, (self.pos[0] - offset[0], self.pos[1]-offset[1]))

    def rect(self):
        return pygame.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])