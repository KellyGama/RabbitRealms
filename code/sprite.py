from typing import Any
import pygame
from config import *
import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y , width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0),(x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES

        self.x_change = 0
        self.y_change= 0

        self.facing = 'down'
        self.animation_loop = 1

        new_width = 50
        new_height = 50

        self.image = pygame.transform.scale(self.game.character_spritesheet.get_sprite(0,0,self.width, self.height),(new_width, new_height))
        

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.level = 10

    def update(self):
        self.movement()
        self.animate()
        self.collide_mouche()
        self.collide_troll()

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        diagonal_factor = 1 / math.sqrt(2) 

        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

        if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            self.x_change *= diagonal_factor
            self.y_change *= diagonal_factor
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            self.x_change *= diagonal_factor
            self.y_change *= diagonal_factor
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            self.x_change *= diagonal_factor
            self.y_change *= diagonal_factor
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            self.x_change *= diagonal_factor
            self.y_change *= diagonal_factor
    

    def collide_mouche(self):
        hits = pygame.sprite.spritecollide(self, self.game.mouche, False)
        if hits :
            self.kill()
            self.game.playing = False

    def collide_troll(self):
        hits = pygame.sprite.spritecollide(self, self.game.troll, False)
        if hits : 
            self.kill()
            self.game.playing = False


    

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits: 
                if self.x_change > 0:
                    self.rect.x= hits [0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits: 
                if self.y_change > 0:
                    self.rect.y= hits [0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(32, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(64, 0, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(0, 32, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(32, 32, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(0, 32, self.width, self.height),
                         self.game.character_spritesheet.get_sprite(64, 32, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(64, 64, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(0, 96, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(32, 96, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(0, 96, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(64, 96, self.width, self.height)]
        
        if self.facing == "down":
            if self.y_change == 0:
                self.image= self.game.character_spritesheet.get_sprite(0,0, self.width, self.height)
            else:
                self.image= down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "up":
            if self.y_change == 0:
                self.image= self.game.character_spritesheet.get_sprite(0,32, self.width, self.height)
            else:
                self.image= up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "left":
            if self.x_change == 0:
                self.image= self.game.character_spritesheet.get_sprite(0,64, self.width, self.height)
            else:
                self.image= left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1

        if self.facing == "right": 
            if self.x_change == 0:
                self.image= self.game.character_spritesheet.get_sprite(0,96, self.width, self.height)
            else:
                self.image= right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1



class Mouche(pygame.sprite.Sprite):
    def __init__(self,game, x, y):
        self.game = game
        self._layer = MOUCHE_LAYER
        self.groups = self.game.all_sprites, self.game.mouche
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right']) 

        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(1,2) 

        self.image = self.game.mouche_spritesheet.get_sprite(0,0, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.choose_direction()

        self.level = 10

    def choose_direction(self):
        self.facing = random.choice(['left', 'right', 'up', 'down'])

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.y_change = 0
        self.x_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= MOUCHE_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.choose_direction()
        elif self.facing == 'right':
            self.x_change += MOUCHE_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.choose_direction()
        elif self.facing == 'up':
            self.y_change -= MOUCHE_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.choose_direction()
        elif self.facing == 'down':
            self.y_change += MOUCHE_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.choose_direction()

    def animate(self):
        left_animations = [self.game.mouche_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.mouche_spritesheet.get_sprite(32, 0, self.width, self.height)]

        right_animations = [self.game.mouche_spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.game.mouche_spritesheet.get_sprite(32, 0, self.width, self.height)]

        up_animations = [self.game.mouche_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.mouche_spritesheet.get_sprite(32, 0, self.width, self.height)]

        down_animations = [self.game.mouche_spritesheet.get_sprite(0, 0, self.width, self.height),
                           self.game.mouche_spritesheet.get_sprite(32, 0, self.width, self.height)]

        if self.facing == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
        elif self.facing == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
        elif self.facing == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
        elif self.facing == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]

        self.animation_loop += 0.1
        if self.animation_loop >= 2:
            self.animation_loop = 1

class Troll(pygame.sprite.Sprite):
    def __init__(self,game, x, y):
        self.game = game
        self._layer = TROLL_LAYER
        self.groups = self.game.all_sprites, self.game.troll
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['up', 'down']) 

        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(25,30) 

        self.image = self.game.troll_spritesheet.get_sprite(0,0, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.choose_direction()

        self.level = 30

    def choose_direction(self):
        self.facing = random.choice(['up', 'down'])

    def update(self):
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.y_change = 0
        self.x_change = 0

    def movement(self):
        if self.facing == 'up':
            self.y_change -= TROLL_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.choose_direction()
        elif self.facing == 'down':
            self.y_change += TROLL_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.choose_direction()

    def animate(self):
        up_animations =[self.game.troll_spritesheet.get_sprite(0, 32, self.width, self.height),
                        self.game.troll_spritesheet.get_sprite(32, 32, self.width, self.height),
                        self.game.troll_spritesheet.get_sprite(64, 32, self.width, self.height)]

        down_animations = [self.game.troll_spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.game.troll_spritesheet.get_sprite(32, 0, self.width, self.height),
                            self.game.troll_spritesheet.get_sprite(64, 0, self.width, self.height)]

        if self.facing == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
        elif self.facing == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]

        self.animation_loop += 0.1
        if self.animation_loop >= 3:
            self.animation_loop = 1




class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x* TILESIZES
        self.y = y* TILESIZES
        self.width = TILESIZES
        self.height = TILESIZES
        

        self.image = self.game.terrain_spritesheet.get_sprite(32,0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZES
        self.y = y * TILESIZES
        self.width = TILESIZES
        self.height= TILESIZES

        self.image = self.game.terrain_spritesheet.get_sprite(0,0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Button:
    def __init__(self, x , y , width, height , fg , bg, content, fontsize):
        self.font = pygame.font.Font('font/Pixeltype.ttf', fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()

        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self,pos, pressed):
        if self.rect.collidepoint(pos):
            if pressed [0]:
                return True
            return False
        return False

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x , y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x= x
        self.y = y
        self.width = TILESIZES
        self.height = TILESIZES
        
        self.animation_loop = 0

        self.image = self.game.attacks_spritesheet.get_sprite(0,0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.mouche, True)
        troll_hits = pygame.sprite.spritecollide(self, self.game.troll, True)

        if hits:
            self.game.player.level += 10

        if troll_hits:
            self.game.player.level += 20

        for troll in troll_hits:
            if self.game.player.level >= troll.level:
                self.game.player.level += 30
                troll.kill()


    def animate(self):
        direction  = self.game.player.facing
        
        up_animations = [self.game.attacks_spritesheet.get_sprite(0, 0, self.width, self.height)]
        
        down_animations = [self.game.attacks_spritesheet.get_sprite(32, 0, self.width, self.height)]
        
        left_animations = [self.game.attacks_spritesheet.get_sprite(64,0, self.width, self.height)]

        right_animations = [self.game.attacks_spritesheet.get_sprite(96, 0, self.width, self.height)]

        if direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 1 :
                self.kill()
        if direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 1 :
                self.kill()
        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 1 :
                self.kill()
        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 1 :
                self.kill()

