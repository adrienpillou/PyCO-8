import pygame
import settings
from pyco8 import *

class Coin():
    def __init__(self, x, y):
        self.sprite = 17
        self.x = x
        self.y = y

def collide(ax, ay, bx, by, aw, ah, bw, bh):
    if ax<bx+bw and ay< by+bh and ax+aw>bx and ay+ah>by:
        return True
    return False

# Use this for initialisation
def _init():
    add(coins, Coin(16, 64))
    add(coins, Coin(24, 64))
    add(coins, Coin(32, 64))
    add(coins, Coin(16, 72))
    add(coins, Coin(24, 72))
    add(coins, Coin(32, 72))
    add(coins, Coin(16, 80))
    add(coins, Coin(24, 80))
    add(coins, Coin(32, 80))
    mset(2, 4, 3)
    mset(12, 12, 38)
    fset(38, 0, True)
    fset(3, 0, True)
    
# Called once per frame
def _update():
    global pos, flip
    pos = [mid(0, pos[0], 128), mid(0, pos[1], 128)]
    next_pos = []
    next_pos.append(pos[0])
    next_pos.append(pos[1])

    for c in coins:
        if collide(pos[0], pos[1], c.x, c.y, 8, 8, 8, 8):
            rem(coins, c)
            sfx(0)

    if btnp('right'):
        next_pos[0] = pos[0] + 8
        flip = False
        sfx(1)
    elif btnp('left'):
        sfx(1)
        next_pos[0] = pos[0] - 8
        flip = True
    elif btnp('up'):
        sfx(1)
        next_pos[1] = pos[1] - 8
    elif btnp('down'):
        sfx(1)
        next_pos[1] = pos[1] + 8
    
    next_pos[0] = mid(0, next_pos[0], 128)
    next_pos[1] = mid(0, next_pos[1], 128)
    if not (fget(mget(next_pos[0]//8, (next_pos[1])//8), 0)):
        pos = next_pos

# Called once per frame
def _draw():
    cls()
    map()
    for c in coins:
        spr(c.sprite, c.x, c.y)
    spr(1, pos[0], pos[1], 8, 8, flip)
    text(f"[OLD MAN]:", 8, 17, 2)
    text(f"[OLD MAN]:", 8, 16, 9)
    text(f"IT'S DANGEROUS TO GO ALONE!", 8, 24, 7)
    text(str(time()), 8, 8)

if __name__ == "__main__":
    # cd to parent dir
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
   
    # Initialize some stuff
    pygame.mixer.pre_init(44100, -16, 1, 1024)
    pygame.init()
    settings.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Global variables
    coins = []
    pos = [64, 64]
    flip = False

    # Framework variables
    RESOLUTION = (128, 128)
    MULTIPLIER = 10

    # Loading shared attributes and resources
    settings.window = pygame.display.set_mode((RESOLUTION[0]*MULTIPLIER, RESOLUTION[1]*MULTIPLIER))
    settings.display = pygame.Surface(RESOLUTION)
    settings.spritesheet = pygame.image.load("./spritesheet.gif")
    settings.map_data = load_map()
    settings.fontsheet = pygame.image.load("./font.gif")
    settings.sounds = load_sounds() # Sound effects 
    settings.flags = load_flags() # Sprite flags data
    
    # Pygame setup
    clock = pygame.time.Clock()
    pygame.display.set_caption("PyCO-8")
    pygame.display.set_icon(pygame.image.load("./icon.png"))
    
    cls()
    _init()
    while True:
        _update()
        settings.display = pygame.Surface(RESOLUTION)
        _draw()
        settings.display = pygame.transform.scale(settings.display, (RESOLUTION[0]*MULTIPLIER, RESOLUTION[1]*MULTIPLIER))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            manage_input(event)
        settings.window.blit(settings.display, (0, 0))
        pygame.display.update()
        clock.tick(60)