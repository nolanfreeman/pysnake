# entity.py

class Entity:
    def __init__(self, pos=(0,0), dim=(0,0)): # TODO set default pos to be random, dim to be default entity size,
        self.posx, self.posy = pos
        self.width, self.height = dim

