# Installation
RhymeLight has the following requirements:
-	Python 3.7 (later versions will not work)
-	fitz python module
-	big-phoney python module

Both modules can be installed using python’s pip tool by using the following commands:

  *pip install fitz*

  *pip install big-phoney*

After installing these modules, you should be able to run the main.py file. The other files are libraries that are used by main.py.

# How does RhymeLight work?
RhymeLight.py acts as a library of functions that were used to implement rhyme highlighting to a word processor created with the tkinter python module. The syllabank(text, phoDict) function takes the lyrics in as a string called text and accepts the dictionary of phonemes as phoDict. This function goes through text and finds all phonemes that are repeated and returns them as a list. 

The function rhymeLight(textWidget, syllaList, phoDict) takes in the text widget as textWidget, the list of repeated phonemes as syllaList, and the phonetic dictionary as phoDict. After a repeated phoneme is found within the widget it is then highlighted. These two functions are called upon every key release and when the scroll wheel is used. This is because each of these actions refresh the highlighting and line numbers. Tkinter will not apply the highlighting if the characters are not on-screen when the function is called so having the entire project refresh frequently is important.

# Color Assignment
Each phoneme is assigned a six-bit hex value where every two characters represent a value for Red, Green, and Blue. This value is used as the color that the phoneme will be highlighted. These hex values are made by randomly selecting from a list of points ranging from 00 to FF. This list was created by finding points in this range that were fairly well distributed and then removing values that conflict with the color of the text or background. The list ended up having seven possible values, which allows for 210 different colors when drawing from the list without repetition within one hex value. 

Euclidian distance calculations were used to determine how far apart the values in the list should be. This involves finding the change in red, green, and blue values and then taking the square root of the summation of the squares of these changes. 
