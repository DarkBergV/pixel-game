import pygame 
from tilemap import Tilemap

class Body(pygame.sprite.Sprite):
    def __init__(self, game, pos, size, type):
        self.game = game
        self.pos = pos
        self.size = size 
        self.display = pygame.surface.Surface((self.size))
        self.velocity = [0,0]
        self.collisions = {"up":False,"down":False,"left":False,"right":False}
        self.type = type


        #animation stuff
        self.action = ''
        self.anim_offset = (-3,-3)
        self.flip = False
        self.gravity = True

    def set_action(self,action):

        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()


    def update(self,tilemap, movement, offset = (0,0)):
        self.collisions = {"up":False,"down":False,"left":False,"right":False}
        framemove = (movement[0]  + self.velocity[0], movement[1] + self.velocity[1])
        self.animation.update()
       


        #note to self: always put the body_rect after the frame move
        self.pos[0]+=framemove[0] * 2
        body_rect_x = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if body_rect_x.colliderect(rect):
                
                if framemove[0] < 0:
                    self.collisions['left']  = True
                    body_rect_x.left = rect.right
                    
                 
                if framemove[0] > 0:
                    
                    self.collisions['right']  = True
                    body_rect_x.right = rect.left 
                    
            
                self.pos[0] = body_rect_x.x
               

        #note to self: always put the body_rect after the frame move
        self.pos[1]+=framemove[1] * 2
        body_rect = self.rect()
        for rect in tilemap.physics_rect_around(self.pos):
            if body_rect.colliderect(rect):
               
                if framemove[1]< 0:
                    self.collisions['up']  = True
                    body_rect.top = rect.bottom 
                    
                if framemove[1] > 0:
                    self.collisions['down']  = True
                    body_rect.bottom = rect.top
                self.pos[1] = body_rect.y
      
        if movement[0] > 0:
            self.flip = False

        if movement[0] < 0:
            self.flip = True


    def render(self, surf, color, offset = (0,0)):
       
        self.display.fill(color)
        
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False),
                  (
                      self.pos[0] - offset[0] + self.anim_offset[0],
                      self.pos[1] - offset[1] + self.anim_offset[1],
                  ))

    def rect(self):
        return pygame.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    

class Player(Body):
    def __init__(self, game, pos, size, type):
        super().__init__(game, pos, size, type)
        self.hp = 0
        self.status = 'player_head'
        self.set_action('walk')
        

    def update(self, tilemap, movement, offset=(0, 0)):
        player_rect = self.rect()
        
        for enemy in self.game.enemies:
            if player_rect.colliderect(enemy.rect()):
                enemy.hp-=1

                if enemy.status =='corpse':
                    self.status = 'player_' + enemy.type
                    print(self.status)
             
        return super().update(tilemap, movement, offset)
    
    def render(self, surf, color, offset=(0, 0)):
       
        return super().render(surf, color, offset)
    
    def attack(self, surf, offset = (0,0)):
        attack_rect = pygame.rect.Rect(self.pos[0] , self.pos[1], self.size[0], self.size[1])
        attack_display = pygame.surface.Surface((32,16))
        attack_display.fill([0,255,52])
        surf.blit(attack_display, (attack_rect[0]+ 32 - offset[0], attack_rect[1] - offset[1]))
       

class Enemy(Body):
    def __init__(self, game, pos, size, type, action):
        super().__init__(game, pos, size, type)
        self.hp = 5
        self.status = 'enemy'
        self.type = type
        self.set_action(action)
        

    def update(self, tilemap, movement, offset=(0, 0)):
        
  
        super().update(tilemap, movement, offset)
        if self.hp == 0:
            return 'kill'
        
    def render(self, surf, color, offset=(0, 0)):
        if self.hp <=0:
            self.status = 'corpse'
            color = [0,0,0]
        return super().render(surf, color, offset)
    

class Corpse(Body):
    def __init__(self, game, pos, size, type):
        super().__init__(game, pos, size, type)
    def update(self, tilemap, movement, offset=(0, 0)):


        return super().update(tilemap, movement, offset)
    def render(self, surf, color, offset=(0, 0)):
        return super().render(surf, color, offset)