import pygame

class Player(pygame.sprite.Sprite):

#speed defines how many pixels player will move within each iteration

    def __init__(self, x, y, colour, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        img = pygame.image.load(f'Animation/CHARACTER_SPRITES/{colour}/0.png')
        self.img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def move(self, move_left, move_right):
        dx = 0
        dy = 0

        if move_left:
            dx = -self.speed
        if move_right:
            dx = self.speed

        self.rect.x += dx
        self.rect.y += dy

        pass

    def draw(self, screen):
        screen.blit(self.img, self.rect)
        pass


