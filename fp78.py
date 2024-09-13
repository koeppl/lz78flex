#!/usr/bin/env python3
""" lz78 parsing and flexible lz78 parsing """
# pylint: disable=bad-indentation,line-too-long,invalid-name

import logging
import common as C


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
		C.log_factor('fp', parent_id, current_factor[-1], current_factor, len(dictionary) + 1, textpos, len(text), len(factorization))

		textpos += current_length
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

def test_fp78_instance(text):
	""" test FP78 factorization"""
	phrases = fp78(text)
	assert text == decode_fp78(phrases, text), f'decoding-mismatch:\n{text} [original] not equal to:\n{decode_fp78(phrases,text)} (decoded)'

def test_fp78():
	""" test factorizations """
	for text in C.test_text_collections():
		test_fp78_instance(text)

if __name__ == '__main__':
	C.main(
			description='flexible parsing LZ78 Compressor',
			name='FP78',
			can_decode=False,
			compressor=fp78,
			decoder=decode_fp78,
			decodetester=decode_fp78,
			tester=test_fp78)
