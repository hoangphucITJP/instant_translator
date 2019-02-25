import sys
from ctypes import *
import time

import clipboard
import tkinter as tk
from mtranslate import translate

DEFAULT_TIMEOUT = 1000

Xlib = CDLL("libX11.so.6")
display = Xlib.XOpenDisplay(None)


def get_mouse_position():
    if display == 0:
        sys.exit(2)
    w = Xlib.XRootWindow(display, c_int(0))
    (root_id, child_id) = (c_uint32(), c_uint32())
    (root_x, root_y, win_x, win_y) = (c_int(), c_int(), c_int(), c_int())
    mask = c_uint()
    ret = Xlib.XQueryPointer(display, c_uint32(w), byref(root_id), byref(child_id),
                             byref(root_x), byref(root_y),
                             byref(win_x), byref(win_y), byref(mask))
    if ret == 0:
        sys.exit(1)
    return root_x.value, root_y.value


def popup(msg, pos, timeout):
    window = tk.Tk()
    window.overrideredirect(1)
    window.geometry("+%s+%s" % (pos[0], pos[1]))
    var = tk.StringVar()
    label = tk.Label(window, textvariable=var, relief=tk.RAISED)
    var.set(msg)
    label.pack()
    window.after(timeout, lambda: window.destroy())
    window.mainloop()


if __name__ == '__main__':
    old_text = None
    while True:
        current_text = clipboard.paste()
        if current_text != old_text:
            translate_text = translate(current_text, 'vi', 'en')
            old_text = current_text
            popup('Translated: %s' % translate_text, get_mouse_position(), DEFAULT_TIMEOUT)
        time.sleep(1)
