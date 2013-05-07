# The defaultdict has a default value for all keys, which speeds up lookup time considerably.
from collections import defaultdict 

"""
Summary: Give me a word/phrase and with a dictionary to parse I will move the whole world!
Or generate a bunch of anagrams. This is the main class for the anagram. Holds the methods 
I will use to generate said anagram.
"""
class Anagram:
	""" Precondition: Takes as arguments a string for which to find anagrams, name of
	the dictionary file, list of words that must be in the anagram, list of words that 
	must not be in the anagram, and a maximum number of words in the anagram.
	Postcondition: Generates a trie of all the words in the dictionary file save the ones
	to be excluded. Additionally, strips the string and makes it a class variable
	Summary: Preprocessing for the anagram finder. Gets everything ready for the dictionary
	trie to be traversed.
	"""
	def __init__(self, inputstring, filename, include=[], exclude=[], maxlength=0):
		# This makes the inputstring lowercase and gets rid of any non-alphabetic characters
		self.string = ''.join(char for char in inputstring.lower() if 97 <= ord(char) <= 122)

		# Open the dictionary file, and add class variables for the inputstring and filename
		dictionaryFile = open(filename, 'r')
		self.filename = filename
		self.inputstring = inputstring

		# Make a list of all the characters in the processed string, and remove any of them that
		# fall in the list of words to include (easiest way of doing it, also reduces lookup times)
		stringlist = list(self.string)
		for word in include:
			for letter in word:
				if letter in stringlist:
					stringlist.remove(letter)
				else:
					raise Exception("There weren't enough/any of the letter {0} in {1}".format(letter, self.inputstring))
		
		# Join the parsed string list together
		self.string = ''.join(stringlist)

		# Create a new trie, and put all the dictionary words into it.
		self.trie = Trie(include, maxlength)
		for word in dictionaryFile:
			cleanword = word.strip().lower()
			if cleanword not in exclude:
				self.trie.insert(cleanword)

	""" Precondition: Expects init to have been run.
	Postcondition: Prints to stdout an exhaustive list of all the dictionary 
	word anagrams of the input string.
	Summary: Starts the recursive traversing of the trie.
	"""
	def findAnagrams(self):
		# Create a dictionary with each unique letter of the input string as key, and its count as the value.
		# This allows me to look up whether a letter is still in the input string really easily.
		chars = defaultdict(int)
		for char in set(self.string):
			chars[char] = self.string.count(char)

		# Find all anagrams, with the root of the trie as the base.
		self.trie.anagramization(chars, self.trie.root, [], len(self.string), "")

		# Final output.
		print("There were {0} unique anagrams made from '{1}' using the dictionary '{2}'.".format(self.trie.count, self.inputstring, self.filename))

"""
Summary: The Trie class holds all the words from the input dictionary as nodes made of its letters.
"""
class Trie:
	""" Precondition: List of words to include and the maximum length of the anagram.
	Postcondition: Initializes some class variables.
	Summary: Initializes the trie with some variables I'll need later.
	"""
	def __init__(self, include, maxlength):
		self.root = Node('')
		self.count = 0
		self.maxlength = (maxlength if maxlength else float('inf'))
		self.include = include

	""" Precondition: Initialized trie, and word to be inserted into the trie.
	Postcondition: The word is now in the trie.
	Summary: Adds a word to the trie letter by letter, giving its leaf node the leafiness property.
	"""
	def insert(self, word):
		# Adds a word to the trie, appending letters as it goes if necessary.
		current = self.root
		for letter in word:
			child = current.findChild(letter)
			if not child:
				child = Node(letter)
				current.addChild(letter, child)
			current = child

		# Gives the end node the leaf property so I know it completes a word.
		current.leafiness = True

	""" Precondition: Completed trie, and a defaultdict of chars, the current node, the running
	progress, maximum length of the word, and previous word all as inputs.
	Postcondition: This specific call will print out an anagram if it completes one.
	Summary: Recursive function for generating the anagrams. Traverses the trie letter by letter.
	"""
	def anagramization(self, chars, current, progress, wordlength, previousWord):
		# If the current node is a leaf
		if current.leafiness:
			# Join the running list of the traversal together to form a string
			word = ''.join(progress)
			# If the current word is not earlier in the alphabet than the previous word (gets rid of rearranged anagrams)
			if word.split()[-1] >= previousWord:
				# If the length of the running traversal progress is equal to the length of the original word, output it
				if len(''.join(word.split())) == wordlength:
					self.count += 1
					print("{0:4}: {1}".format(self.count, ' '.join(sorted(self.include + word.split()))))
				elif len(self.include + word.split()) < self.maxlength:
					# Otherwise, keep recursing, but go back to the root so as to start with a new word
					self.anagramization(chars, self.root, progress + [' '], wordlength, word.split()[-1])
		# For each child of the current node (since it's a dictionary and I need both the keys and values, I use iteritems())
		for letter, node in current.children.iteritems():
			# Get the count of the letter in the current word, and if it's non-zero...
			count = chars[letter]
			if count:
				# Temporarily drop the count of the letter by one and keep recursing
				chars[letter] -= 1
				self.anagramization(chars, node, progress + [letter], wordlength, previousWord)
				chars[letter] += 1

"""
Summary: Basic node in the trie, has a letter, dictionary of children, and a leaf property.
"""
class Node:
	def __init__(self, letter):
		self.letter = letter
		self.children = {}
		self.leafiness = False

	def addChild(self, letter, child):
		self.children[letter] = child

	def findChild(self, letter):
		return self.children.get(letter, None)