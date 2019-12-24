import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """一个对飞船发射子弹进行管理的类"""
    def __init__(self, ai_settings, screen, ship):
        """在飞船所处的位置创建一个子弹对象"""
        super().__init__()
        self.screen = screen

        # 在(0,0)创建一个表示子弹的矩形，再设置正确的位置
        # 创建了子弹的属性rect
        # 子弹并非基于图像的，因此我们必须使用pygame.Rect() 类从空白开始创建一个矩形
        # 子弹的初始位置取决于飞船当前的位置,子弹的宽度和高度是从ai_settings 中获取的
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                ai_settings.bullet_height)

        # 将子弹的centerx 设置为飞船的rect.centerx
        self.rect.centerx = ship.rect.centerx
        # 子弹应从飞船顶部射出，将表示子弹的rect的top属性设置为飞船的rect的top属性，让子弹看起来像是从飞船中射出的
        self.rect.top = ship.rect.top

        # 存储小数表示的子弹位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹"""
        # 更新 小数值(表示子弹位置)
        self.y -= self.speed_factor
        # 更新 rect(子弹)位置
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        # draw.rect():使用存储在self.color中的颜色填充表示子弹的rect占据的屏幕部分
        pygame.draw.rect(self.screen, self.color, self.rect)

