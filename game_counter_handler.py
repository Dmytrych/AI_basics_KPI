class GameCounterHandler():
    def __init__(self, food_cost):
        self.score = 0
        self.food_cost = food_cost

    def set_max_points(self, points):
        self.max_score = points
        print(points)

    def picked(self):
        self.score = self.score + self.food_cost
        print(self.score)

    def is_win(self):
        return self.score >= self.max_score
