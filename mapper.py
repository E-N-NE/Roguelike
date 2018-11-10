from constants import Icons

class Mapper:

    def __init__(self):
        pass

    @staticmethod
    def visual_icon(x, y, visibility):
        if visibility <= 0:
            return Icons.UNKNOWN
        elif mob_is_at(x, y):
            return icon_of_mob_at(x, y)
        elif item_is_at(x, y):
            return icon_of_item_at(x, y)
        else:
            return Icons.NOTHING

    @staticmethod
    def draw_map(ROS, x, y):
