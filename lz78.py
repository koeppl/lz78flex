#!/usr/bin/env python3
""" abook replacement """
# pylint: disable=bad-indentation,line-too-long,invalid-name

import sys
import logging

def lz78(text):
	dictionary = {}
	parent_id = 0
	factor = ''
	for char in text:
		factor += char
		if factor not in dictionary:
			dictionary[factor] = len(dictionary) + 1
			logging.debug(f'({parent_id},"{factor[-1]}") : {factor} -> {dictionary[factor]}')
			factor = ''
		else:
			parent_id = dictionary[factor]
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

		first_length = len(potential_factor)+1
		second_length = 0
		if first_length < len(text[textpos:]):
			for i in range(1,len(potential_factor)+2):
				potential_subsequent_factor = longest_prefix(dictionary, text[textpos+i:])
				if len(potential_subsequent_factor) >= second_length:
					first_length = i
					second_length = len(potential_subsequent_factor)

		first_factor = text[textpos:textpos+first_length]
		if first_factor not in dictionary:
			dictionary[first_factor] = len(dictionary) + 1
		parent_id = dictionary[first_factor[:-1]] if len(first_factor) >= 2 else 0
		logging.debug(f'({parent_id},"{first_factor[-1]}") : {first_factor} -> {dictionary[first_factor]}')
		textpos += first_length
	return len(dictionary)


if __name__ == '__main__':
	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
	filename='stdin'
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		with open(filename,encoding='utf-8') as file:
			text = file.read()
	else:
		text = sys.stdin.read()

	# text='abababcabcdabcdeabcdefabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefg'
	logging.debug('78')
	lz78phrases = lz78(text)
	logging.debug('flex')
	flex_phrases = lz78flex(text)
	print(f'file={filename} length={len(text)} factors78={lz78phrases} factorsflex={flex_phrases}')
