import random
import msvcrt


class G:
    board = []
    score = 0
    
    def open_slots():
        return [[x, y] for x in C.rx
                       for y in C.ry
                       if G.board[y][x] == 0]
    
    def reset():
        G.score = 0
        G.board = [[0 for i in C.rx] for j in C.ry]
        slots = G.open_slots()
        for i in range(C.sc):
            random.shuffle(slots)
            s = slots.pop()
            G.board[s[1]][s[0]] = random.choice(C.p)


class C:
    sx = 4
    rx = range(4)
    sy = 4
    ry = range(4)
    sc = 4
    p = [2, 2, 2, 4]
    def resize(x, y):
        sx = x
        rx = range(sx)
        sy = y
        ry = range(sy)


def pchr(i):
    if i == 0: return "."
    return repr(i)

def show():
    print("-"*50)
    print("Score: " + repr(G.score))
    for line in G.board:
        print()
        print(" ".join([pchr(i).center(4) for i in line]))


class K:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    EXIT = 4
    RESET = 5

    def get():
        while (True):
            k = msvcrt.getch()
            print(k)
            if k == b'q' or k == b'Q':
                return K.EXIT
            if k == b'r' or k == b'R':
                return K.RESET
            if k == b'\000' or k == b'\xe0':
                k = msvcrt.getch()
                if k == b'H': return K.UP
                if k == b'P': return K.DOWN
                if k == b'K': return K.LEFT
                if k == b'M': return K.RIGHT


def fall(line):
    moved = False
    for i in range(1, len(line)):
        if line[i] != 0 and line[i-1] == 0:
            line[i-1] = line[i]
            line[i] = 0
            moved = True
    return moved

def combine(line):
    moved = False
    for i in range(0, len(line) - 1):
        if line[i] != 0 and line[i+1] == line[i]:
            G.score = G.score + line[i]
            line[i] = 2 * line[i]
            del line[i+1]
            line.append(0)
            moved = True
    return moved

def compress(line):
    items = line.copy()
    while fall(line): pass
    # while combine(line): pass
    combine(line)
    return line != items

def up():
    c = False
    for x in C.rx:
        items = [G.board[y][x] for y in C.ry]
        c = compress(items) or c
        for y in C.ry:
            G.board[y][x] = items[y]
    return c

def down():
    c = False
    for x in C.rx:
        items = [G.board[y][x] for y in C.ry]
        items.reverse()
        c = compress(items) or c
        items.reverse()
        for y in C.ry:
            G.board[y][x] = items[y]
    return c

def left():
    c = False
    for y in C.ry:
        items = G.board[y].copy()
        c = compress(items) or c
        G.board[y] = items
    return c

def right():
    c = False
    for y in C.ry:
        items = G.board[y].copy()
        items.reverse()
        c = compress(items) or c
        items.reverse()
        G.board[y] = items
    return c

def move(k):
    moved = False
    if k == K.UP:
        moved = up()
    elif k == K.DOWN:
        moved = down()
    elif k == K.LEFT:
        moved = left()
    elif k == K.RIGHT:
        moved = right()

    if moved:
        slot = random.choice(G.open_slots())
        G.board[slot[1]][slot[0]] = random.choice(C.p)

def is_locked():
    for x in C.rx:
        for y in range(C.sy - 1):
            n = G.board[y][x]
            if n != 0 and n == G.board[y+1][x]: return False
    for y in C.ry:
        for x in range(C.sx - 1):
            n = G.board[y][x]
            if n != 0 and n == G.board[y][x+1]: return False
    return len(G.open_slots()) == 0

def main():
    G.reset()
    while True:
        show()
        if is_locked():
            print("Game is over!")
            exit()
        else:
            k = K.get()
            if k == K.EXIT:
                exit()
            elif k == K.RESET:
                G.reset()
            else:
                move(k)

if __name__ == "__main__":
    main()
    