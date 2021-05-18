import pygame

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, colour, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(f'Animation/CHARACTER_SPRITES/{colour}/0.png')
        self.img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.img, self.rect)
        pass
