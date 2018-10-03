from basic_functions import d, r


class World:

    @classmethod
    def create_new_stage(cls, connections, stage_info, generator):
        return cls.Stage(connections, stage_info, generator)

    class Pattern:

        def __init__(self, contents=(('.',),), width=1, height=1):
            self.contents = contents
            self.width = width
            self.height = height
            assert height == len(contents),\
                "Pattern creation failed, size_y mismatch."
            assert width == len(contents[0]),\
                "Pattern creation failed, size_x mismatch."
            if __debug__:
                for i in range(len(contents) - 1):
                    assert len(contents[i]) == len(contents[i+1]),\
                        "Pattern creation failed, lengths mismatch."

        def intake(self, start_x, start_y, pattern):
            for i in range(pattern.size_x):
                for j in range(pattern.size_y):
                    if '?' not in pattern[i][j]:
                        self.contents[start_x+i][start_y+j] = pattern[i][j]

    class Divergence:

        def __init__(self, randomizer, probability):
            self.randomizer = randomizer
            self.probability = probability
            assert 0.0 <= probability <= 1.0,\
                "Incorrect probability, {}.".format(probability)

    class Movement:

        def __init__(self, count, direction, divergence):
            self.count = count
            self.direction = direction
            self.divergence = divergence
            assert len(direction) == 2,\
                "Incorrect direction, {}.".format(direction)

    class Generator:

        def __init__(self, count, pattern, movement):
            self.count = count
            self.pattern = pattern
            self.movement = movement

        def modify(self, stage):
            rightmost = stage.width - self.pattern.width
            downmost = stage.height - self.pattern.height
            for i in range(self.count):
                pos_x = d(rightmost + 1) - 1
                pos_y = d(downmost + 1) - 1
                for j in range(self.movement.count):
                    if rightmost >= pos_x >= 0 and rightmost >= pos_y >= 0:
                        stage.contents.intake(pos_x, pos_y, self.pattern)
                    else:
                        break
                    if r(self.movement.divergence.probability):
                        move = self.movement.divergence.randomizer()
                    else:
                        move = self.movement.direction
                    pos_x += move[0]
                    pos_y += move[1]

    class StageInfo:

        def __init__(self, height, width, mobs, template):
            self.height = height
            self.width = width
            self.mobs = mobs
            self.template = template  # Pattern class.

    class Stage:

        def __init__(self, connections, stage_info, generators):
            self.contents = stage_info.template
            for generator in generators:
                generator.modify(self.contents)

