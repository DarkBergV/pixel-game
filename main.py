import pygame
import sys
#test
from sprites import Body, Player, Enemy, Corpse
from tilemap import Tilemap
from utils import load_images, load_image, Animation

WIDTH = 640

HEIGHT = 480

PLAYER_DAMAGE_EVENT = pygame.USEREVENT + 1
ENEMY_DAMAGE_EVENT = pygame.USEREVENT + 2
PLAYER_ATTACK_EVENT = pygame.USEREVENT + 3
COOLDOWN = pygame.USEREVENT + 4
ENEMY_DIED_EVENT = pygame.USEREVENT + 5

class Main():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('dead game')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.surface.Surface((WIDTH//4, HEIGHT//4))
        self.running = True
        self.clock = pygame.time.Clock()

        #game assets
        self.assets = {'ground/ground': load_images('tiles/ground'),
                        'player/walk': Animation(load_images('player/player')),
                        'player/skelly': Animation(load_images('player/skeleton')),
                        'player/zombie':Animation(load_images('player/zombie')),
                        'skelly/walk': Animation(load_images('Enemy/skelly/walk')),
                        'zombie/walk': Animation(load_images('Enemy/zombie/walk')),
                        'attack/right':Animation(load_images('attack/right')), 
                        'attack/up':Animation(load_images('attack/up')), 
                        'attack/down':Animation(load_images('attack/down')), 
                        'player/rect':load_image('player\player\player1.png'),
                        'zombie/dead':Animation(load_images('Enemy/zombie/dead')),
                        'skelly/dead':Animation(load_images('Enemy/skelly/dead'))
                        


                      }

        #player
        self.movement = [0,0,0,0]
        self.scroll = [0,0]
        self.dead = 0
        self.hp_font = pygame.font.Font(None, size = 40)
        
       
        
        #enemies

        self.remove_body = False

        self.corpses = []



     
        self.tilemap = Tilemap(self, tilesize=32)
        self.load()

    def load(self):
        self.tilemap.load('map.json')
        self.scene = []
        self.enemies = []

        for ground in self.tilemap.extract([('ground/ground')], keep = True):
            self.scene.append(pygame.Rect(ground['pos'][0], ground['pos'][1], 32.0,32.0))
        for spawner in self.tilemap.extract([('spawners',0), ('spawners', 1), ('spawners', 2)]):
            if spawner['variant'] == 0:
                self.player = Player(self,spawner['pos'],(32,32), 'player')
            if spawner['variant'] == 1:
                enemy2 = Enemy(self, spawner['pos'], (32,32), 'skelly', 'walk')
                self.enemies.append(enemy2)
            if spawner['variant'] == 2:
                
                enemy = Enemy(self, spawner['pos'], (32,32), 'zombie', 'walk')
                self.enemies.append(enemy)

        self.dead = 0


            
                
    def run(self):

        #map
       
        while self.running:
            self.display.fill((155,155,155))
            self.tilemap.render(self.display, self.scroll)
            hp_text = self.hp_font.render(f'hp:{self.player.hp}', True, (0,0,0))
        
         
            if self.dead:
                self.dead+=1
                if self.dead > 40:
                    self.load()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == PLAYER_DAMAGE_EVENT:
                    self.player.can_take_damage = True
                    pygame.time.set_timer(PLAYER_DAMAGE_EVENT,0)
                if event.type == ENEMY_DAMAGE_EVENT:
                    
                    pygame.time.set_timer(ENEMY_DAMAGE_EVENT,0)
                if event.type == COOLDOWN:
                    self.player.attack_cooldown = False
                    pygame.time.set_timer(COOLDOWN, 0)
                if event.type == PLAYER_ATTACK_EVENT:
                    self.player.is_atacking = False
                    self.player.attack_anima.done = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                        self.player.attack_down = False
                        self.player.attack_up = False
                        self.player.attack_right = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                        self.player.attack_down = False
                        self.player.attack_up = False
                        self.player.attack_right = True

                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                        self.player.attack_up = True
                        self.player.attack_down = False
                        self.player.attack_right = False

                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                        self.player.attack_down = True
                        self.player.attack_up = False
                        self.player.attack_right = False

                    if event.key == pygame.K_z:
                        if not self.player.attack_cooldown:
                            self.player.attack()
                    if event.key == pygame.K_x:
                        self.player.player_head()
                            
                    

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

                    if event.key == pygame.K_UP:
                        self.movement[2] = False

                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False

                 

            
            #player movement
            self.scroll[0]+= (self.player.rect().centerx - self.display.get_width()/2 - self.scroll[0])
            self.scroll[1]+= (self.player.rect().centery - self.display.get_height()/2 - self.scroll[1])
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            if not self.dead:
                player_dies = self.player.update(self.tilemap, (self.movement[1] - self.movement[0] , self.movement[3] - self.movement[2]), render_scroll)
                self.player.render(self.display, (255,75,25),render_scroll)
                if player_dies:
                    self.dead+=1


            if len(self.enemies)>0: 
                for enemy in self.enemies:
                    status = enemy.update(self.tilemap, (0,0))
                    enemy.render(self.display,(0,22,200), self.scroll)

                 
      
        

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()),(0,0)) 
            self.screen.blit(hp_text, (50,60))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    game = Main()
    while game.running:
        game.run()

    pygame.quit()
    sys.exit()
