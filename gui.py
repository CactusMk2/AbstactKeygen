import tkinter as tk
from colors import *
from config import *
from pyperclip import copy, paste
import sys

class Root(tk.Tk):
	key = "Generating..."
	alive = True
	generating = False
	def __init__(self, icon_path):
		super(Root, self).__init__()
		self.configure(bg=BACKGROUND)
		self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file=icon_path))
		W =self.winfo_screenwidth() // 2
		H = self.winfo_screenheight() // 2
		POSW = W-(SIZEW//2)
		POSH = H-(SIZEH//2)
		self.geometry(f"{SIZEW}x{SIZEH}-{POSW}-{POSH}")
		self.resizable(False, False)
		self.attributes(
			'-alpha', ALPHA)
		self.protocol("WM_DELETE_WINDOW", self.on_root_closing)
		self.bind('<Control-KeyPress-c>', self.copy_code)

	def on_root_closing(self):
		self.destroy()
		self.alive = False

	def setNewKey(self, key, timeleft, docopy=True):
		self.key_var.set(key)
		self.date_label.configure(text=timeleft)
		self.key = key
		if docopy:
			copy(key)

	def copy_code(self, *args):
		inbuf = paste()
		if not inbuf == self.key:
			copy(self.key)

	def setupGUI(self):
		# defining widgets
		self.key_var = tk.StringVar()
		self.key_var.set(self.key)
		self.key_entry = tk.Entry(
			self,
			state="readonly",
			relief=tk.FLAT,
			textvariable=self.key_var,
			readonlybackground=CODE_BG,
			fg=CODE_FG,
			justify="center",
			font=("Arial", 35),
			)

		self.copy_btn = tk.Button(
			self,
			relief=tk.GROOVE,
			text="Copy",
			bg=COPY_BUTTON_BG,
			fg=COPY_BUTTON_FG,
			activebackground=COPY_BUTTON_ACTIVE_BG,
			activeforeground=COPY_BUTTON_ACTIVE,
			font=("Arial", 26),
			command=self.copy_code
			)

		self.date_label = tk.Label(
			self,
			text="",
			bg=BACKGROUND,
			fg=DATE_LABEL_BG,
			font=("Arial", 18)
			)

		self.reg_btn = tk.Button(
			self,
			relief=tk.GROOVE,
			text="Regenerate",
			bg=REG_BUTTON_BG,
			fg=REG_BUTTON_FG,
			activebackground=REG_BUTTON_ACTIVE_BG,
			activeforeground=REG_BUTTON_ACTIVE,
			font=("Arial", 26)
			)
		self.placeGUI()

	def placeGUI(self):
		self.copy_btn.place(anchor="center", relx=0.5, rely=0.4, width=170, height=40)
		self.date_label.place(anchor="center", relx=0.5, rely=0.6,)
		self.reg_btn.place(anchor="center", relx=0.5, rely=0.85, width=380, height=50)
		self.key_entry.place(anchor="center", relx=0.5, width=380, height=40, rely=0.15)
		self.update()

	def flip(self):
		if self.alive:	
			try: self.update()
			except: pass
		else:
			sys.exit()