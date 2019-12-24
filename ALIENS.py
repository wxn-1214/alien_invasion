import pygame
import sys  # 玩家退出时，使用sys模块来退出游戏
from settings import Settings  # 调用设置类
from ship import Ship  # 调用飞船类
from alien import Alien  # 调用外星人类
import game_functions as gf
from pygame.sprite import Group  # pygame.sprite.Group类 类似于列表，但提供了有助于开发游戏的额外功能
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


def run_game():
    """初始化游戏并创建一个屏幕对象"""
    # 初始化pygame、背景设置、屏幕对象
    pygame.init()
    """
       对象screen是一个surface
       在Pygame中，surface是屏幕的一部分，用于显示游戏元素
       在这个游戏中，每个元素（如外星人或飞船）都是一个surface
       display.set_mode()返回的surface表示整个游戏窗口
       我们激活游戏的动画循环后，每经过一次循环都将自动重绘这个surface
       调用pygame.display.set_mode()创建一个名为screen的窗口，游戏的图形元素都在其中绘制
       实参(1200, 600)元组指定了窗口宽1200像素，高600像素(改调用settings类)
    """
    ai_settings = Settings()
    screen = pygame.display.set_mode(ai_settings.size, pygame.RESIZABLE)
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, 'Play')
    # 创建统计游戏数据的实例以及得分
    stats = GameStats(ai_settings)
    sb = ScoreBoard(ai_settings, screen, stats)
    # 创建建一艘飞船、一个子弹编组和一个外星人编组
    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    bullets = Group()  # 创建一个用于存储子弹和外星人的编组
    aliens = Group()  # 这个编组将是pygame.sprite.Group类的一个实例
    # 创建一个外星人
    # alien = Alien(ai_settings, screen)
    gf.create_fleet(ai_settings, screen, ship, aliens)  # 创建外星人群

    # 设置背景颜色
    # background_color = (102, 204, 255)  # 66ccff天蓝色
    # 开始游戏的主循环
    while 1:
        # 监视键盘和鼠标事件
        gf.check_events(ai_settings, aliens, bullets, screen, ship, stats,
                        play_button, sb)
        # ship.firing_bullet(ai_settings, screen, ship, bullets)
        gf.show_high_score(stats, sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets,
                              stats, sb)
            gf.update_aliens(ai_settings, stats, screen, bullets, aliens,
                             ship, sb)
            # print(len(aliens))
        # 每次循环都重绘屏幕
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets,
                         play_button, sb)


run_game()
