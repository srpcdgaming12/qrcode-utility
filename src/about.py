import tkinter as tk
import webbrowser

opened = False
cur_about = None


def about_window(master, icon, *args, **kwargs):
    global cur_about
    if opened:
        cur_about.focus_force()
        return
    about = AboutWindow(master, icon, *args, **kwargs)
    about.focus_force()
    cur_about = about
    return about


class AboutWindow(tk.Toplevel):
    """
    QRCode Utility - srpcdgaming12
    Version v1.00
    
    Barcode Scanner: {bar_name}
    """

    def __init__(self, master, icon, use_cv2, *args, **kwargs):
        global opened
        super().__init__(master, *args, **kwargs)
        self.withdraw()
        self.geometry("400x290")
        self.title("About")
        self.opened = opened = True
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.iconbitmap(icon)
        self.resizable(False, False)
        self.frame = tk.Frame(self, bg='#222222')
        self.frame.columnconfigure(1, weight=1)
        self.frame.pack(fill='both', expand=True)
        self.text = tk.Label(self.frame, text='About QRCode Utility', font=("Calibri", 12, 'bold'), fg='white',
                             bg='#151515', padx=125, pady=10)
        self.explanation = tk.Label(self.frame, font=("Calibri", 11), fg='white', bg='#222222', justify=tk.LEFT,
                                    text=self.__doc__.format(bar_name="OpenCV 2.0" if use_cv2 else "Pyzbar"))
        self.url = "https://github.com/srpcdgaming12/qrcode-utility"
        self.github_btn = tk.Button(self.frame, text='Github', padx=9, pady=3, bg='black',
                                    fg='white', activebackground='#353535', activeforeground='white', relief=tk.SUNKEN,
                                    bd=0, command=lambda: webbrowser.open(self.url))
        self.exit_btn = tk.Button(self.frame, text='Ok', padx=21, pady=3, bg='black',
                                  fg='white', activebackground='#353535', activeforeground='white', relief=tk.SUNKEN,
                                  bd=0, command=self.close)
        self.github_link = tk.Entry(self.frame, width=38, font=('Calibri', 11), background='black',
                                    foreground='white', bd=0, relief=tk.SUNKEN, disabledbackground='black',
                                    disabledforeground='white')
        self.github_link.insert(0, self.url)
        self.github_link.config(state=tk.DISABLED)
        self.text.grid(row=0, column=2)
        self.explanation.grid(row=1, column=0, columnspan=3, sticky='w', padx=25)
        self.github_btn.grid(row=2, column=0, columnspan=3, pady=20, sticky='w', padx=25)
        self.exit_btn.grid(row=3, column=2)
        self.github_link.grid(row=2, column=1, columnspan=3, padx=(0, 35), sticky='e')
        self.deiconify()

    def close(self):
        global opened
        opened = False
        self.opened = False
        self.destroy()
