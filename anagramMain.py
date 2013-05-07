from Anagram import *

"""
Main function for the program. The Anagram initialization takes input in the
format: 0: "word/phrase", 1: dictionary file (in current directory)
2: list of words that must be in the anagram, 3: list of words to exclude from the anagram,
and 4: maximum number of words in the anagram (0 = unlimited)
Example: Anagram("Richard Neal", "english.txt", ["dire"], ["card"], 3)
will generate all anagrams for Mark LeBlanc from the dictionary english.txt that include the word
dire, don't include the word card, and are 3 words or less.
"""
def main():
	DICTIONARY = "english.txt"
	# Get the input word or phrase
	inputstring = raw_input("Please enter a word or phrase for which to find anagrams: ")
	
	# Check to see if the user wants to use advanced features.
	advanced_options = raw_input("Would you like to enter advanced options for the anagram finder? Enter true or false: ")
	if advanced_options.lower() == "true":
		# If so, ask for lists of the includes and excludes, and a number for max words.
		include_words = raw_input("Please enter a list of comma-separated words that must be in the anagram (Hit enter to ignore): ")
		exclude_words = raw_input("Please enter a list of comma-separated words that must NOT be in the anagram (Hit enter to ignore): ")
		maximum_length = raw_input("Please enter a maximum number of words for each anagram (Hit enter to ignore): ")
		
		# Since I want the user to be able to hit enter for ignoring the options, I use raw input,
		# which I must try to cast to an int in the try/except block below
		try:
			maxlength = int(maximum_length)
		except:
			maxlength = 0
		# Add the inputs to the Anagram class
		a = Anagram(inputstring, DICTIONARY, filter(None, include_words.split(', ')), filter(None, exclude_words.split(', ')), maxlength)
	
	# If the user just wanted basic functions, do so
	else:
		a = Anagram(inputstring, DICTIONARY)

	# Go crazy generating anagrams
	a.findAnagrams()


if __name__ == '__main__':
	main()