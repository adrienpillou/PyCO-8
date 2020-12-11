import pyco8 as p8

class Coin():
    def __init__(self, x, y):
        self.sprite = 17
        self.x = x
        self.y = y


def collide(ax, ay, bx, by, aw, ah, bw, bh):
    if ax<bx+bw and ay< by+bh and ax+aw>bx and ay+ah>by:
        return True
    return False

def _init():
    p8.add(coins, Coin(16, 64))
    p8.add(coins, Coin(24, 64))
    p8.add(coins, Coin(32, 64))
    p8.add(coins, Coin(16, 72))
    p8.add(coins, Coin(24, 72))
    p8.add(coins, Coin(32, 72))
    p8.add(coins, Coin(16, 80))
    p8.add(coins, Coin(24, 80))
    p8.add(coins, Coin(32, 80))
    p8.mset(2, 4, 3)
    p8.mset(12, 12, 38)
    p8.fset(38, 0, True)
    p8.fset(3, 0, True)

def _update():
    global pos, flip
    pos[0]  = p8.mid(0, pos[0], 128)
    pos[1]  = p8.mid(0, pos[1], 128)

    next_pos = []
    next_pos.append(pos[0])
    next_pos.append(pos[1])

    for c in coins:
        if collide(pos[0], pos[1], c.x, c.y, 8, 8, 8, 8):
            p8.rem(coins, c)
            p8.sfx(0)

    if p8.btnp('right'):
        next_pos[0] = pos[0] + 8
        flip = False
        p8.sfx(1)
    elif p8.btnp('left'):
        p8.sfx(1)
        next_pos[0] = pos[0] - 8
        flip = True
    elif p8.btnp('up'):
        p8.sfx(1)
        next_pos[1] = pos[1] - 8
    elif p8.btnp('down'):
        p8.sfx(1)
        next_pos[1] = pos[1] + 8
    
    next_pos[0] = p8.mid(0, next_pos[0], 128)
    next_pos[1] = p8.mid(0, next_pos[1], 128)
    if not (p8.fget(p8.mget(next_pos[0]//8, (next_pos[1])//8), 0)):
        pos = next_pos
    
def _draw():
    p8.cls()
    p8.map()
    for c in coins:
        p8.spr(c.sprite, c.x, c.y)
    p8.spr(1, pos[0], pos[1], 8, 8, flip)
    p8.text(f"[MATTHIS]:", 8, 17, 2)
    p8.text(f"[MATTHIS]:", 8, 16, 9)
    p8.text(f"JE VEUX DES V BUCKS !", 8, 22, 7)
    p8.text(str(p8.time()), 8, 8)


coins = []
pos = [64, 64]
flip = False