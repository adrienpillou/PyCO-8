# PyCO-8 library
# Author : Adrien Pillou
# Date : 12/07/2020

### Notes ###
# 128x128p = 8 ko
# 1 sprite = 64 bytes
# 256 sprites in a sheet
# 8 flags per sprite => 1 byte =>256 bytes

import os
import sys
import csv
import random
import math
import pygame
import settings


# PICO-8 color palette
palette = [
    (0, 0, 0),
    (29, 43, 83),
    (126, 37, 83),
    (0, 135, 81),
    (171, 82, 54),
    (95, 87, 79),
    (194, 195, 199),
    (247, 233, 225),
    (255, 0, 77),
    (255, 163, 0),
    (255, 236, 39),
    (0, 228, 54),
    (41, 173, 255),
    (131, 118, 156),
    (255, 119, 168),
    (255, 204, 170),
]

# Add an element to a list
def add(t:list, v):
    t.append(v)
    return t

# Check if a button is hold down
def btn(i, p=0):
    if i == 'up':
        if settings.gamepad.up:
            return True
    if i == 'down':
        if settings.gamepad.down:
            return True
    if i == 'right':
        if settings.gamepad.right:
            return True
    if i == 'left':
        if settings.gamepad.left:
            return True
    if i == 'x':
        if settings.gamepad.x:
            return True
    if i == 'o':
        if settings.gamepad.o:
            return True
    return False

# Check if a button is pressed
def btnp(i, p=0):
    if i == 'up':
        if settings.gamepad.up:
            settings.gamepad.up = False
            return True
    if i == 'down':
        if settings.gamepad.down:
            settings.gamepad.down = False
            return True
    if i == 'right':
        if settings.gamepad.right:
            settings.gamepad.right = False
            return True
    if i == 'left':
        if settings.gamepad.left:
            settings.gamepad.left = False
            return True
    if i == 'x':
        if settings.gamepad.x:
            settings.gamepad.x = False
            return True
    if i == 'o':
        if settings.gamepad.o:
            settings.gamepad.o = False
            return True
    return False

# Draw a circle
def circ(x, y, r, col):
    pygame.draw.circle(settings.display, palette[col], (x, y), r, 1)

# Draw a filled circle shape
def circfill(x, y, r, col):
    pygame.draw.circle(settings.display, palette[col], (x, y), r)

# Clear the screen
def cls(c = 0):
    if c < 0:
        c = 0
    elif c >= 15:
        c = 15
    settings.window.fill((0, 0, 0))
    settings.display.fill(palette[c])

# Get a flag state
def fget(n, f=None):
    if f is None:
        return settings.flags[n]
    # Convert flag data to binary string
    spr_flags = "{0:b}".format(settings.flags[n]).zfill(8)
    # Check flag state
    if spr_flags[7-f] == "1":
        return True
    return False

# Set a flag state
def fset(n, f=0, v=False):
    # Convert flag data to binary string
    if(not isinstance(v, bool)):
        print("Wrong flag value type : bool only.")
        return
    if f<0 or f>7:
        print("Flag index out of bound. Should be between 0 and 7")
        return
    if n<0 or n>127:
        print("Sprite index out of bound !")
        return
    spr_flags = "{0:b}".format(settings.flags[n]).zfill(8)
    flag_list = list(spr_flags)
    flag_list[7-f] = str(int(v)) # Set flag state to 1 or 0
    spr_flags = "".join(flag_list)
    dec = int(spr_flags, 2)
    settings.flags[n] = dec
    save_flags()

# Load flag save file (framework only)
def load_flags():
    #if len(flags) == 0:
    #    flags = [0 for i in range(128)]
    f = open("flags.bin", "rb")
    data = list(f.read())
    f.close()
    return data

# Load map file (framework only)
def load_map():
    with open("./map.txt", newline='') as file:
        reader = csv.reader(file, delimiter='\t', quotechar='|')
        data = []
        for row in reader:
            for i in range(len(row)):
                row[i] = int(row[i])# Converting string to int
            data.append(row)
    return data

# Load sound effects located in 'sfx' directory (framework only)
def load_sounds():
    sfxs = []
    sfx_dir = "./sfx"
    for filename in os.listdir('./sfx'):
        if filename.endswith(".wav"):
            sfxs.append(pygame.mixer.Sound(os.path.join(sfx_dir, filename)))
    return sfxs

# Handle various inputs (framework only)
def manage_input(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            settings.gamepad.up = True
        if event.key == pygame.K_DOWN:
            settings.gamepad.down = True
        if event.key == pygame.K_RIGHT:
            settings.gamepad.right = True
        if event.key == pygame.K_LEFT:
            settings.gamepad.left = True
        if event.key == pygame.K_x:
            settings.gamepad.x = True
        if event.key == pygame.K_c:
            settings.gamepad.o = True
    elif event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
            settings.gamepad.up = False
        if event.key == pygame.K_DOWN:
            settings.gamepad.down = False
        if event.key == pygame.K_RIGHT:
            settings.gamepad.right = False
        if event.key == pygame.K_LEFT:
            settings.gamepad.left = False
        if event.key == pygame.K_x:
            settings.gamepad.x = False
        if event.key == pygame.K_c:
            settings.gamepad.o = False

# Draw the map
def map(celx=0, cely=0, sx=0, sy=0, celw=16, celh=16, layer=0):
    # Load the map if it isn't done yet
    if settings.map_data is None:
        settings.map_data = load_map()
    # Draw each cell of it using spr()
    # 4x2 screens (16x16 tiles per screen)
    # 128 wide x 32 high tiles
    # csv format
    celw = mid(0, celw, 127)
    celh = mid(0, celw, 31)
    for j in range(celw):
        for i in range(celh):
            spr(settings.map_data[j][i], sx+i*8, sy+j*8)
    pass

# Get tile sprite index from the map
def mget(x, y):
    return settings.map_data[y][x]

def mid(first, second, third):
    if first < second:
        return second
    elif second > third:
        return third
    else:
        return second

# Set tile sprite index to the map
def mset(x, y, v):
    settings.map_data[y][x] = v

# Get the color of a pixel on the display
def pget(x, y):
    c = settings.display.get_at((x,y))
    for i, p in enumerate(palette):
        if p == c:
            return i
    return 

# Set the color of a pixel on the display
def pset(x, y, c):
    settings.display.set_at((x, y), palette[c])

# Draw a rect shape
def rect(x0, y0, x1, y1, col):
    pygame.draw.rect(settings.display, palette[col], (x0, y0, x1-x0, y1-y0), 1)

# Draw a filled rect shape
def rectfill(x0, y0, x1, y1, col):
    pygame.draw.rect(settings.display, palette[col], (x0, y0, x1-x0, y1-y0))

# Remove an element from a given list
def rem(t:list, v):
    if v in t:
        t.remove(v)

# Play a sound effect
def sfx(c):
    if c >= len(settings.sounds):
        print('Sfx index out of bound !')
        return
    settings.sounds[c].play()
    settings.sounds[c].set_volume(1)

# Draw a sprite sliced from the spritesheet
def spr(s, x=0, y=0, w=8, h=8, flip_x=False, flip_y=False):
    if(s==0):
        return
    sprite  = pygame.Surface((w,h))
    sprite.blit(settings.spritesheet, (0, 0), (s%16*8, math.floor(s/16)*8, w, h))
    sprite.set_colorkey((0,0,0))
    if flip_x or flip_y:
        sprite = pygame.transform.flip(sprite, flip_x, flip_y)
    settings.display.blit(sprite, (x,y))

# Save all flags to a binary file
def save_flags():
    f = open("flags.bin","wb")
    data = bytearray(settings.flags)
    f.write(data)
    f.close()

# Print text on the display
def text(t, x=0, y=0, color = 7):
    pivot = (x,y)
    font_width = 4
    font_height = 6
    color = mid(0, color, 15)
    char_index = 0
    for char in t:
        sprite = pygame.Surface((font_width, font_height))
        chars = {
            "A" : (0,0),
            "B" : (1,0),
            "C" : (2,0),
            "D" : (3,0),
            "E" : (4,0),
            "F" : (5,0),
            "G" : (6,0),
            "H" : (7,0),
            "I" : (8,0),
            "J" : (9,0),
            "K" : (10,0),
            "L" : (11,0),
            "M" : (12,0),
            "N" : (13,0),
            "O" : (14,0),
            "P" : (15,0),
            "Q" : (16,0),
            "R" : (17,0),
            "S" : (18,0),
            "T" : (19,0),
            "U" : (20,0),
            "V" : (21,0),
            "W" : (22,0),
            "X" : (23,0),
            "Y" : (24,0),
            "Z" : (25,0),
            "a" : (0,1),
            "b" : (1,1),
            "c" : (2,1),
            "d" : (3,1),
            "e" : (4,1),
            "f" : (5,1),
            "g" : (6,1),
            "h" : (7,1),
            "i" : (8,1),
            "j" : (9,1),
            "k" : (10,1),
            "l" : (11,1),
            "m" : (12,1),
            "n" : (13,1),
            "o" : (14,1),
            "p" : (15,1),
            "q" : (16,1),
            "r" : (17,1),
            "s" : (18,1),
            "t" : (19,1),
            "u" : (20,1),
            "v" : (21,1),
            "w" : (22,1),
            "x" : (23,1),
            "y" : (24,1),
            "z" : (25,1),
            "0" : (0,2),
            "1" : (1,2),
            "2" : (2,2),
            "3" : (3,2),
            "4" : (4,2),
            "5" : (5,2),
            "6" : (6,2),
            "7" : (7,2),
            "8" : (8,2),
            "9" : (9,2),
            "." : (10,2),
            "," : (11,2),
            "\"" : (12,2),
            "'" : (13,2),
            "?" : (14,2),
            "!" : (15,2),
            "@" : (16,3),
            "_" : (17,3),
            "*" : (18,3),
            "#" : (19,3),
            "$" : (20,3),
            "%" : (21,3),
            "(" : (22,3),
            ")" : (23,3),
            "+" : (24,2),
            "-" : (25,2),
            "/" : (0,3),
            ":" : (1,3),
            ";" : (2,3),
            "<" : (3,3),
            "=" : (4,3),
            ">" : (5,3),
            "[" : (6,3),
            "\\": (7,3),
            "]" : (8,3),
            "^" : (9,3),
            "{" : (10,3),
            "|" : (11,3),
            "}" : (12,3),
            "~" : (13,3),
        }
        if(char == "\n"):
            y+=6
            x=pivot[0]
            continue
        if char in chars:
            (i, j) = chars[char]
        else:(i, j) = (24, 3)
        
        # Cut the char bitmap
        sprite.blit(settings.fontsheet, (0, 0), (i*font_width, j*font_height, font_width, font_height))
        sprite.set_colorkey((0,0,0))

        # Tint the bitmap
        mask = pygame.surface.Surface(sprite.get_size())
        mask.fill(palette[color])
        sprite.blit(mask, (0, 0), special_flags = pygame.BLEND_RGB_MULT)
        
        # Print the text
        settings.display.blit(sprite, (x, y))
        x+=sprite.get_width()

# Get ellapsed time since the game has started (since pygame.init())
def time():
    return pygame.time.get_ticks()/1000
