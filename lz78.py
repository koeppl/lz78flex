#!/usr/bin/env python3
""" lz78 parsing and flexible lz78 parsing """
# pylint: disable=bad-indentation,line-too-long,invalid-name

import sys
import logging
import argparse
import common as C
import json




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
			# logging.debug('[78] factor (%d, %s) : %s -> factor id %d, progress: [%d/%d, %f%%] z=%d',  parent_id, current_factor[-1], current_factor, len(dictionary) + 1, textpos, len(text), textpos*100.0/len(text), len(factorization))
			C.log_factor('78', parent_id, current_factor[-1], current_factor, len(dictionary) + 1, textpos, len(text), len(factorization))


			current_factor = ''
			parent_id=0
		else:
			parent_id = dictionary[current_factor]
	return factorization


def decode_lz78(factorization) -> str:
	""" decode factorization """
	string = ''
	factors = ['']
	for (_,(parent_id, char)) in enumerate(factorization):
		factor = factors[parent_id] + char
		string += factor
		factors.append(factor)
	return string

def test_lz78_instance(text):
	""" test LZ78 factorization"""
	phrases = lz78(text)
	assert text == decode_lz78(phrases), f'decoding-mismatch:\n{text} [original] not equal to:\n{decode_lz78(phrases)} (decoded)'


def test_lz78():
	""" test LZ78 factorization """
	for text in C.test_text_collections():
		test_lz78_instance(text)

if __name__ == '__main__':
	C.main(
			description='LZ78 Compressor',
			name='LZ78',
			can_decode=True,
			compressor=lz78,
			decoder=decode_lz78,
			decodetester=lambda x,_ : decode_lz78(x),
			tester=test_lz78)
