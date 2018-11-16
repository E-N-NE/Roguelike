from constants import Icons

class Mapper:

    def __init__(self, world):
        self.world = world

    def visual_icon(cls, x, y, visibility):
        if visibility <= 0:
            return Icons.UNKNOWN
        elif cls.mob_is_at(x, y):
            return cls.icon_of_mob_at(x, y)
        elif cls.furniture_is_at(x, y):
            return cls.icon_of_furniture_at(x, y)
        elif cls.item_is_at(x, y):
            return cls.icon_of_item_at(x, y)
        else:
            return Icons.NOTHING

    def draw_map(self, x, y):
