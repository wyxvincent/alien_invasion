import pygame

class GameStatus():
    # 跟踪游戏的统计信息
    def __init__(self, ai_settings, screen):
        # 初始化统计信息
        self.ai_settings = ai_settings
        self.reset_status()
        self.game_active = True

        self.screen = screen
        self.image = pygame.image.load(r'C:\Users\wyxvi\OneDrive\Coding\Python Lessons\AdenClass\Games\alien_invasion_v1.9\images\ship.png')
        self.live_image = pygame.transform.scale(self.image, (30, 49))

        self.rect = self.live_image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

    def display_life(self):
        self.screen.blit(self.live_image, self.rect)

    def reset_status(self):
        # 初始化在游戏运行期间可能变化的统计信息
        self.ship_lifes = self.ai_settings.ship_lifes