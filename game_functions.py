import json
import sys
from time import sleep

import pygame
from alien import Alien
from bullet import Bullet


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.moving_top = True
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.moving_bottom = True
    elif event.key == pygame.K_SPACE:
        # ship.firing_bullets = True
        # 创建一颗子弹并加入到Bullets编组中
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()  # 退出游戏


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = False
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.moving_top = False
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.moving_bottom = False
    # elif event.key == pygame.K_SPACE:
    # ship.firing_bullets = False


def check_events(ai_settings, aliens, bullets, screen, ship, stats,
                 play_button, sb):
    # 添加形参bullets
    """响应按键和鼠标事件"""
    for event in pygame.event.get():  # 访问pygame检测到的事件
        if event.type == pygame.QUIT:
            sys.exit()  # 退出游戏
        elif event.type == pygame.KEYDOWN:  # 按下键
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:  # 松开键
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # pygame.mouse.get_pos()返回一个元组.其中包含玩家单击时鼠标的x和y坐标
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, aliens, bullets, screen, ship, stats,
                              play_button, mouse_x, mouse_y, sb)
        """# 实现全屏(尚不成熟)
        elif event.type == pygame.RESIZABLE:
            ai_settings.size = pygame.display.list_modes()[0]
            screen = pygame.display.set_mode(
                    ai_settings.size, pygame.FULLSCREEN | pygame.HWSURFACE)
            update_screen(ai_settings, screen, ship, aliens, bullets)
        """


def check_play_button(ai_settings, aliens, bullets, screen, ship, stats,
                      play_button, mouse_x, mouse_y, sb):
    """在玩家单击Play按钮时开始新游戏"""
    # collidepoint()检查鼠标单击位置是否在Play按钮的rect 内
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # 仅当玩家单击了Play按钮且游戏当前处于非活动状态时,游戏才重新开始
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)  # 隐藏光标
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 重置得分和等级
        sb.prep_ships()
        sb.prep_high_score()
        sb.prep_score()
        sb.prep_level()
        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人并将新飞船放在屏幕中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():  # 使用方法copy()来设置for循环，这能够在循环中修改bullets(?)
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))
    check_bullet_alien_collisions(ai_settings, screen, ship, bullets, aliens,
                                  stats, sb)


def check_bullet_alien_collisions(ai_settings, screen, ship, bullets, aliens,
                                  stats, sb):
    """方法sprite.groupcollide()将每颗子弹的rect同每个外星人的rect进行比较，
    并返回一个字典，其中包含发生了碰撞的子弹和外星人。
    在这个字典中，每个键都是一颗子弹，而相应的值都是被击中的外星人
    第14章实现记分系统时，也会用到这个字典
    
    这行代码遍历编组bullets中的每颗子弹，再遍历编组aliens中的每个外星人。
    每当有子弹和外星人的rect重叠时，groupcollide()就在它返回的字典中添加一个键-值对。
    两个实参True告诉Pygame删除发生碰撞的子弹和外星人。
    (要模拟能够穿行到屏幕顶端的高能子弹——消灭它击中的每个外星人，
    可将第一个布尔实参设置为False，并让第二个布尔实参为True。
    这样被击中的外星人将消失，但所有的子弹都始终有效，直到抵达屏幕顶端后消失。）"""
    # 检查是否击中了外星人；如果是，同时删除外星人和子弹
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        # 在check_bullet_alien_collisions()中,与外星人碰撞的子弹都是字典collisions中的一个键
        # 而与每颗子弹相关的值都是一个列表,其中包含该子弹撞到的外星人。
        # 我们遍历字典collisions,确保将消灭的每个外星人的点数都记入得分
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1  # 提高等级
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    filename = r'D:/pycharm/alien_invasion/high_score.json'
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
    with open(filename, 'w') as f_obj:
        json.dump(stats.high_score, f_obj)


def show_high_score(stats, sb):
    filename = r'D:/pycharm/alien_invasion/high_score.json'
    if filename:
        with open(filename) as f_obj:
            stats.high_score = json.load(f_obj)
        sb.prep_high_score()


def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有到达限制，就发射一颗子弹"""
    # 创建新子弹，并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人来获取每行可容纳外星人的个数
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_aliens_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):  # range(5)是0、1、2、3、4
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    # 使用下面这句代码中无alien.x，会导致外星人移动时一行只显示一个外星人
    # alien.rect.x = alien.rect.width + 2 * alien.rect.width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_aliens_number_aliens_x(ai_settings, alien_width):
    """计算一行可以放多少个外星人，外星人间距为外星人宽度"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算可以容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - 3 * alien_height -
                         ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def check_fleet_edges(ai_settings, aliens):
    """外星人到达边缘后的动作"""
    for alien in aliens.sprites():  # ?
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将外星人整体下移并改变移动分向"""
    for alien in aliens.sprites():  # ?
        alien.rect.y += ai_settings.drop_fleet_factor  # 下移
    ai_settings.fleet_direction *= -1  # 调整方向


def ship_hit(ai_settings, stats, screen, bullets, aliens, ship, sb):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()  # 更新记分牌
        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人并将新飞船放在屏幕中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)  # 暂停
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """检测是否有外星人到达屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 处理和飞船被撞到一样
            ship_hit(ai_settings, stats, screen, bullets, aliens, ship, sb)
            break


def update_aliens(ai_settings, stats, screen, bullets, aliens, ship, sb):
    """检测是否有外星人在屏幕边缘并更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测飞船和外星人碰撞
    if pygame.sprite.spritecollideany(ship, aliens):  # 两个实参：前者为编组，后者为精灵
        ship_hit(ai_settings, stats, screen, bullets, aliens, ship, sb)
        # print('Ship hit!!!')

    # 检测外星人是否到底部
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)


def update_screen(ai_settings, screen, stats, ship, aliens, bullets,
                  play_button, sb):  #
    # 添加形参bullets
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环都重绘屏幕
    screen.fill(ai_settings.background_color)  # 调用fill()方法，用背景色填充屏幕
    # 在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blit_me()  # 绘制飞船
    # alien.blit_me()  # 绘制外星人
    aliens.draw(screen)  # 在屏幕上绘制编组的每个外星人，代码：精灵组.draw()
    sb.show_score()
    sb.show_level()
    if not stats.game_active:
        play_button.draw_button()
    # 让绘制的屏幕可见
    pygame.display.flip()  # 令pygame让最近绘制的屏幕可见，并擦除旧屏幕
