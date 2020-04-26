# game.py


class Game:
    def __init__(self, window):
        self.window = window
        self.canvas_size = (800, 800)

    # redraws any changes made in update
    def draw(self):
        pass

    # updates logic like player location
    def update(self):
        pass

    def set_canvas_size(self, size):
        self.canvas_size = size
