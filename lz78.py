#!/usr/bin/env python3
""" lz78 parsing and flexible lz78 parsing """
# pylint: disable=bad-indentation,line-too-long,invalid-name

import sys
import logging
import typing
from itertools import product


def lz78_timestamped_dict(text) -> dict:
	""" lz78 parsing dictionary computation, dict stores pairs of factor_id and the ending position when the factor was created """
	dictionary = {}
	parent_id = 0
	current_factor = ''
	num_factors = 0
	for (textpos,char) in enumerate(text):
		current_factor += char
		if current_factor not in dictionary or textpos+1 == len(text):
			if current_factor not in dictionary:
				dictionary[current_factor] = (len(dictionary) + 1, textpos)
			logging.debug('[78T] factor (%d, %s) : %s -> factor id %d, progress: [%d/%d, %f%%] z=%d',  parent_id, current_factor[-1], current_factor, len(dictionary) + 1, textpos, len(text), textpos*100.0/len(text), num_factors)
			current_factor = ''
			num_factors += 1
			parent_id=0
		else:
			parent_id = dictionary[current_factor][0]
	return dictionary

def longest_timestamped_prefix_length(dictionary, text, startposition) -> int:
	""" find the longest prefix of text in dictionary """
	prefix = ''
	for char in text[startposition:]:
		prefix += char
		if prefix not in dictionary:
			return len(prefix)-1
		if dictionary[prefix][1] >= startposition:
			return len(prefix)-1
	return len(prefix)


def fp78(text):
	""" flexible parsing (FP) of lz78 """
	dictionary = lz78_timestamped_dict(text)
	textpos = 0
	factorization = []
	while textpos < len(text):
		potential_factor_length = longest_timestamped_prefix_length(dictionary, text, textpos)+1
		current_length = potential_factor_length
		combined_length = 0
		if current_length < len(text[textpos:]):
			for i in range(1,potential_factor_length+1):
				potential_subsequent_factor_length = longest_timestamped_prefix_length(dictionary, text, textpos+i)
				if potential_subsequent_factor_length+i >= combined_length:
					current_length = i
					combined_length = potential_subsequent_factor_length+i
		current_factor = text[textpos:textpos+current_length]
		# if current_factor not in dictionary:
		# 	dictionary[current_factor] = len(dictionary) + 1
		parent_id = dictionary[current_factor[:-1]][0] if len(current_factor) >= 2 else 0

		factorization.append((parent_id, current_factor[-1]))
		logging.debug('[FP78] factor (%d, %s) : %s -> factor id %d, progress: [%d/%d, %f%%] z=%d',  parent_id, current_factor[-1], current_factor, len(dictionary) + 1, textpos, len(text), textpos*100.0/len(text), len(factorization))

		textpos += current_length
	return factorization



def lz78(text):
	""" lz78 parsing """
	dictionary = {}
	parent_id = 0
	current_factor = ''
	factorization = []
	for (textpos,char) in enumerate(text):
		current_factor += char
		if current_factor not in dictionary or textpos+1 == len(text):
			dictionary[current_factor] = len(dictionary) + 1
			factorization.append((parent_id, current_factor[-1]))
			logging.debug('[78] factor (%d, %s) : %s -> factor id %d, progress: [%d/%d, %f%%] z=%d',  parent_id, current_factor[-1], current_factor, len(dictionary) + 1, textpos, len(text), textpos*100.0/len(text), len(factorization))
			current_factor = ''
			parent_id=0
		else:
			parent_id = dictionary[current_factor]
	return factorization

def longest_prefix_length(dictionary, text) -> int:
	""" find the longest prefix of text in dictionary """
	prefix = ''
	for char in text:
		prefix += char
		if prefix not in dictionary:
			return len(prefix)-1
	return len(prefix)


def fpa78(text):
	""" alternative flexible parsing (FPA) of lz78 """
	dictionary = {}
	textpos = 0
	factorization = []
	while textpos < len(text):
		potential_factor_length = longest_prefix_length(dictionary, text[textpos:])+1
		current_length = potential_factor_length
		combined_length = 0
		if current_length < len(text[textpos:]):
			for i in range(1,potential_factor_length+1):
				potential_subsequent_factor_length = longest_prefix_length(dictionary, text[textpos+i:])
				if potential_subsequent_factor_length+i >= combined_length:
					current_length = i
					combined_length = potential_subsequent_factor_length+i
		assert 0 < current_length <= potential_factor_length

		# add the greedy LZ78 phrase
		dictionary[text[textpos:textpos+potential_factor_length]] = len(dictionary) + 1
		current_factor = text[textpos:textpos+current_length]
		# if current_factor not in dictionary:
		# 	dictionary[current_factor] = len(dictionary) + 1
		parent_id = dictionary[current_factor[:-1]] if len(current_factor) >= 2 else 0
		textpos += current_length
		factorization.append((parent_id, current_factor[-1]))
		# logging.debug('FPA (%d, %s) : %s -> %d [%d/%d]',  parent_id, current_factor[-1], current_factor, dictionary[current_factor], textpos, len(text))
		logging.debug('[FPA] factor (%d, %s) : %s -> factor id %d, progress: [%d/%d, %f%%] z=%d',  parent_id, current_factor[-1], current_factor, len(dictionary) + 1, textpos, len(text), textpos*100.0/len(text), len(factorization))
	return factorization


def decode_fp78(factorization, text) -> str:
	""" decode FP78 factorization """
	dictionary = lz78_timestamped_dict(text)
	factors = ['']*(len(dictionary)+1)
	for (key,pair) in dictionary.items():
		factors[pair[0]] = key
	string = ''
	for (_,(parent_id, char)) in enumerate(factorization):
		factor = factors[parent_id] + char
		string += factor
	return string

def decode_fpa78(factorization, text) -> str:
	""" decode FPA78 factorization """
	string = ''
	dictionary = {}
	factors = ['']
	for (_,(parent_id, char)) in enumerate(factorization):
		ref_length = longest_prefix_length(dictionary, text[len(string):])+1
		dictionary[text[len(string):len(string)+ref_length]] = len(factors)
		factors.append(text[len(string):len(string)+ref_length])

		factor = factors[parent_id] + char
		string += factor
	return string


def decode_78(factorization) -> str:
	""" decode factorization """
	string = ''
	factors = ['']
	for (_,(parent_id, char)) in enumerate(factorization):
		factor = factors[parent_id] + char
		string += factor
		factors.append(factor)
	return string


def test_text_collection() -> typing.List[str]:
	""" test text collection """
	return [''.join(p) for p in product('ab', repeat=10)] + [''.join(p) for p in product('a', repeat=33)] + [
			'aaaaaaaaaaaaaaa', 'abababcabcdabcdeabcdefabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefg',
			'abababcabcdabcdeabcdefabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefg',
			'abababcabcdabcdeabcdefabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefg',
			'abababcabcdabcdeabcdefabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefg',
			]+ [
    "abcd",           # All four characters
    "aabbccdd",       # Repeated pattern of all characters
    "ababab",         # Alternating characters
    "cccc",           # Same character repeated
    "abcabc",         # Repeated sequence of 'abc'
    "dddd",           # Only 'd' repeated
    "aabccda",        # Mixed characters
    "abcdabcdabcd",   # Repeated longer pattern
    "a"*50,           # Long string with only 'a'
    "b"*50,           # Long string with only 'b'
    "abc"*10,         # Repeated 'abc' pattern
    "aaabbbcccddd",   # Grouped repeating pattern
		]


def test_fp78(text):
	""" test FP78 factorization"""
	phrases = fp78(text)
	assert text == decode_fp78(phrases, text), f'decoding-mismatch:\n{text} [original] not equal to:\n{decode_fp78(phrases,text)} (decoded)'

def test_fpa78(text):
	""" test LZ78 factorization"""
	phrases = fpa78(text)
	assert text == decode_fpa78(phrases,text), f'decoding-mismatch:\n{text} [original] not equal to:\n{decode_fpa78(phrases,text)} (decoded)'

def test_78(text):
	""" test LZ78 factorization"""
	phrases = lz78(text)
	assert text == decode_78(phrases), f'decoding-mismatch:\n{text} [original] not equal to:\n{decode_78(phrases)} (decoded)'

def test_factorizations():
	""" test factorizations """
	for text in test_text_collection():
		test_78(text)
		test_fpa78(text)
		test_fp78(text)

if __name__ == '__main__':
	logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
	filename='stdin'
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		with open(filename,encoding='utf-8') as file:
			inputtext = file.read()
	else:
		inputtext = sys.stdin.read()

	if logging.getLogger().isEnabledFor(logging.DEBUG):
		logging.debug('BEGIN TEST')
		test_factorizations()
		logging.debug('END TEST')

	logging.debug('78')
	lz78phrases = lz78(inputtext)
	if logging.getLogger().isEnabledFor(logging.DEBUG):
		assert inputtext == decode_78(lz78phrases), f'{inputtext} != {decode_78(lz78phrases)}'

	logging.debug('fpa')
	fpa_phrases = fpa78(inputtext)
	if logging.getLogger().isEnabledFor(logging.DEBUG):
		assert inputtext == decode_fpa78(fpa_phrases,inputtext) , f'{inputtext} != {decode_fpa78(fpa_phrases,inputtext)}'

	logging.debug('fp')
	fp_phrases = fp78(inputtext)
	if logging.getLogger().isEnabledFor(logging.DEBUG):
		assert inputtext == decode_fp78(fp_phrases,inputtext), f'{inputtext} != {decode_fp78(fp_phrases, inputtext)}'
	print(f'file={filename} length={len(inputtext)} 78={len(lz78phrases)} fpa={len(fpa_phrases)} fp={len(fp_phrases)}')


# inputtext='abababcabcdabcdeabcdefabcdefgabcdefgabcdefgabcdefgabcdefgabcdefgabcdefg'
