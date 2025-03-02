# File Name: print_from_file.py
# Assignment: Homework 1
# Status: Abandoned due to file /usr/share/dict/words not being available on 3/1/2025
# Problem: 
# Write a script to read in /usr/share/dict/words and print just the last 10 lines of the 
# file. Write another script to only print words beginning with the letters “pyt”.

# Function: next_word()
#  Returns next word from a text file

# def next_word():
	 

# def print_string():
	

def read_from_words(filename):
	# Read individual words from a text file and return them as a list.
	words = []
	try:
		with open(filename, 'r', encoding='utf-8') as file:
			for line in file:
				words.extend(line.split())  # Split line into words and add to list
	except FileNotFoundError:
		print(f"Error: The file '{filename}' was not found.")
	return words

# Example usage:
filename = "/usr/share/dict/words"  # Replace with your file name
word_list = read_from_words(filename)
print(word_list)

