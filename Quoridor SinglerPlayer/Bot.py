import random


class Bot():
    def __init__(self, gs, players, player):
        self.gs = gs
        self.valid_hor = gs.possible_hor_build
        # list of build objects
        # (maybe i need to change that to text aswell so it will be easier to use in algorithem which isnt random)
        self.valid_ver = gs.possible_ver_build
        # list of build objects
        # (maybe i need to change that to text aswell so it will be easier to use in algorithem which isnt random)
        self.valid_moves = gs.getValidMoves(players, player)
        # False because bot is 2nd player moves represented by Text of the square (eg: c2)
        self.walls = 10

    def validChoices(self, gs, players, player):
        self.valid_hor = gs.getValidBuildsHorizontal(players)  # list of
        self.valid_ver = gs.getValidBuildsVertical(players)
        self.valid_moves = gs.getValidMoves(players, player)

    def randomAlgo(self):  # return move or build, try_to_build
        rand = random.randint(0, 5)
        if self.walls <= 0:
            return random.choice(list(self.valid_moves)), False
        if rand < 3:
            return random.choice(list(self.valid_moves)), False
        elif rand < 4:
            self.walls -= 1
            return random.choice(self.valid_hor), True
        else:
            self.walls -= 1
            return random.choice(self.valid_ver), True
