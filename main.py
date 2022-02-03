# Name: main.py
# Author: Darrion Munroe
# Date: Oct 7 2021
# Notes: The main program for RhymeLight.

import fitz
from fpdf import FPDF
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import	messagebox
from tkinter.scrolledtext import ScrolledText
from big_phoney import PhoneticDictionary
from lineNumbers import lineNumbers
from rhymeLight import *

# Initialize Phonetic Dictionary, BigPhoney phoneme prediction model, and syllable list
phonizer = PhoneticDictionary()

# Create tkinter GUI with given size and title
root = Tk()
root.title("RhymeLight")
root.geometry("1280x720")

# Refresh the line numbers
def refresh(event):
	line_nums.build()
	# Highlight rhymes in text widget
	lyrics = text_field.get("1.0", "end")
	syllables = syllabank(lyrics, phonizer)
	rhymeLight(text_field, syllables, phonizer)

# Clear the current text widget and reset title
def newFile():
	text_field.delete("1.0", "end")
	root.title("RhymeLight")

# Open a text file and import text to text widget
def openFile():
	# Clear the text widget
	text_field.delete("1.0", "end")
	
	# Get file name and add it to program title
	file_name = filedialog.askopenfilename(initialdir = "C:", title = "Open File", 
		filetypes = [("Text Files", "*.txt"), ("All Files", "*.*")])

	# Check if user canceled opening file
	if file_name == '':
		return
	
	# Open the file (Done in one read() since song lyrics tend to be quite small)
	file = open(file_name, 'r')
	new_title = file_name.split("/")[-1] + " - RhymeLight"
	root.title(new_title)
	text = file.read()
	text_field.insert("end", text)

	# Apply rhyme highlighting
	syllables = syllabank(text, phonizer)
	rhymeLight(text_field, syllables, phonizer)
	line_nums.build()

# Allow user to save text file and name
def saveAsFile():
	# Create dialog window for user to save the file
	file = filedialog.asksaveasfile(mode = 'w', defaultextension = ".txt", filetypes = [("Text Files", "*.txt"), ("All Files", "*.*")])
	
	# Check if user hit the cancel button
	if file is None:
		return
	
	# Write text to file and close
	text = text_field.get("1.0", "end")
	file.write(text)
	file.close()

def export():
	# Get file name from user 
	file = filedialog.asksaveasfilename(defaultextension = ".pdf", filetypes = [("PDF", "*.pdf")])
	file_name = file.split("/")[-1]
	
	# Write text to file
	text = text_field.get("1.0", "end")
	syllables = syllabank(text, phonizer)
	pdf = FPDF('P', 'mm', 'Letter')
	pdf.set_font("helvetica", '', 16)
	pdf.add_page()
	pdf.multi_cell(150, 10, text)
	pdf.output(file_name)
	pdf.close()

def readme():
	messagebox.showinfo("Help", "RhymeLight will automatically highlight your rhyme scheme as you write")
	
def readme2():
	messagebox.showinfo("Rhyme Undetected", "The RhymeLight team is always working to improve the rhyme detection of the software. Some words not found in dictionaries may not be detected")

# Create text field with scrollbar widget
text_field = ScrolledText(root, width = 100, height = 100, 
	font = ("helvetica", 16), bg = "#2C2C2C", fg = "#909090")
# Bind events to refresh line numbers
text_field.bind("<MouseWheel>", refresh)
text_field.bind("<KeyRelease>", refresh) 
text_field.bind("<KeyPress>", refresh)

# Create a menu bar
menu_bar = Menu(root)
root.config(menu = menu_bar)

# File menu for saving, opening and exporting
file_menu = Menu(menu_bar)
menu_bar.add_cascade(label = "File", menu = file_menu)
file_menu.add_command(label = "New File", command=newFile)
file_menu.add_separator()
file_menu.add_command(label = "Open", command=openFile)
file_menu.add_separator()
file_menu.add_command(label = "Save as...", command=saveAsFile)
file_menu.add_separator()
file_menu.add_command(label = "Export", command=export)

# Help menu to act as a guide for the user
help_menu = Menu(menu_bar)
menu_bar.add_cascade(label = "Help", menu = help_menu)
help_menu.add_command(label = "Help", command=readme)
help_menu.add_separator()
help_menu.add_command(label = "Rhyme Undetected", command=readme2)

# Create line numbers
line_nums = lineNumbers(root, width = 35)
line_nums.connect(text_field)
line_nums.pack(fill = Y, side = "left")

# Pack text later so the numbers are on top
text_field.pack(fill = BOTH, expand = True)


# Begins the program loop
root.mainloop()
