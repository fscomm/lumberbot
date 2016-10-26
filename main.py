import time
from enum import Enum
from pymouse import PyMouseEvent
from pymouse import PyMouse
from pykeyboard import PyKeyboard

pymouse = PyMouse()
pykeyboard = PyKeyboard()

class Tree(Enum):
    LEFT = 1
    RIGHT = 2

leaf = Tree.LEFT

def get_pixel_colour(i_x, i_y):
    import PIL.Image # python-imaging
    import PIL.ImageStat # python-imaging
    import Xlib.display # python-xlib
    o_x_root = Xlib.display.Display().screen().root
    o_x_image = o_x_root.get_image(i_x, i_y, 1, 1, Xlib.X.ZPixmap, 0xffffffff)
    o_pil_image_rgb = PIL.Image.fromstring("RGB", (1, 1), o_x_image.data, "raw", "BGRX")
    lf_colour = PIL.ImageStat.Stat(o_pil_image_rgb).mean
    return tuple(map(int, lf_colour))

def tap():
    global leaf
    if leaf == Tree.LEFT:
        pykeyboard.tap_key(pykeyboard.left_key)
    else:
        pykeyboard.tap_key(pykeyboard.right_key)

def changing_position():
    global leaf
    x = 577
    y = 849
    if leaf == Tree.RIGHT:
        x += 100
    for x_axis in range(x-1,x+2):
        for y_axis in range(y-1, y+2):
            pixel = get_pixel_colour(x_axis, y_axis)
            sum_pixel = sum(pixel)
            if sum_pixel > 270 and sum_pixel < 346:
                #print("("+str(x)+", "+str(y_axis)+"): "+str(pixel))
                return True
    return False

def change_leaf():
    global leaf
    if leaf == Tree.LEFT:
        leaf = Tree.RIGHT
    else:
        leaf = Tree.LEFT

def main():
    global pymouse
    global pykeyboard
    global leaf

    x_dim, y_dim = pymouse.screen_size()
    pymouse.click(100, y_dim - 100, 1)

    i = 0
    while i < 2000:
        tap()
        if changing_position():
            change_leaf()
        i += 1
        time.sleep(0.12)

if __name__ == "__main__":
    main()