import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置"""
        super().__init__()
        self.screen = screen
        self.ai_setting = ai_settings

        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load(
            r'D:/pycharm/alien_invasion/images/ship.bmp')
        # 使用get_rect()获取属性rect(矩形为rect对象)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        """
           在pygame中，(0,0)位于屏幕左上角
           在1200x600屏幕上,右下角的坐标为(1200,600)
           使用center、centerx、centery来表示居中
           使用top、bottom、left、right表示上下左右
        """
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中添加小数值
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_top = False
        self.moving_bottom = False
        # self.firing_bullets = False

    def update(self):
        """根据移动标志调整飞船位置"""
        # 更新飞船的center值，而不是rect
        # self.rect.right返回飞船外接矩形的右边缘x坐标
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_setting.ship_speed_factor
        # self.rect.left返回飞船外接矩形的左边缘x坐标
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.centerx -= self.ai_setting.ship_speed_factor
        # self.rect.top返回飞船外接矩形的上边缘y坐标
        if self.moving_top and self.rect.top > self.screen_rect.top:
            self.centery -= self.ai_setting.ship_speed_factor
        # self.rect.right返回飞船外接矩形的下边缘y坐标
        if self.moving_bottom and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_setting.ship_speed_factor

        # 根据self.center更新rect对象
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    """def firing_bullet(self, ai_settings, screen, ship, bullets):
        if self.firing_bullets:
            # 创建一颗子弹并加入到Bullets编组中
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)"""

    def blit_me(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # 让飞船在屏幕上居中
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.rect.bottom = self.screen_rect.bottom

        # 在飞船的属性center中添加小数值
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
