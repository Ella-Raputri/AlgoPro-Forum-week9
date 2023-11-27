class GameStats():
    "Track statistic for alien invasion"

    def __init__(self, ai_settings):
        #initialize
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0
     
    def reset_stats(self):
        #initialize stats that can change during game
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
    
    