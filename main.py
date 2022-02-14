import pygame
import math
from comet_event import CometFallEvent
pygame.init()

# resolution screen
screen = pygame.display.set_mode((1020, 700))
pygame.display.set_caption('cool rocket')

# background
background = pygame.image.load('assets.lul/space.png')

# importer charger notre banniére
banner = pygame.image.load('assets.lul/banner.png')
banner = pygame.transform.scale(banner, (500, 500))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)

# importer ou charger notre bouton pour charger la partie
play_button = pygame.image.load('assets.lul/button.png')
play_button = pygame.transform.scale(play_button, (400, 150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width() / 3.33)
play_button_rect.y = math.ceil(screen.get_height() / 2)


# class game
class Game:

    def __init__(self):
        self.is_playing = False
        self.player = Player()
        self.comet_event = CometFallEvent
        self.pressed = {}

    def update(self, screen):
        screen.fill((0, 0, 0))
        # appliquer player
        screen.blit(self.player.image, self.player.rect)

        for projectile in self.player.all_projectiles:
            projectile.move()

        # apliquer bar du joueur
        self.player.update_health_bar(screen)

        # appliquer bar d evenement

        # appliquer l'ensemble d'image de laser
        self.player.all_projectiles.draw(screen)

        pygame.display.flip()

        # control
        if self.pressed.get(pygame.K_d) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_q) and self.player.rect.x > 0:
            self.player.move_left()
        if self.pressed.get(pygame.K_z) and self.player.rect.y > -40:
            self.player.move_up()
        elif self.pressed.get(pygame.K_s) and self.player.rect.y + self.player.rect.height < screen.get_height():
            self.player.move_down()


# class player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.velocity = 10
        self.all_projectiles = pygame.sprite.Group()
        self.image = pygame.image.load('assets.lul/small2.png')
        self.rect = self.image.get_rect()
        self.rect.x = 120
        self.rect.y = 500

    def update_health_bar(self, surface):
        # dessiner notre barre de vie
        pygame.draw.rect(surface, (128, 128, 128), [self.rect.x + 42, self.rect.y - -59, self.max_health, 20])
        pygame.draw.rect(surface, (0, 255, 0), [self.rect.x + 42, self.rect.y - -59, self.health, 20])

    def launch_projectile(self):
        self.all_projectiles.add(Projectile(self))

    def move_right(self):
        self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def move_up(self):
        self.rect.y -= self.velocity

    def move_down(self):
        self.rect.y += self.velocity


class Projectile(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.velocity = 19
        self.player = player
        self.image = pygame.image.load('assets.lul/laser.png')
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 118
        self.rect.y = player.rect.y + 86
        self.origin_image = self.image
        self.angle = 100

    def move(self):
        self.rect.x += self.velocity

        # suprimer le projectile
        self.remove()


game = Game()


running = True

# boucle jeu
while running:

    # apliquer background
    screen.blit(background, (-4, -50))
    # verifier si notre joueur a commence ou non
    if game.is_playing:
        # declencher les instruction de la partie
        game.update(screen)
    # verifier si notre jeu n a pas commence
    else:
        # ajuster mon ecran de bienvenue
        screen.blit(play_button, play_button_rect)
        screen.blit(banner, banner_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            pygame.quit()
            print('closing the game')

# check control fingers

        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True

            if event.key == pygame.K_SPACE:
                game.player.launch_projectile()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # verificaion pour savoir si la souris et en collision avec button play
            if play_button_rect.collidepoint(event.pos):
                # mettre le jeu en mode lancé
                game.is_playing = True
