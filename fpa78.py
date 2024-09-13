#!/usr/bin/env python3
""" lz78 parsing and flexible lz78 parsing """
# pylint: disable=bad-indentation,line-too-long,invalid-name

import logging
import common as C

# def longest_prefix_length(dictionary, text) -> int:
# 	""" find the longest prefix of text in dictionary """
# 	prefix = ''
# 	for char in text:
# 		prefix += char
# 		if prefix not in dictionary:
# 			return len(prefix)-1
# 	return len(prefix)


def fpa78(text):
	""" alternative flexible parsing (FPA) of lz78 """
	dictionary = {}
	textpos = 0
	factorization = []
	while textpos < len(text):
		potential_factor_length = C.longest_timestamped_prefix_length(dictionary, text, textpos)+1
		current_length = potential_factor_length
		combined_length = 0
		if current_length < len(text[textpos:]):
			for i in range(1,potential_factor_length+1):
				potential_subsequent_factor_length = C.longest_timestamped_prefix_length(dictionary, text, textpos+i)
				if potential_subsequent_factor_length+i >= combined_length:
					current_length = i
					combined_length = potential_subsequent_factor_length+i
		assert 0 < current_length <= potential_factor_length

		# add the greedy LZ78 phrase
		dictionary[text[textpos:textpos+potential_factor_length]] = [len(dictionary) + 1, textpos+potential_factor_length-1]
		current_factor = text[textpos:textpos+current_length]
		# if current_factor not in dictionary:
		# 	dictionary[current_factor] = len(dictionary) + 1
		parent_id = dictionary[current_factor[:-1]][0] if len(current_factor) >= 2 else 0
		textpos += current_length
		factorization.append((parent_id, current_factor[-1]))
		C.log_factor('fpa', parent_id, current_factor[-1], current_factor, len(dictionary) + 1, textpos, len(text), len(factorization))

	return factorization

def decode_fpa78(factorization, text) -> str:
	""" decode FPA78 factorization """
	string = ''
	dictionary = {}
	factors = ['']
	for (_,(parent_id, char)) in enumerate(factorization):
		ref_length = C.longest_timestamped_prefix_length(dictionary, text, len(string))+1
		dictionary[text[len(string):len(string)+ref_length]] = [len(factors), len(string)+ref_length-1]
		factors.append(text[len(string):len(string)+ref_length])

		factor = factors[parent_id] + char
		string += factor
	return string

def test_fpa78_instance(text):
	""" test LZ78 factorization"""
	phrases = fpa78(text)
	assert text == decode_fpa78(phrases,text), f'decoding-mismatch:\n{text} [original] not equal to:\n{decode_fpa78(phrases,text)} (decoded)'


def test_fpa78():
	""" test factorizations """
	for text in C.test_text_collections():
		test_fpa78_instance(text)

if __name__ == '__main__':
	C.main(
			description='alternative flexible parsing LZ78 Compressor',
			name='FPA78',
			can_decode=False,
			compressor=fpa78,
			decoder=decode_fpa78,
			decodetester=decode_fpa78,
			tester=test_fpa78)
