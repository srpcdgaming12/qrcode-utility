"""\
Your computer may not be compatible with pyzbar.
Some QRCodes can be read, but some zoomed or colored can't be scanned.
"""

from root import *

if __name__ == "__main__":
    qrcode_util = QRCodeUtility()
    qrcode_util.mainloop()
