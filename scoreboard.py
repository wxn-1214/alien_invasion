import json

import pygame.font
from pygame.sprite import Group
from ship import Ship


class ScoreBoard:
    """显示得分信息的类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化相关属性"""
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats

        # 显示得分时的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont('calibri', 48)

        # 准备包含最高和当前得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)  # py2中需要调用int(round())
        high_score_str = "{:,}".format(high_score)  # 使用逗号来指出你要添加千位分隔符
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color,
                                                 self.ai_settings.background_color)
        # 将最高得分放在屏幕之间
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.right = self.screen_rect.right - 20
        self.high_score_image_rect.top = 20

    def prep_score(self):
        """将得分转换为一副渲染的图像"""
        # 函数round()通常让小数精确到小数点后多少位,其中小数位数是由第二个实参指定的
        # 如果将第二个实参指定为负数,round()将圆整到最近的10、100、1000等整数倍
        rounded_score = round(self.stats.score, -1)  # py2中需要调用int(round())
        score_str = "{:,}".format(rounded_score)  # 使用逗号来指出你要添加千位分隔符
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.ai_settings.background_color)

        # 将得分放在屏幕右上角
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.centerx
        self.score_image_rect.top = 20

    def show_score(self):
        """显示分数"""
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)

    def prep_level(self):
        """将等级转化为渲染的图片"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color,
                                            self.ai_settings.background_color)
        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.high_score_image_rect.right
        self.level_rect.top = self.high_score_image_rect.bottom + 10

    def show_level(self):
        """显示等级"""
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_ships(self):
        """显示还剩下多少飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

