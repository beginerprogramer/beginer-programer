import pygame


class CometFallEvent:
    # lors du chargement --> definir un pourcentage
    def __init__(self):
        self.percent = 0

    def add_percent(self):
        self.percent += 1

    def update_bar(self, surface):
        # bar noir en arriere plan
        pygame.draw.rect(surface, (0, 0, 0), [
            0, # l'axe des x
            pygame.get_height, # l'axe des y
            pygame.get_width,
            10

        ])
        # bar rouge en arriere plan
        pygame.draw.rect(surface, (187, 11, 11), [
            0,  # l'axe des x
            pygame.get_height(),  # l'axe des y
            (pygame.get_width() / 100) * self.percent,   # longeur de la fentre
            10  # epaiseur de la barre
            ])


