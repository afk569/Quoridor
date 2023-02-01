import pygame as pg
import Functions
import copy

SIZE = 504
EXTRA_HEIGHT = 126
DIMENSION = 9
SQ_SIZE = SIZE // DIMENSION


class GameState():
    def __init__(self):
        # Board is an 9x9 graph  -> columns represented by letters for left to right (a-i) and rows by numbers (1-9)
        # each node has its adiacent nodes edges
        self.board = {'a1': {'b1', 'a2'}, 'b1': {'c1', 'b2', 'a1'}, 'c1': {'c2', 'd1', 'b1'}, 'd1': {'e1', 'c1', 'd2'},
                      'e1': {'f1', 'd1', 'e2'}, 'f1': {'e1', 'f2', 'g1'}, 'g1': {'h1', 'g2', 'f1'},
                      'h1': {'g1', 'h2', 'i1'},
                      'i1': {'h1', 'i2'}, 'a2': {'a1', 'a3', 'b2'}, 'b2': {'c2', 'b1', 'a2', 'b3'},
                      'c2': {'c1', 'c3', 'd2', 'b2'},
                      'd2': {'c2', 'd1', 'e2', 'd3'}, 'e2': {'f2', 'e3', 'd2', 'e1'}, 'f2': {'g2', 'f1', 'e2', 'f3'},
                      'g2': {'f2', 'g1', 'g3', 'h2'}, 'h2': {'h3', 'g2', 'h1', 'i2'}, 'i2': {'i3', 'h2', 'i1'},
                      'a3': {'a4', 'a2', 'b3'}, 'b3': {'a3', 'c3', 'b4', 'b2'}, 'c3': {'c2', 'd3', 'c4', 'b3'},
                      'd3': {'e3', 'c3', 'd4', 'd2'}, 'e3': {'e4', 'e2', 'f3', 'd3'}, 'f3': {'g3', 'f2', 'e3', 'f4'},
                      'g3': {'h3', 'g2', 'g4', 'f3'}, 'h3': {'i3', 'h2', 'g3', 'h4'}, 'i3': {'h3', 'i2', 'i4'},
                      'a4': {'a3', 'a5', 'b4'}, 'b4': {'a4', 'c4', 'b3', 'b5'}, 'c4': {'c3', 'b4', 'd4', 'c5'},
                      'd4': {'e4', 'd3', 'c4', 'd5'}, 'e4': {'e5', 'e3', 'd4', 'f4'}, 'f4': {'f5', 'e4', 'g4', 'f3'},
                      'g4': {'g3', 'g5', 'f4', 'h4'}, 'h4': {'i4', 'h3', 'g4', 'h5'}, 'i4': {'i3', 'i5', 'h4'},
                      'a5': {'a4', 'b5', 'a6'}, 'b5': {'a5', 'b4', 'c5', 'b6'}, 'c5': {'b5', 'c4', 'c6', 'd5'},
                      'd5': {'e5', 'd4', 'c5', 'd6'}, 'e5': {'f5', 'e4', 'e6', 'd5'}, 'f5': {'e5', 'f6', 'g5', 'f4'},
                      'g5': {'f5', 'g6', 'g4', 'h5'}, 'h5': {'g5', 'i5', 'h6', 'h4'}, 'i5': {'i4', 'i6', 'h5'},
                      'a6': {'a7', 'a5', 'b6'}, 'b6': {'b7', 'b5', 'c6', 'a6'}, 'c6': {'d6', 'c7', 'c5', 'b6'},
                      'd6': {'c6', 'd7', 'e6', 'd5'}, 'e6': {'e5', 'f6', 'e7', 'd6'}, 'f6': {'f5', 'g6', 'e6', 'f7'},
                      'g6': {'f6', 'g5', 'h6', 'g7'}, 'h6': {'i6', 'g6', 'h7', 'h5'}, 'i6': {'i7', 'i5', 'h6'},
                      'a7': {'b7', 'a8', 'a6'}, 'b7': {'a7', 'b8', 'c7', 'b6'}, 'c7': {'b7', 'c8', 'd7', 'c6'},
                      'd7': {'d6', 'd8', 'c7', 'e7'}, 'e7': {'e6', 'd7', 'e8', 'f7'}, 'f7': {'g7', 'f6', 'f8', 'e7'},
                      'g7': {'g8', 'g6', 'h7', 'f7'}, 'h7': {'i7', 'h8', 'h6', 'g7'}, 'i7': {'i6', 'i8', 'h7'},
                      'a8': {'a7', 'a9', 'b8'}, 'b8': {'b7', 'a8', 'c8', 'b9'}, 'c8': {'b8', 'd8', 'c7', 'c9'},
                      'd8': {'d7', 'c8', 'e8', 'd9'}, 'e8': {'f8', 'd8', 'e9', 'e7'}, 'f8': {'g8', 'f9', 'e8', 'f7'},
                      'g8': {'g7', 'g9', 'f8', 'h8'}, 'h8': {'g8', 'h9', 'h7', 'i8'}, 'i8': {'i7', 'h8', 'i9'},
                      'a9': {'a8', 'b9'},
                      'b9': {'a9', 'b8', 'c9'}, 'c9': {'c8', 'd9', 'b9'}, 'd9': {'d8', 'e9', 'c9'},
                      'e9': {'f9', 'e8', 'd9'},
                      'f9': {'f8', 'g9', 'e9'}, 'g9': {'g8', 'f9', 'h9'}, 'h9': {'g9', 'i9', 'h8'}, 'i9': {'i8', 'h9'}}
        self.board_positions = self.getBoardPositions()  # array of squares with thier positions
        self.board_squares = self.getBoardSquares()  # array of positions with thier squares
        self.log = []
        self.hor_walls = []  # list of STARTING squares there is a horizontalwall
        self.ver_walls = []  # list of STARTING squares there is a verticalwall
        self.walls = []  # list of squares there is a wall
        self.p1_to_win = ["a9", "b9", "c9", "d9", "e9", "f9", "g9", "h9", "i9"]
        self.p2_to_win = ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1", "i1"]
        self.possible_hor_build, self.possible_ver_build = self.possibleBuilds()  # len of 64 each list of builds

    def possibleBuilds(self):
        horBuild = []
        verBuild = []
        ranks_to_rows = {"1": 8, "2": 7, "3": 6, "4": 5, "5": 4, "6": 3, "7": 2, "8": 1, "9": 0}
        rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
        files_to_cols = ranks_to_rows = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8}
        cols_to_files = {v: k for k, v in files_to_cols.items()}

        for r in range(1, 9):
            for c in range(0, 8):
                sq = cols_to_files[c] + rows_to_ranks[r]
                w = Wall("horizontal")
                w.pos = sq
                w.real_pos = self.board_positions[sq]
                horBuild.append(Build(cols_to_files[c] + rows_to_ranks[r], w))
        for r in range(0, 8):
            for c in range(1, 9):
                sq = cols_to_files[c] + rows_to_ranks[r]
                w = Wall("vertical")
                w.pos = sq
                w.real_pos = self.board_positions[sq]
                verBuild.append(Build(cols_to_files[c] + rows_to_ranks[r], w))
        return horBuild, verBuild

    def getBoardPositions(self):
        real_pos = {}
        counter = 0
        for i, item in enumerate(self.board):
            if i % DIMENSION == 0:
                counter += 1
            real_pos[item] = [SQ_SIZE * (i % DIMENSION), SIZE - SQ_SIZE * counter]
        return real_pos

    def getBoardSquares(self):
        real_sq = {}
        counter = 0
        for i, item in enumerate(self.board):
            if i % DIMENSION == 0:
                counter += 1
            real_sq[str([SQ_SIZE * (i % DIMENSION), SIZE - SQ_SIZE * counter])] = item
        return real_sq

    def makeMove(self, players, p1_to_move, move):  # return swap player
        # print(move)
        player = players[1 - p1_to_move]
        if move.moved_to in self.getValidMoves(players, p1_to_move):
            player.pos = move.moved_to
            print(move.getNotation())  # doc moves
            self.log.append(move)
            return not p1_to_move
        return p1_to_move  # if not valid, do nothing

    def getValidMoves(self, players, p1_to_move):  # without jumping
        player = players[1 - p1_to_move]
        other_player_pos = players[p1_to_move].pos  # opponent pos
        moves = self.jumpSq(player.pos, other_player_pos)
        if other_player_pos in moves:
            moves.remove(other_player_pos)
        return moves

    def jumpSq(self, p1, p2):  # p1 try to move
        moves = self.board[p1].copy()
        if p2 in moves:
            if p1[0] == p2[0] and int(p1[1]) == int(p2[1]) - 1:  # we go upwards
                p2_moves = self.board[p2].copy()
                if p1[0] + str(int(p1[1]) + 2) in p2_moves:  # if upwards is not blocked
                    moves.remove(p2)
                    moves.add(p1[0] + str(int(p1[1]) + 2))
                else:  # upwards is blocked
                    # print(p2_moves, p1)
                    p2_moves.remove(p1)
                    for move in p2_moves:
                        moves.add(move)
            elif p1[0] == p2[0] and int(p1[1]) == int(p2[1]) + 1:  # we go downwards
                p2_moves = self.board[p2].copy()
                if p1[0] + str(int(p1[1]) - 2) in p2_moves:  # if upwards is not blocked
                    moves.remove(p2)
                    moves.add(p1[0] + str(int(p1[1]) - 2))
                else:  # downwards is blocked
                    # print(p2_moves, p1)
                    p2_moves.remove(p1)
                    for move in p2_moves:
                        moves.add(move)
            elif chr(ord(p1[0]) + 1) == p2[0] and p1[1] == p2[1]:  # we go right
                p2_moves = self.board[p2].copy()
                if chr(ord(p1[0]) + 2) + p1[1] in p2_moves:  # if right is not blocked
                    moves.remove(p2)
                    moves.add(chr(ord(p1[0]) + 2) + p1[1])
                else:  # right is blocked
                    # print(p2_moves, p1)
                    p2_moves.remove(p1)
                    for move in p2_moves:
                        moves.add(move)
            elif chr(ord(p1[0]) - 1) == p2[0] and p1[1] == p2[1]:  # we go left
                p2_moves = self.board[p2].copy()
                if chr(ord(p1[0]) - 2) + p1[1] in p2_moves:  # if right is not blocked
                    moves.remove(p2)
                    moves.add(chr(ord(p1[0]) - 2) + p1[1])
                else:  # left is blocked
                    # print(p2_moves, p1)
                    p2_moves.remove(p1)
                    for move in p2_moves:
                        moves.add(move)
        return moves

    def getValidBuildsHorizontal(self, players):
        arr = []
        for i in self.possible_hor_build:
            if self.canBuild(i, players):
                arr.append(i)
        return arr

    def getValidBuildsVertical(self, players):
        arr = []
        for i in self.possible_ver_build:
            if self.canBuild(i, players):
                arr.append(i)
        return arr

    def getValidBuilds(self, players):
        arr = []
        arr.append(self.getValidBuildsVertical(players))
        arr.append(self.getValidBuildsHorizontal(players))
        return arr

    def makeBuild(self, players, p1_to_move, build):
        player = players[1 - p1_to_move]
        if player.walls <= 0:
            return p1_to_move, None
        if self.canBuild(build, players, True):
            player.walls -= 1
            self.walls.append(build.build_at1)
            self.walls.append(build.build_at2)
            if build.wall.axis == "horizontal":
                self.hor_walls.append(build.build_at1)
            else:
                self.ver_walls.append(build.build_at1)
            print(build.getNotation())  # doc moves
            self.log.append(build)
            return not p1_to_move, build.wall
        # print(self.board)
        return p1_to_move, None

    def canBuild(self, build, players, delete=False):

        temp = copy.deepcopy(self.board)
        axis = build.wall.axis
        sq1 = build.build_at1
        sq2 = build.build_at2
        if axis == "horizontal":
            if sq1 in self.hor_walls or sq2 in self.hor_walls or chr(ord(sq1[0]) - 1) + sq1[1] \
                    in self.hor_walls or sq2[0] + str(int(sq1[1]) + 1) in self.ver_walls:
                return False
            temp[sq1].remove(sq1[0] + str(int(sq1[1]) + 1))
            temp[sq1[0] + str(int(sq1[1]) + 1)].remove(sq1)
            temp[sq2].remove(sq2[0] + str(int(sq2[1]) + 1))
            temp[sq2[0] + str(int(sq2[1]) + 1)].remove(sq2)
            if Functions.BFS_SP(temp, players[0].pos, self.p1_to_win) and Functions.BFS_SP(temp, players[1].pos,
                                                                                           self.p2_to_win):
                if delete:
                    self.board = temp  # delete connections
                return True
            else:

                return False
        else:  # Vertical
            if sq1 in self.ver_walls or sq2 in self.ver_walls or sq1[0] + str(int(sq1[1]) + 1) in self.ver_walls or chr(
                    ord(sq2[0]) - 1) + sq2[1] in self.hor_walls:
                return False
            temp[sq1].remove(chr(ord(sq1[0]) - 1) + sq1[1])
            temp[chr(ord(sq1[0]) - 1) + sq1[1]].remove(sq1)
            temp[sq2].remove(chr(ord(sq2[0]) - 1) + sq2[1])
            temp[chr(ord(sq2[0]) - 1) + sq2[1]].remove(sq2)
            if Functions.BFS_SP(temp, players[0].pos, self.p1_to_win) and Functions.BFS_SP(temp, players[1].pos,
                                                                                           self.p2_to_win):
                if delete:
                    self.board = temp  # delete connections
                return True
        # self.temp = self.board  # restore connections
        return False


class Wall():
    def __init__(self, axis='horizontal'):
        self.axis = axis
        self.pos = "a1"
        self.real_pos = (SIZE * 2 / 3 + 2, SIZE + EXTRA_HEIGHT / 2 - 5) if axis == 'horizontal' \
            else (SIZE / 3 - SQ_SIZE - 5, SIZE + EXTRA_HEIGHT / 2 - SQ_SIZE + 2)
        self.img = pg.image.load("horizontal_wall.png") if axis == 'horizontal' else pg.image.load("vertical_wall.png")
        # 108 x 11 img
        #  when blit the wall, need adjustments to be in the middle
        #  screen.blit(pos + 2,pos - 5) # horizontal
        #  screen.blit(p2.img, (pos - 5,pos + 2) # vertical

    def sqPos(self):
        return self.pos

class Player():
    def __init__(self, turn='p1'):
        self.turn = turn
        self.walls = 10
        self.pos = 'e1' if turn == 'p1' else 'e9'
        self.img = pg.image.load("p1.png") if turn == 'p1' else pg.image.load("p2.png")
        self.img = pg.transform.scale(self.img, (SQ_SIZE, SQ_SIZE))


class Build():
    # maps boarder to notation (keys : value)
    ranks_to_rows = {"1": 8, "2": 7, "3": 6, "4": 5, "5": 4, "6": 3, "7": 2, "8": 1, "9": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = ranks_to_rows = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, end_sq, wall):
        # self.player = players[1 - p1_to_move]
        # self.players = players
        self.wall = wall
        self.build_at1 = end_sq
        if self.wall.axis == 'horizontal':
            self.build_at2 = chr(ord(self.build_at1[0]) + 1) + self.build_at1[1]
        else:
            self.build_at2 = self.build_at1[0] + str(int(self.build_at1[1]) - 1)

    def getNotation(self):
        return str(self.build_at1) + str(self.build_at2)


class Move():
    # maps boarder to notation (keys : value)
    ranks_to_rows = {"0": 9, "1": 8, "2": 7, "3": 6, "4": 5, "5": 4, "6": 3, "7": 2, "8": 1, "9": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, end_sq, p1_to_move, players, bot=False):  # gets start and end mouse pos
        self.player = players[1 - p1_to_move]
        self.other_player = players[p1_to_move]
        self.start_row, self.start_col = self.player.pos
        self.end_row, self.end_col = end_sq[0], end_sq[1]
        self.moved_from = self.player.pos
        if bot:
            self.moved_to = end_sq
        else:
            self.moved_to = str(self.cols_to_files[self.end_col]) + self.rows_to_ranks[self.end_row]

    def getNotation(self):
        return self.player.turn + ". " + self.moved_from + " -> " + self.moved_to
