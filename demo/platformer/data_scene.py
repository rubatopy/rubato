from rubato import Scene


class DataScene(Scene):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level_size = 0
