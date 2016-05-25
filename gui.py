from tkinter.ttk import *
from tkinter import *
from tkinter import font
from browser import b

class GUI(Frame):

	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent)
		self.parent = parent
		self.init_ui()

	def init_ui(self):
		global browser

		self.parent.title('Python Music Player')
		self.pack(fill = BOTH, expand = 1)

		small_font = font.Font(size = 14)

		self.lb = Listbox(self, font=small_font)
		self.lb.pack(fill = BOTH, expand = 1)

		self.lb.insert(END, 'Back')
		for item in b.curlist():
			self.lb.insert(END, item)

		self.lb.bind('<<ListboxSelect>>', self.on_select)

	def on_select(self, val):
		newlist = []

		if val.widget.get(val.widget.curselection()[0]) == 'Back':
			newlist = b.back()
		else:
			newlist = b.select(val.widget.curselection()[0] - 1)
		
		self.lb.delete(0, END)
		self.lb.insert(END, 'Back')
		for item in newlist:
			self.lb.insert(END, item)

def main():
	root = Tk()
	app = GUI(root)
	root.geometry('300x250+300+300')
	root.mainloop()

if __name__ == '__main__':
	main()
