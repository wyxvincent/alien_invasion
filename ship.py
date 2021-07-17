import pygame

class Ship():
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load(r'C:\Users\wyxvi\OneDrive\Coding\Python Lessons\AdenClass\Games\alien_invasion_v1.9\images\ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.shoot = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self, ship, width, height):
        if self.moving_right:
            if self.rect.centerx <= width:
                self.rect.centerx += 1
        if self.moving_left:
            if self.rect.centerx >= 0:
                self.rect.centerx -= 1
        if self.moving_up:
            if self.rect.centery >= 0 :
                self.rect.centery -= 1
        if self.moving_down:
            if self.rect.centery <= height:
                self.rect.centery += 1

    def center_ship(self):
        # 重置飞船：让飞船在屏幕底端居中
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom