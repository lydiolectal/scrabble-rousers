from src.coord import Coord

# stores a start position and the template associated with it.
class StartSequence:

    # points only for Ai to choose optimal play
    def __init__(self, x, y, template, ish, points = 0):
        self.x = x
        self.y = y
        self.template = template
        self.ish = ish
        self.points = points

    # compare based on points for now
    def __eq__(self, other):
        return self.points == other.points

    def __ne__(self, other):
        return self.points != other.points

    def __lt__(self, other):
        return self.points < other.points

    def __le__(self, other):
        return self.points <= other.points

    def __gt__(self, other):
        return self.points > other.points

    def __ge__(self, other):
        return self.points >= other.points
