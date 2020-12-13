# PyCO-8 Shared varibales 

# Gamepad class used for controls
class Gamepad():
    def __init__(self):
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.o = False
        self.x = False
    
    def debug(self):
        print(f"UP:{self.up}\nDOWN:{self.down}\nRIGHT:{self.right}\nLEFT:{self.left}")

def init():
    global window
    global display
    global gamepad
    gamepad = Gamepad()
    global sounds
    global spritesheet
    global fontsheet
    global map_data
    global flags

    