import gui
import sys
import os

def restart_program():
	python = sys.executable
	os.execl(python, python, *sys.argv)

gui.main()
