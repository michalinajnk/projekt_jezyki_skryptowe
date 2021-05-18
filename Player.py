import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, colour, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Animation/CHARACTER_SPRITES/Black/0.png')
        self.img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)