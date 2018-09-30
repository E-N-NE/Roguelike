class World:

    @classmethod
    def create_new_stage(cls, connections, stage_info, generator):
        return cls.Stage(connections, stage_info, generator)

    class Generator:

        def __init__(self, goers):
            self.goers = goers

    class StageInfo:

        def __init__(self, height, width):
            self.height = height
            self.width = width

    class Stage:

        def __init__(self, connections, stage_info, generator):

