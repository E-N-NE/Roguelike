from constants import Constants

class Mapper:

    def __init__(self):
        pass

    @staticmethod
    def visual_icon(x, y, visibility):
        if visibility > 0:
            return Constants.icons['unknown']
        elif mob_is_at(x, y):
            return icon_of_mob_at(x, y)
        elif item_is_at(x, y):
            return icon_of_item_at(x, y)
        else:
            return Constants.icons['nothing']

    @staticmethod
    def draw_map(ROS, x, y):
