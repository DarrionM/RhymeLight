import tkinter

# Class for line numbers in tkinter
class lineNumbers(tkinter.Canvas):
	# Constructor for lineNumbers
	def __init__(self, *args, **kwargs):
		tkinter.Canvas.__init__(self, *args, **kwargs)
		self.textWidget = None
	# Connect lineNumbers to a text widget
	def connect(self, textWidget):
		self.textWidget = textWidget
	# Draw line numbers
	def build(self, *args):
		# Reset current numbers
		self.delete("all")
		i = self.textWidget.index("@0,0")
		# Determine number for each line and draw the numbers to canvas
		while True:
			# Calculate the line number
			dline = self.textWidget.dlineinfo(i)
			if dline is None:
				break
			y = dline[1]
			linenum = str(i).split(".")[0]
			# Draw line number to canvas
			self.create_text(5, y, anchor = "nw", text = linenum, 
				font = ("Berlin Sans FB", 16))
			i = self.textWidget.index("%s+1line" % i)