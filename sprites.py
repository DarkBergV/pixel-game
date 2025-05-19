import pygame 
from tilemap import Tilemap
from utils import load_image
PATH_IMG = "img/"
PATH_PLAYER = "player\player\player1.png"
PATH_PLAYER_S = 'img\player\skeleton\player1.png'
PATH_PLAYER_Z = 'img\player\zombie\player1.png'
PATH_ENEMY_S_W = 'img\Enemy\skelly\walk\skeleton1.png'
PATH_ENEMY_Z_W = 'img\Enemy\zombie\walk\zombie1.png'


PLAYER_DAMAGE_EVENT = pygame.USEREVENT + 1
ENEMY_DAMAGE_EVENT = pygame.USEREVENT + 2

PLAYER_ATTACK_EVENT = pygame.USEREVENT + 3
COOLDOWN = pygame.USEREVENT + 4

class Body(pygame.sprite.Sprite):
    def __init__(self, game, pos, size, type):
        self.game = game
        self.pos = pos
        self.size = size 
       
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
       
        rect = self.rect()
        self.display = pygame.surface.Surface((rect.size))
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

        
        self.can_take_damage = True
        #attack direction
        self.attack_up = False
        self.attack_down = False
        self.attack_right = True
        #attack
        self.attack_direction = ''
        self.attack_animation('right')
        self.is_atacking = False
        self.attack_cooldown = False
        self.cooldown_time = 800
        
    def player_rect(self):
        return pygame.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def attack_animation(self, attack_direction):
        
        if self.attack_direction != attack_direction:
            self.attack_direction = attack_direction
            self.attack_anima = self.game.assets['attack' + '/' + self.attack_direction].copy()
    def update(self, tilemap, movement, offset=(0, 0)):
        
        player_rect = self.rect()
        hitbox = self.hitbox()
        for enemy in self.game.enemies:
            if player_rect.colliderect(enemy.rect()):
               
                if self.can_take_damage:
                    self.hp -=1

                    pygame.time.set_timer(PLAYER_DAMAGE_EVENT, 5000)
                 
                    self.can_take_damage = False
                    

                if enemy.status =='corpse':
                   
      
                    self.set_action(enemy.type)
                    self.status = enemy.type
           
    
        if self.status == 'skelly': #skelleton have quicker attacks, less damage
            self.cooldown_time = 300

        if self.status == 'zombie': #zombie have slower attacks, more damage
            self.cooldown_time = 1200

        if self.attack_down:
            self.attack_animation('down')
        if self.attack_up:
            self.attack_animation('up')
        
        if self.attack_right:
            self.attack_animation('right')
        
            
        self.attack_anima.update()
        
        
        
      
        return super().update(tilemap, movement, offset)
    
    def hitbox(self):
        if self.attack_up:
            return pygame.rect.Rect(self.pos[0], self.pos[1] - 32 ,32,32)
        if self.attack_down:
            return pygame.rect.Rect(self.pos[0], self.pos[1] + 24,32,32)
        if not self.flip:
            return pygame.rect.Rect(self.pos[0] + 32, self.pos[1] ,32,32)
        if self.flip:
            return pygame.rect.Rect(self.pos[0] - 32, self.pos[1] ,32,32)

    def render(self, surf, color, offset=(0, 0)):
        if self.is_atacking == True:
            hit = self.hitbox()
            attack = pygame.surface.Surface(hit.size)
            attack.fill((155,0,155))
            

            surf.blit(attack, (hit[0] - offset[0], hit[1] - offset[1]))
            surf.blit(pygame.transform.flip(self.attack_anima.img(), self.flip, False),
                (
                    self.pos[0] - offset[0] + self.anim_offset[0],
                    self.pos[1] - offset[1] + self.anim_offset[1],
                ))
    
       
        return super().render(surf, color, offset)

    
    def attack(self):
        if not self.attack_cooldown:
            pygame.time.set_timer(COOLDOWN, self.cooldown_time)
            self.attack_cooldown = True
            pygame.time.set_timer(PLAYER_ATTACK_EVENT , 500)
            self.is_atacking = True
            enemies = [enemy for enemy in self.game.enemies]
            hitbox = self.hitbox()
            for enemy in enemies:
                if hitbox.colliderect(enemy.rect()) and self.is_atacking:
                    enemy.take_damage()
       

class Enemy(Body):
    def __init__(self, game, pos, size, type, action):
        super().__init__(game, pos, size, type)
        self.hp = 5
        self.status = 'corpse'
        self.type = type
        self.set_action(action)
        self.can_take_damage = True
        

    def update(self, tilemap, movement, offset=(0, 0)):
        
        print(self.hp)
        super().update(tilemap, movement, offset)
        rect = self.rect()
     
        if self.hp == 0:
            return 'kill'
    
        
    def render(self, surf, color, offset=(0, 0)):
        if self.hp <=0:
            self.status = 'corpse'
            color = [0,0,0]
        return super().render(surf, color, offset)
    
    def take_damage(self):
      
        if self.can_take_damage:

            self.hp -=1
            pygame.time.set_timer(ENEMY_DAMAGE_EVENT, 2000)
            self.can_take_damage = False
            print(self.hp)

class Corpse(Body):
    def __init__(self, game, pos, size, type):
        super().__init__(game, pos, size, type)
    def update(self, tilemap, movement, offset=(0, 0)):


        return super().update(tilemap, movement, offset)
    def render(self, surf, color, offset=(0, 0)):
        return super().render(surf, color, offset)