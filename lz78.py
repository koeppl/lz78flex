#!/usr/bin/env python3
""" lz78 parsing and flexible lz78 parsing """
# pylint: disable=bad-indentation,line-too-long,invalid-name

import sys
import logging

def lz78(text):
	""" lz78 parsing """
	dictionary = {}
	parent_id = 0
	current_factor = ''
	for char in text:
		current_factor += char
		if current_factor not in dictionary:
			dictionary[current_factor] = len(dictionary) + 1
			logging.debug('(%d, %s) : %s -> %d',  parent_id, current_factor[-1], current_factor, dictionary[current_factor])
			current_factor = ''
		else:
			parent_id = dictionary[current_factor]
	return len(dictionary)

def longest_prefix(dictionary, text):
	""" find the longest prefix of text in dictionary """
	prefix = ''
	for char in text:
		prefix += char
		if prefix not in dictionary:
			return prefix[:-1]
	return prefix



def lz78flex(text):
	""" flexible parsing of lz78 """
	dictionary = {}
	textpos = 0
	while textpos < len(text):
		potential_factor = longest_prefix(dictionary, text[textpos:])

		current_length = len(potential_factor)+1
		next_length = 0
		if current_length < len(text[textpos:]):
			for i in range(1,len(potential_factor)+2):
				potential_subsequent_factor = longest_prefix(dictionary, text[textpos+i:])
				if len(potential_subsequent_factor) >= next_length:
					current_length = i
					next_length = len(potential_subsequent_factor)

		current_factor = text[textpos:textpos+current_length]
		if current_factor not in dictionary:
			dictionary[current_factor] = len(dictionary) + 1
		parent_id = dictionary[current_factor[:-1]] if len(current_factor) >= 2 else 0
		logging.debug('(%d, %s) : %s -> %d',  parent_id, current_factor[-1], current_factor, dictionary[current_factor])
		textpos += current_length
	return len(dictionary)


if __name__ == '__main__':
	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
	filename='stdin'
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		with open(filename,encoding='utf-8') as file:
			inputtext = file.read()
	else:
		inputtext = sys.stdin.read()

	logging.debug('78')
	lz78phrases = lz78(inputtext)
	logging.debug('flex')
	flex_phrases = lz78flex(inputtext)
	print(f'file={filename} length={len(inputtext)} factors78={lz78phrases} factorsflex={flex_phrases}')


# inputtext='abababcabcdabcdeabcdefabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefg'
