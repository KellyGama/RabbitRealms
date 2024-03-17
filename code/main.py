import pygame
import pygame.mixer
from sprite import *
from config import *
import sys 

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        pygame.mixer.init()

        pygame.display.set_caption("RabbitRealms : Ears of Destiny")
        new_icon = pygame.image.load("img/iconebunny.png")
        pygame.display.set_icon(new_icon)
        self.font = pygame.font.Font ('font/Pixeltype.ttf', 70)
        self.running = True

        self.intro_background = pygame.image.load('./img/backgroundintro.png')
        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.mouche_spritesheet = Spritesheet('img/mouche.png')
        self.troll_spritesheet = Spritesheet('img/troll.png')
        self.attacks_spritesheet = Spritesheet('img/attacks.png')

        self.camera = pygame.Rect(0, 0, WIN_WIDTH, WIN_HEIGHT)

        


    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "M":
                    Mouche(self, j ,i)
                if column == "T":
                    Troll(self, j, i)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.mouche = pygame.sprite.LayeredUpdates()
        self.troll = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        

        self.createTilemap()

    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - TILESIZES)
                    elif self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + TILESIZES)
                    elif self.player.facing == 'left':
                        Attack(self, self.player.rect.x - TILESIZES, self.player.rect.y)
                    elif self.player.facing == 'right':
                        Attack(self, self.player.rect.x + TILESIZES , self.player.rect.y)

    def update (self):
        self.all_sprites.update()

    
    def draw(self):
        self.screen.fill(GREEN)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()
    
    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()


    
    def intro_screen(self):
        intro = True

        pygame.mixer.music.load('backgroundmusic.mp3')  
        pygame.mixer.music.set_volume(0.2)  
        pygame.mixer.music.play(loops=-1)


        
        title = self.font.render('Rabbit Realms : Ears of Destiny', True, BLACK)
        title_rect = title.get_rect(x=400, y = 100)

        intro_image = pygame.image.load('img/iconebunny.png')
        intro_image = pygame.transform.rotozoom(intro_image, 0, 3)
        intro_image_rect = intro_image.get_rect(x=900, y= 338)

        play_button = Button(50, 350, 500, 50, BLACK, LIGHTBLUE, 'Commencer une nouvelle partie', 32)
        quit_button = Button(50, 400, 325, 50, BLACK, LIGHTBLUE, 'Quitter le jeu', 32)
        
        while intro: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
                
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro= False
            
            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                self.running = False
            
            
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(intro_image, intro_image_rect)
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()


    def game_over(self):
        text = self.font.render('Game Over', True, BLACK)
        text_rect = text.get_rect(x=600, y = 250)

        restart_button = Button(640 , 350, 120 ,50,BLACK, LIGHTBLUE, 'Reessayer',32)
        quit_button = Button(535, 410, 325, 50, BLACK, LIGHTBLUE, 'Quitter le jeu', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if restart_button.is_pressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
                self.running = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
  
    
g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()