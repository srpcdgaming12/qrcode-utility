import threading
import cv2
from main import __doc__ as comp_warning
from tkinter import Toplevel, Frame, Menubutton, messagebox

use_cv2 = False
pyzbar = None

try:
    from pyzbar import pyzbar
except Exception as pyzbar_event:
    messagebox.showwarning(message=comp_warning, title="Compatibility Error")
    use_cv2 = True
    del pyzbar_event


class OpenImage(threading.Thread):
    def __init__(self, image):
        super().__init__(target=image.show)


def decode_qr_code(image):
    decoded_data = ''
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if not use_cv2:
        barcodes = pyzbar.decode(gray)

        for barcode in barcodes:
            data = barcode.data.decode("utf-8")
            decoded_data += data + '\n'
    else:
        qr_code_detector = cv2.QRCodeDetector()
        qrcode_data = qr_code_detector.detectAndDecodeMulti(gray)

        for data in qrcode_data[1]:
            decoded_data += data + '\n'

    return decoded_data


class ThemedMenu(Frame):
    def __init__(self, master=None, **kw) -> None:
        if 'arrow_syntax' in kw.keys():
            self.arrow_syntax = True
            kw.pop('arrow_syntax')
        else:
            self.arrow_syntax = False
    
        super().__init__(master, **kw)
        self.master = master
        self.cur_menubutton = None
        self.widget = None
        self.buttons: list = []
        self.menus: list = []

    def shift_left_menu(self, event):
        self.widget = event.widget
        self.widget.config(bg=self.widget['activebackground'])
    
    def shift_right_menu(self):
        for menubutton in self.buttons:
            menubutton.config(bg=self['background'])

    def add_cascade(self, label: str = None, menu=None, **kw):
        if not menu:
            self.buttons.append(Menubutton(self, text=label, **kw))
        else:
            self.buttons.append(Menubutton(self, text=label, menu=menu, **kw))
            self.buttons[-1].cmenu = menu

        return self.buttons[-1]

    def menu_bind_all(self):
        for index, menubutton in enumerate(self.buttons):
            menubutton.bind("<ButtonPress-1>", self.shift_left_menu)
            self.master.bind("<ButtonPress-1>", lambda event: self.shift_right_menu())

    def edit_cascade(self, index: int, **kw) -> None:
        self.buttons[index].config(**kw)
        if 'menu' in kw.keys():
            self.buttons[index].cmenu = kw['menu']


class QRCodeUnresponsive(Toplevel):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.withdraw()
    
    def responsive(self, condition: bool):
        if condition:
            self.grab_set()
        else:
            self.grab_release()

    