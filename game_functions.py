import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from tkinter import *
from tkinter import messagebox
import alien_invasion as ai

# 事件检查方法
def check_events(ai_settings, screen, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_RIGHT:
                ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                ship.moving_left = True
            elif event.key == pygame.K_UP:
                ship.moving_up = True
            elif event.key == pygame.K_DOWN:
                ship.moving_down = True
            elif event.key == pygame.K_SPACE:
                ship.shoot = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False
            elif event.key == pygame.K_UP:
                ship.moving_up = False
            elif event.key == pygame.K_DOWN:
                ship.moving_down = False
            elif event.key == pygame.K_SPACE:
                ship.shoot = False

def shooting(ship, ai_settings, screen, bullets):
    if ship.shoot:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def update_screen(ai_settings, screen, ship, bullets, aliens, status):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    update_ship_lifes(status)
    ship.blitme()
    # alien.blitme()
    aliens.draw(screen)
    pygame.display.flip()
    
def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width
    # 计算每行能放多少个外星人
    number_aliens_x = int(available_space_x/(2*alien_width))
    for alien_number in range(number_aliens_x):
        # 创建一个外星人并将其加入当前行
        alien = Alien(ai_settings, screen)
        alien.x = alien_width + 2*alien_width*alien_number
        alien.rect.x = alien.x
        aliens.add(alien)

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, screen, ship, aliens, bullets, status):
    # 检查是否有外星人到达了屏幕底端
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, screen, ship, aliens, bullets, status)
            break

def update_aliens(ai_settings, aliens, ship, status, screen, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, ship, aliens, bullets, status)
    # 检查是否有外星人到达了屏幕底端
    check_aliens_bottom(ai_settings, screen, ship, aliens, bullets, status)

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

def ship_hit(ai_settings, screen, ship, aliens, bullets, status):
    # 响应外星人撞到的飞船
    if status.ship_lifes > 0:
        # 将ship_lifes减1
        status.ship_lifes -= 1
        aliens.empty()
        bullets.empty()
        sleep(1)
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
    else:
        status.game_active = False

def game_over():
    Tk().wm_withdraw()
    if messagebox.askyesno('Game Over!','是否要重新开始？'):
        ai.run_game()
    else:
        sys.exit()

def update_ship_lifes(status):
    for i in range(status.ship_lifes):
        if status.rect.x > (status.ship_lifes * 2 * status.rect.width):
            status.rect.x = 10
        status.display_life()
        status.rect.x += (2*status.rect.width)