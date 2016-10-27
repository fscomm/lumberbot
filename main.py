import time
from enum import Enum
from pymouse import PyMouse
from pykeyboard import PyKeyboard

pymouse = PyMouse()
pykeyboard = PyKeyboard()
gaps = []

class Position(Enum):
    LEFT = 0
    RIGHT = 1

position = Position.LEFT

#detect brown colour in branch
def is_tree_branch(rgb_p):
    sum_p = sum(rgb_p)
    #print ("sum: " + str(sum_p))
    if sum_p > 270 and sum_p < 346:
        return True
    return False

#fill missing branches array
#if branch is missing, we must tap twice accordingly to current position
def fill_gaps(i_x, i_y):
    import PIL.Image
    import PIL.ImageStat
    import Xlib.display
    global gaps
    global position

    #print("DEBUG: fill_gaps: (" + str(i_x) + "," + str(i_y) + "); position = " + str(position))
    gaps = []
    o_x_root = Xlib.display.Display().screen().root
    while i_y > 100:
        o_x_image = o_x_root.get_image(i_x, i_y, 1, 1, Xlib.X.ZPixmap, 0xffffffff)
        o_pil_image_rgb = PIL.Image.fromstring("RGB", (1, 1), o_x_image.data, "raw", "BGRX")
        lf_colour = PIL.ImageStat.Stat(o_pil_image_rgb).mean
        rgb_p = tuple(map(int, lf_colour))
        #print ("(" + str(i_x) + "," + str(i_y) + "): " + str(rgb_p))
        if not is_tree_branch(rgb_p):
            gaps.append(position)
            i_y -= 100
        else:
            if position == Position.LEFT:
                position = Position.RIGHT
                i_x += 115
            else:
                position = Position.LEFT
                i_x -= 115
    return i_x

def do_taps(position):
    for i in range(2):
        if position == Position.LEFT:
            pykeyboard.tap_key(pykeyboard.left_key)
        else:
            pykeyboard.tap_key(pykeyboard.right_key)
        time.sleep(0.022)

def main():
    global pymouse
    global pykeyboard
    global gaps

    x_dim, y_dim = pymouse.screen_size()
    pymouse.click(100, y_dim - 100, 1)
    time.sleep(0.3)

    i_x = 935

    while True:
        i_x = fill_gaps(i_x, 677)
        for pos in gaps:
            do_taps(pos)
        time.sleep(0.17)

if __name__ == "__main__":
    main()