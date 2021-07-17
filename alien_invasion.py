import pygame
from pygame.display import update
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from alien import Alien
from game_status import GameStatus

def run_game():
    # 初始化pygame
    pygame.init()
    # 获取窗口大小、背景颜色的设置
    ai_settings = Settings()
    # 将窗口大小值给到pygame.display.set_mode
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    # 窗口名称
    pygame.display.set_caption("Alien Invasion")
    status = GameStatus(ai_settings, screen)
    # 获取飞船信息  
    ship = Ship(screen)
    bullets = Group()
    # 获取外星人信息
    # alien = Alien(ai_settings, screen)
    # 创建外星人群
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        if status.game_active:
            ship.update(ship, ai_settings.screen_width, ai_settings.screen_height)
            gf.shooting(ship, ai_settings, screen, bullets)
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, aliens, ship, status, screen, bullets)
        else:
            gf.game_over()
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, status)

run_game()