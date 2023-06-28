import tkinter as tk
import qrcode
import about
import sys
import os
from tkinter import filedialog
from utils import *
from PIL import Image, ImageTk


class QRCodeUtility(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("420x600")
        self.title("QRCode Utility")
        self.resizable(False, False)
        self.config(bg='#222222')
        sys.exit(0) if not hasattr(sys, "_MEIPASS") else None
        self.iconbitmap(f"{sys._MEIPASS}\\icons\\qrcode_gen_icon.ico")
        self.responsive = QRCodeUnresponsive(self)
        self.qr_photo_image = self.resized_image = self.prev_image = self.decoded_data = None
        self.blank_image = Image.new("RGB", (160, 160), "white")
        self.blank_image = ImageTk.PhotoImage(self.blank_image)
        
        self.menu_bar = ThemedMenu(self, height=16, bg='#131313')
        self.menu_bar.pack(side=tk.TOP, fill=tk.X)
        
        self.generator_cascade = self.menu_bar.add_cascade(label='Generator', height=-15, activebackground='#202020',
                                                           bg='#131313', bd=0, highlightthickness=0, relief=tk.SUNKEN,
                                                           activeforeground='white', fg='white')
        self.generator_cascade.grid(row=0, column=0)
        self.scanner_cascade = self.menu_bar.add_cascade(label='Scanner', height=-15, activebackground='#202020',
                                                         bg='#131313', bd=0, highlightthickness=0, relief=tk.SUNKEN,
                                                         activeforeground='white', fg='white')
        self.scanner_cascade.grid(row=0, column=1, padx=5)
        self.helper_cascade = self.menu_bar.add_cascade(label='Help', height=-15, activebackground='#202020',
                                                        bg='#131313', bd=0, highlightthickness=0, relief=tk.SUNKEN,
                                                        activeforeground='white', fg='white')
        self.helper_cascade.grid(row=0, column=2)
        
        self.generator_menu = tk.Menu(self.menu_bar.buttons[0], tearoff=0, bg='#202020', fg='white',
                                      disabledforeground='gray', activeforeground='white', activebackground='#303030')
        self.generator_menu.add_command(label='Generate', command=self.change_image)
        self.generator_menu.add_separator()
        self.generator_menu.add_command(label="Save", command=self.save)
        self.generator_menu.add_command(label="Delete", command=self.delete)
        self.generator_menu.add_command(label="Show", command=self.show)
        self.generator_menu.add_separator()
        self.generator_menu.add_command(label="Exit", command=self.destroy)
        
        self.scanner_menu = tk.Menu(self.menu_bar.buttons[1], tearoff=0, bg='#202020', fg='white',
                                    activeforeground='white', activebackground='#303030')

        self.current_mode = tk.IntVar(value=0)

        self.scanner_menu.add_command(label='Open File', command=self.open_image)
        self.scanner_menu.add_separator()
        self.scanner_menu.add_checkbutton(label='Edit Mode', command=self.show_user_path, variable=self.current_mode,
                                          onvalue=1, offvalue=0, selectcolor='white')
        self.scanner_menu.add_separator()
        self.scanner_menu.add_command(label='Load Image', command=self.edit_directory)
        self.scanner_menu.add_command(label='Delete', command=self.delete_scan)

        self.help_menu = tk.Menu(self.menu_bar.buttons[2], tearoff=0, bg='#202020', fg='white',
                                 activeforeground='white', activebackground='#303030')

        self.icon = f"{getattr(sys, '_MEIPASS', os.getcwd())}\\icons\\qrcode_gen_icon.ico"

        self.help_menu.add_command(label='About', command=lambda: about.about_window(self, self.icon, use_cv2))

        self.menu_bar.edit_cascade(0, menu=self.generator_menu)
        self.menu_bar.edit_cascade(1, menu=self.scanner_menu)
        self.menu_bar.edit_cascade(2, menu=self.help_menu)

        self.menu_bar.menu_bind_all()
        
        self.bind("<Alt_L>", lambda e: (self.generator_menu.post(self.winfo_x()+8, self.winfo_y()+55)))
        
        self.generator = tk.LabelFrame(self, bg='#222222', text='Generator', fg='white')
        self.generator.pack(padx=25, pady=15)
        self.gen_label = tk.Label(self.generator, bg='SystemButtonFace', image=self.blank_image, bd=0)
        self.gen_label.grid(row=3, column=0, padx=25, pady=25, rowspan=7, sticky='w')
        self.gen_entry = tk.Entry(self.generator, width=31, font=('Helvetica', 11), background='black', fg='white',
                                  bd=0, relief=tk.SUNKEN)
        self.gen_entry.grid(row=2, column=0, pady=(15, 0), padx=15)
        self.gen_button = tk.Button(self.generator, text='Generate', command=self.change_image, bg='black', fg='white',
                                    padx=11, pady=3, activebackground='#353535', activeforeground='white',
                                    relief=tk.SUNKEN, bd=0)
        self.gen_button.grid(row=2, column=2, pady=(15, 0), padx=(0, 30))
        self.save_button = tk.Button(self.generator, text='Save', command=self.save, padx=11, pady=3, bg='black',
                                     fg='white', activebackground='#353535', activeforeground='white', relief=tk.SUNKEN,
                                     bd=0)
        self.del_button = tk.Button(self.generator, text='Delete', command=self.delete, padx=7, pady=3, bg='black',
                                    fg='white', activebackground='#353535', activeforeground='white', relief=tk.SUNKEN,
                                    bd=0)
        self.show_button = tk.Button(self.generator, text='Open', command=self.show, padx=9, pady=3, bg='black',
                                     fg='white', activebackground='#353535', activeforeground='white', relief=tk.SUNKEN,
                                     bd=0)
        self.save_button.grid(row=3, column=0, padx=25, pady=(25, 0), columnspan=2, sticky='e')
        self.del_button.grid(row=4, column=0, padx=25, columnspan=2, sticky='e')
        self.show_button.grid(row=5, column=0, padx=25, columnspan=2, sticky='e')
        
        self.scanner = tk.LabelFrame(self, bg='#222222', text='Scanner', fg='white')
        self.scanner.pack(padx=25, pady=(0, 25))

        self.open_file = tk.Button(self.scanner, text='Open File', command=self.open_image, padx=5, pady=3, bg='black',
                                   fg='white', activebackground='#353535', activeforeground='white', relief=tk.SUNKEN,
                                   bd=0)
        self.open_file.grid(row=0, column=0, pady=(0, 0), sticky='w', padx=15)
        self.preview_file_path = tk.Entry(self.scanner, width=22, font=('Helvetica', 11), background='black',
                                          foreground='white', bd=0, relief=tk.SUNKEN, disabledbackground='black',
                                          disabledforeground='white', state=tk.DISABLED)
        self.preview_file_path.grid(row=0, column=1, pady=15, sticky='e')
        self.preview_file_path.bind("<Return>", lambda e: self.fast_enter())

        self.edit_image = Image.open(f"{getattr(sys, '_MEIPASS', os.getcwd())}\\icons\\edit.png")
        self.edit_icon = ImageTk.PhotoImage(self.edit_image.resize((13, 13)))

        self.edit_file_path = tk.Button(self.scanner, image=self.edit_icon, padx=8, pady=8, width=23, height=23,
                                        bg='black', fg='white', activebackground='black', activeforeground='white',
                                        relief=tk.SUNKEN, bd=0, command=self.show_user_path)
        self.edit_file_path.grid(row=0, column=2, sticky='e', padx=(14, 8))

        self.conv_image = Image.open(f"{getattr(sys, '_MEIPASS', os.getcwd())}\\icons\\convert.png")
        self.conv_icon = ImageTk.PhotoImage(self.conv_image.resize((13, 13)))

        self.conv_file_path = tk.Button(self.scanner, image=self.conv_icon, padx=8, pady=8, width=23, height=23,
                                        bg='black', fg='white', activebackground='#353535', activeforeground='white',
                                        relief=tk.SUNKEN, bd=0, command=self.edit_directory)
        self.conv_file_path.grid(row=0, column=3, padx=(0, 20))

        self.qr_text_frame = tk.Frame(self.scanner, bg='#222222')
        self.qr_text_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=20, sticky='w')
        self.qrcode_text = tk.Text(self.qr_text_frame, width=20, height=8, background='black', state='disabled',
                                   foreground='white', bd=0, relief=tk.SUNKEN)
        self.qrcode_text.pack(side=tk.LEFT)
        self.scrollbar = tk.Scrollbar(self.qr_text_frame, orient=tk.VERTICAL, command=self.qrcode_text.yview,
                                      bg='black', width=15)
        self.loaded_file_path = ''
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.qrcode_text.config(yscrollcommand=self.scrollbar.set)
        self.prev_example = Image.new("RGB", (130, 130), "white")
        self.prev_example = ImageTk.PhotoImage(self.prev_example)
        self.preview_qr_read = tk.Label(self.scanner, image=self.prev_example)
        self.preview_qr_read.grid(row=1, column=1, sticky='e', padx=(20, 14), columnspan=3)
        
        self.delete()

    def generate_custom_qrcode(self, website_url, size):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10, border=4)
        qr.add_data(website_url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        self.resized_image = qr_image.resize((size, size))
        return self.resized_image

    def fast_enter(self):
        if not os.path.exists(self.preview_file_path.get()):
            messagebox.showerror("Error", f"Path to {self.preview_file_path.get()} doesn't exist.")
            return
        self.hide_user_path()
        self.edit_directory()

    def change_image(self):
        self.gen_label.grid_forget()
        self.gen_label.grid(row=3, column=0, padx=25, pady=25, rowspan=7, sticky='w')
        self.gen_label.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
        self.del_button.config(state=tk.NORMAL)
        self.show_button.config(state=tk.NORMAL)
        website_url = self.gen_entry.get()
        qr_code_size = 160
        qr_image = self.generate_custom_qrcode(website_url, qr_code_size)
        self.qr_photo_image = ImageTk.PhotoImage(image=qr_image)
        self.gen_label.configure(bg='white', image=self.qr_photo_image)
        try:
            for i in range(7):
                self.generator_menu.delete(tk.END)
        except tk.TclError:
            pass

        self.generator_menu.add_command(label='Generate', command=self.change_image)
        self.generator_menu.add_separator()
        self.generator_menu.add_command(label="Save", command=self.save)
        self.generator_menu.add_command(label="Delete", command=self.delete)
        self.generator_menu.add_command(label="Show", command=self.show)
        self.generator_menu.add_separator()
        self.generator_menu.add_command(label="Exit", command=self.destroy)

    def hide_user_path(self):
        if not self.preview_file_path.get():
            self.scanner_menu.entryconfigure("Edit Mode", command=self.show_user_path)
            self.edit_file_path.config(command=self.show_user_path, bg='black', activebackground='black')
            self.preview_file_path.config(state=tk.DISABLED)
            self.current_mode.set(0)
            self.conv_file_path.config(command=self.edit_directory)
            return

        if not os.path.exists(self.preview_file_path.get()):
            messagebox.showerror("Error", f"Path to {self.preview_file_path.get()} doesn't exist.")
            return

        self.loaded_file_path = self.preview_file_path.get()
        self.scanner_menu.entryconfigure("Edit Mode", command=self.show_user_path)
        self.edit_file_path.config(command=self.show_user_path, bg='black', activebackground='black')
        self.current_mode.set(0)
        self.conv_file_path.config(command=self.edit_directory)
        private_file_path = self.loaded_file_path

        if self.preview_file_path.get()[1:].startswith(':\\Users\\') or \
                self.preview_file_path.get()[1:].startswith(':/Users/'):
            for index, letter in enumerate(self.loaded_file_path[9:]):
                if letter in ('/', '\\'):
                    break
                private_file_path = private_file_path[:9 + index] + '*' + private_file_path[9 + index + 1:]

        self.preview_file_path.config(state=tk.NORMAL)
        self.preview_file_path.delete(0, tk.END)
        self.preview_file_path.insert(0, private_file_path)
        self.preview_file_path.config(state=tk.DISABLED)

    def show_user_path(self):
        self.preview_file_path.config(state=tk.NORMAL)
        self.preview_file_path.delete(0, tk.END)
        self.preview_file_path.insert(0, self.loaded_file_path)
        self.scanner_menu.entryconfigure("Edit Mode", command=self.hide_user_path)
        self.current_mode.set(1)
        self.edit_file_path.config(command=self.hide_user_path, bg='#171717', activebackground='#171717')
        self.conv_file_path.config(command=self.fast_enter)

    def save(self):
        if file_name := filedialog.asksaveasfilename(defaultextension='.png', filetypes=[
            ('PNG Files', '.png'), ('JPG Files', '.jpg'), ('All Files', '.*')
        ]):
            self.resized_image.save(file_name)

    def edit_directory(self):
        if self.current_mode.get():
            self.scanner_menu.invoke("Edit Mode")

        try:
            self.start_scanning(self.loaded_file_path)
        except Exception as e:
            if str(e) != "return":
                messagebox.showerror(message=f"An error occurred. Path doesn't exist.", title="Error")
            del e
        else:
            self.preview_qr_read.config(image=self.prev_image)

    def show(self):
        show_img = OpenImage(self.resized_image)
        show_img.start()

    def delete(self):
        self.gen_label.config(image=self.blank_image, state=tk.DISABLED)
        self.gen_entry.delete(0, tk.END)

        self.generator_menu.delete(5)
        self.generator_menu.delete(1)
        self.generator_menu.delete("Save")
        self.generator_menu.delete("Delete")
        self.generator_menu.delete("Show")
        self.generator_menu.delete("Exit")

        self.generator_menu.add_separator()
        self.generator_menu.add_command(label="Exit", command=self.destroy)
        
        self.save_button.config(state=tk.DISABLED)
        self.del_button.config(state=tk.DISABLED)
        self.show_button.config(state=tk.DISABLED)

    def delete_scan(self):
        self.preview_file_path.config(state=tk.NORMAL)
        self.preview_file_path.delete(0, tk.END)
        self.qrcode_text.config(state=tk.NORMAL)
        self.qrcode_text.delete("1.0", tk.END)
        self.qrcode_text.config(state=tk.DISABLED)
        self.loaded_file_path = ''
        self.preview_qr_read.config(image=self.prev_example)

    def open_image(self):
        if file_path := filedialog.askopenfilename(filetypes=[('PNG Files', '*.png'), ('JPG Files', '*.jpg'),
                                                              ('All Files', '*.*')],
                                                   initialdir=f"{os.getenv('USERPROFILE')}\\Pictures"):
            try:
                self.start_scanning(file_path)
            except Exception as e:
                if str(e) != "return":
                    messagebox.showerror(message=f"An error occurred, please try again later.", title="Error")
                del e
            else:
                self.preview_qr_read.config(image=self.prev_image)
    
    def start_scanning(self, file_path):
        self.loaded_file_path = file_path
        private_file_path = str(file_path[:])

        if private_file_path[1:].startswith(':/Users/') or private_file_path[1:].startswith(':\\Users\\'):
            for index, letter in enumerate(file_path[9:]):
                if letter in ('/', '\\'):
                    break
                private_file_path = private_file_path[:9 + index] + '*' + private_file_path[9 + index + 1:]

        self.preview_file_path.config(state=tk.NORMAL)
        self.preview_file_path.delete(0, tk.END)
        self.preview_file_path.insert(0, private_file_path)
        self.preview_file_path.config(state=tk.DISABLED)

        try:
            file_path.encode('ascii')
        except UnicodeEncodeError:
            messagebox.showerror(message=f"\"{file_path}\" contains some characters that are not supported "
                                         f"by this application.", title="Error")
            return

        if len(file_path) <= 0:
            messagebox.showerror(message=f"Please enter a file path, or use the open button to select a file path.",
                                 title="Error")
            raise SyntaxError('return')
            
        self.prev_image = ImageTk.PhotoImage(Image.open(file_path).resize((130, 130)))
        
        read_image = cv2.imread(file_path)
        decoded_data = decode_qr_code(read_image)
        if not decoded_data and not messagebox.askyesno(message="This image is decoded empty. Would you "
                                                                "like to continue?", title='Empty QRCode',
                                                        icon=messagebox.WARNING):
            raise SyntaxError('return')

        self.qrcode_text.config(state=tk.NORMAL)
        self.qrcode_text.delete(1.0, tk.END)
        self.qrcode_text.insert(1.0, decoded_data)
        self.qrcode_text.config(state=tk.DISABLED)

