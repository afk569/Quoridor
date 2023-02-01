import pygame as pg
import QuoridorEngine
import math
import time
import Bot

WIDTH = HEIGHT = 504
EXTRA_HEIGHT = 126
PRECISION = 15  # how precise you need to be to place the wall, smaller means more precise
DIMENSION = 9
SQ_SIZE = HEIGHT // 9
MAX_FPS = 30
IMAGES = []
pg.font.init()
STAT_FONT = pg.font.SysFont("comicsans", 30)
TIME_FONT = pg.font.SysFont("comicsans", 20)


def main():
    # pygame initialize
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT + EXTRA_HEIGHT))
    screen.fill(pg.Color(pg.Color("darkorange")))
    clock = pg.time.Clock()
    start_time = time.time()

    gs = QuoridorEngine.GameState()  # Game State
    p1 = QuoridorEngine.Player("p1")
    p2 = QuoridorEngine.Player("p2")
    p1_time = 5 * 60  # secs
    p2_time = 5 * 60
    players = [p1, p2]
    wall_hor = QuoridorEngine.Wall("horizontal")  # init walls
    wall_ver = QuoridorEngine.Wall("vertical")  # init walls
    walls_init = [wall_hor, wall_ver]
    walls = []  # list of walls positions
    nearest_sq = (0, 0)
    location = (0, 0)  # mouse locations
    place_wall = wall_hor  # initialize what wall are we trying to place
    try_to_build = False  # a state the player is in. true if player tries to build
    running = True  # game loop
    p1_to_move = True  # p1 turn
    
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.MOUSEMOTION:
                location = pg.mouse.get_pos()  # (x,y) location of the mouse
            if e.type == pg.MOUSEBUTTONDOWN:
                # print([b.getNotation() for b in gs.getValidBuilds(players)])
                print(len(gs.getValidBuilds(players)))
                col = location[0] // SQ_SIZE  # to what column I want to move
                row = location[1] // SQ_SIZE  # to what row I want to move
                if location[1] < HEIGHT and try_to_build is False:  # we try to move our player
                    move = QuoridorEngine.Move((row, col), p1_to_move, players)
                    if p1_to_move:
                        p1_to_move = gs.makeMove(players, p1_to_move, move)
                    else:
                        p1_to_move = gs.makeMove(players, p1_to_move, move)
                if location[1] < HEIGHT and try_to_build is True:  # we try to place wall
                    nearest_sq_pos = find_nearest_sq_pos(location)  # pos
                    try:  # try to find nearest square
                        nearest_sq = find_nearest_sq(location, gs)  # sq
                        if place_wall.axis == 'horizontal':
                            if nearest_sq[0] == 'i' or nearest_sq[1] == '9':  # walls outside the board
                                try_to_build = False
                        else:
                            if nearest_sq[1] == '1':  # walls outside the board
                                try_to_build = False

                    except:  # nearest square is outside the board square
                        try_to_build = False
                    if try_to_build and distance(location, (nearest_sq_pos[0], nearest_sq_pos[1])) < PRECISION:
                        place_wall.pos = nearest_sq
                        place_wall.real_pos = nearest_sq_pos
                        build = QuoridorEngine.Build(nearest_sq, place_wall)
                        p1_to_move, add_wall = gs.makeBuild(players, p1_to_move, build)
                        if add_wall:
                            walls.append(add_wall)
                    try_to_build = False
                elif chooseHorizontalWall(location, wall_hor):  # we choose horizontal wall
                    try_to_build = not try_to_build  # enter building state
                    if try_to_build:
                        place_wall = QuoridorEngine.Wall("horizontal")  # the wall we want to place
                elif chooseVerticalWall(location, wall_ver):  # we choose horizontal wall
                    try_to_build = not try_to_build  # enter building state
                    if try_to_build:
                        place_wall = QuoridorEngine.Wall("vertical")  # the wall we want to place
        if p1.pos in gs.p1_to_win or p2_time < 0:
            running = False
            print("player 1 won")
        if p2.pos in gs.p2_to_win or p1_time < 0:
            running = False
            print("player 2 won")
        clock.tick(MAX_FPS)
        if p1_to_move:
            p1_time -= time.time() - start_time
        else:
            p2_time -= time.time() - start_time
        start_time = time.time()
        drawGameState(screen, gs, p1, p2, p1_to_move, walls, walls_init)
        drawTime(screen, int(p1_time), int(p2_time))
        if try_to_build:
            drawWallOnMouse(screen, place_wall, location)
        pg.display.flip()


def drawGameState(screen, gs, p1, p2, p1_to_move, walls, walls_init):
    drawBoard(screen)  # draw squares on the board
    drawPlayerValidMoves(screen, gs, p1, p2, p1_to_move)
    drawInitWalls(screen, walls_init)
    drawWalls(screen, walls)
    drawPlayers(screen, gs, p1, p2)  # draw players on the board
    drawText(screen, p1, p2, p1_to_move)


def drawBoard(screen):
    pg.draw.rect(screen, pg.Color("darkorange"), pg.Rect(0, 0, WIDTH, HEIGHT))
    # pg.draw.rect(screen, pg.Color("lightblue"), pg.Rect(0, 0, WIDTH, SQ_SIZE))
    black = pg.Color("black")
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            pg.draw.rect(screen, black, pg.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE), width=3)
    pg.draw.rect(screen, black, pg.Rect(0, HEIGHT, WIDTH, EXTRA_HEIGHT))


def drawInitWalls(screen, walls):
    for wall in walls:
        screen.blit(wall.img, wall.real_pos)
    wall_hor = walls[0]
    wall_ver = walls[1]
    pg.draw.rect(screen, pg.Color("grey"), pg.Rect(wall_hor.real_pos[0] - 3, wall_ver.real_pos[1] + 30, 114, 51),
                 width=3)  # horizontal
    pg.draw.rect(screen, pg.Color("grey"), pg.Rect(wall_ver.real_pos[0] - 20, wall_ver.real_pos[1] - 3, 51, 114),
                 width=3)  # vertical


def drawWalls(screen, walls):
    for wall in walls:
        if wall.axis == "horizontal":
            screen.blit(wall.img, (wall.real_pos[0] + 2, wall.real_pos[1] - 5))
        else:
            screen.blit(wall.img, (wall.real_pos[0] - 5, wall.real_pos[1] + 2))


def drawPlayerValidMoves(screen, gs, p1, p2, p1_to_move):
    moves = gs.getValidMoves([p1, p2], p1_to_move)
    for move in moves:
        pg.draw.rect(screen, pg.Color("lightblue"),
                     pg.Rect(gs.board_positions[move][0] + 2, gs.board_positions[move][1] + 2, SQ_SIZE - 4,
                             SQ_SIZE - 4))


def drawText(screen, p1, p2, p1_to_move):
    text1 = STAT_FONT.render("White Walls: " + str(p1.walls), 1, (255, 255, 255))
    screen.blit(text1, (WIDTH / 2 - SQ_SIZE * 1.5, HEIGHT + EXTRA_HEIGHT / 2 - SQ_SIZE))
    text2 = STAT_FONT.render("Black Walls: " + str(p2.walls), 1, (255, 255, 255))
    screen.blit(text2, (WIDTH / 2 - SQ_SIZE * 1.5, HEIGHT + EXTRA_HEIGHT / 2))


def drawTime(screen, t1, t2):
    t1 = str(t1 // 60) + ":" + str(t1 % 60)
    t2 = str(t2 // 60) + ":" + str(t2 % 60)
    text1 = STAT_FONT.render("Time: " + t1, 1, (255, 255, 255))
    screen.blit(text1, (WIDTH / 2 - SQ_SIZE * 1.5, HEIGHT + EXTRA_HEIGHT / 2 - SQ_SIZE / 2 - 5))
    text2 = STAT_FONT.render("Time:  " + t2, 1, (255, 255, 255))
    screen.blit(text2, (WIDTH / 2 - SQ_SIZE * 1.5, HEIGHT + EXTRA_HEIGHT / 2 + SQ_SIZE / 2 - 5))


def find_nearest_sq_pos(pos):
    return round(pos[0] / SQ_SIZE) * SQ_SIZE, round(pos[1] / SQ_SIZE) * SQ_SIZE


def find_nearest_sq(pos, gs):
    pos = find_nearest_sq_pos(pos)
    return gs.board_squares[str([pos[0], pos[1]])]


def drawPlayers(screen, gs, p1, p2):
    gs_pos = gs.board_positions
    screen.blit(p1.img, gs_pos[p1.pos])
    screen.blit(p2.img, gs_pos[p2.pos])
    pass


def drawWallOnMouse(screen, wall, pos):
    screen.blit(wall.img, pos)


def chooseVerticalWall(location, wall):
    return wall.real_pos[0] - 20 < location[0] < wall.real_pos[0] + 11 + 20 and \
           wall.real_pos[1] - 3 < location[1] < wall.real_pos[1] + 108 + 3


def chooseHorizontalWall(location, wall):
    return wall.real_pos[0] - 3 < location[0] < wall.real_pos[0] - 3 + 114 and \
           wall.real_pos[1] - 20 < location[1] < wall.real_pos[1] - 20 + 51


def distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


if __name__ == "__main__":
    main()
