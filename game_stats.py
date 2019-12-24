class GameStats:
    """跟踪游戏的统计信息"""
    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False  # 游戏刚开始处于非活动状态
        self.high_score = 0  # 不应重置

    def reset_stats(self):
        """初始化在游戏中可能变化的数据"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

