import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()

        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)

    ## Adding Scroll effect to level/screen
    def update(self, x_shift):
        self.rect.x += x_shift