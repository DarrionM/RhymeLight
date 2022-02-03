from tkinter import *
from tkinter import ttk
from random import randint 
import math
import random

# Global color lists
colorList = []
vals = ['00', '45', '5c', '90', 'b8', 'dd', 'ff']

# Global list of problematic characters
punc = [',' , '.' , '"', '!', '?', '(', ')']

# Repopulat Hex Values for color generation
def resetVals():
	global vals
	vals = ['00', '45', '5c', '90', 'b8', 'dd', 'ff']

# Create and return list of repeated phonemes
def syllabank(text, phoDict):
	syllaList = []
	syllALL = []
	# Split text into list of words
	wordList = text.split()
	for word in wordList:
		newWord = ""
		for char in word:
			if char not in punc:
				# replace "in'" suffix with "ing"
				if char == "'" and char == word[-1] and word[-1:-4:-1] == "'ni":
					newWord += 'g'
				else:
					newWord += char
		# Look up phonemes for word
		phonemes = phoDict.lookup(newWord)
		if phonemes != None:
			phonemeList = phonemes.split()
			for phoneme in phonemeList:
				if len(phoneme) == 1:
					pass
				# Determine if phoneme is a duplicate and place into appropriate list
				elif phoneme not in syllALL:
					syllALL.append(phoneme)
				elif phoneme not in syllaList:
					syllaList.append(phoneme)
	return syllaList

# Return count of characters before word
def characterCount(words, index):
	count = 0
	i = 0
	while i < index:
		count += (len(words[i]) + 1)
		i += 1
	return str(count)

def randColor():
	global vals
	colorVal = "#"
	while len(colorVal) < 7:
		if len(vals) < 3:
			resetVals()
		random.shuffle(vals)
		colorVal += vals.pop() + vals.pop() + vals.pop()
		for color in colorList:
			if colorVal in color:
				colorVal = "#"
	colorList.append(colorVal)

# Create tags for phonemes
def colorConfig(textWidget, syllaList):
	for tag in textWidget.tag_names():
		textWidget.tag_delete(tag)
	# Create list of colors
	while len(colorList) < len(syllaList):
		randColor()
	for i in range(0, len(syllaList)):
		# colorIndex = i % len(colorList)
		textWidget.tag_config(syllaList[i], background= colorList[i])

# Highlight word based on phonemes repeated
def highlight(textWidget, syllaList, lineNum, startTag, wordLen, prefix):
	if prefix:
		startTag = str(int(startTag) + 1)
	if len(syllaList) == 1:
		endingTag = int(startTag) + wordLen
		textWidget.tag_add(syllaList, (lineNum  + '.' + startTag), 
			(lineNum  + "." + str(endingTag)))
	syllaList = list(dict.fromkeys(syllaList))
	tagLen = round(float(wordLen / len(syllaList)))
	startingTag = int(startTag)
	endingTag = startingTag + tagLen
	for i in range(0, len(syllaList)):
		if i == (len(syllaList) - 1):
			endingTag = startingTag + wordLen - (i * tagLen)
		textWidget.tag_add(syllaList[i], (lineNum  + '.' + str(startingTag)), (lineNum  + "." + str(endingTag)))
		startingTag = endingTag
		endingTag = startingTag + tagLen
	
# Find words containing repeated phonemes and highlight them 
def rhymeLight(textWidget, syllaList, phoDict):
	# Move index to the front and prepare tags
	i = textWidget.index("@0,0")
	colorConfig(textWidget, syllaList)
	while True:
		# Calculate the line number
		dline = textWidget.dlineinfo(i)
		# Check if index is at the end
		if dline is None:
			break
		# Get line number and text from line
		lineNum = str(i).split(".")[0]
		textLine = textWidget.get(lineNum + ".0", lineNum + ".0+1line")
		textLine = textLine.split()
		# Check each word in line
		for index in range(0, len(textLine)):
			# Lookup phonemes in word
			word = ""
			for char in textLine[index]:
				if char not in punc:
					# replace "in'" suffix with "ing"
					if char == "'" and char == textLine[index][-1] and textLine[index][-1:-4:-1] == "'ni":
						word += 'g'
					else:
						word += char
			phonemes = phoDict.lookup(word)
			if phonemes != None:
				prefix = False
				# change phonemes to list
				phonemes = phonemes.split()
				matches = []
				# Check if phonemes match
				for newSyll in phonemes:
					if newSyll in syllaList:
						matches.append(newSyll)
				# Highlight text if any match
				if len(matches) > 0:
					if textLine[index][0] in ['"', "("]:
						prefix = True
					highlight(textWidget, matches, lineNum, 
					characterCount(textLine, index), len(word), prefix)
		i = textWidget.index("%s+1line" % i)

