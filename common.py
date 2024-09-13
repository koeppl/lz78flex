#!/usr/bin/env python3
""" common test data for LZ78 fact. algorithms """
# pylint: disable=bad-indentation,line-too-long,invalid-name

import sys
import typing
from itertools import product
import logging
import argparse
import json

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

def log_factor(name : str, parent_id, newchar, factor, factor_id, textposition, textlength, num_factors : int):
	if not logging.getLogger().isEnabledFor(logging.DEBUG):
		return
	logstring = f'[{name}] factor:{factor} id:{factor_id} pair:({parent_id}, {newchar}) progress: [{textposition}/{textlength}, {round(textposition*100.0/textlength,2)}%] z={num_factors}'
	logging.debug(logstring)

def test_text_collections() -> typing.List[str]:
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


def main(description : str, name : str, can_decode : bool, compressor, decoder, decodetester, tester):
	parser = argparse.ArgumentParser(description=description)
	parser.add_argument('-o', '--output', required=False, metavar='filename', type=str, nargs='?', help='output filename (otherwise STDOUT)')
	if can_decode:
		parser.add_argument('-d', '--decode', required=False, action='store_true', help='decode instead of compress')
	parser.add_argument('-q', '--quiet', required=False, action='store_true', help='do not produce a compressed output')
	parser.add_argument('-s', '--stats', required=False, action='store_true', help='output statistics on the number of factors')
	parser.add_argument('-t', '--test', required=False, action='store_true', help='runs tests and quit')
	parser.add_argument( '-l', '--loglevel', default='warning', help='Provide logging level. Example --loglevel debug, default=warning' )
	parser.add_argument('input', metavar='filename', type=str, help='input filename (otherwise STDIN)', nargs='?', default='')
	args = parser.parse_args()

	logging.basicConfig(stream=sys.stderr, level=args.loglevel.upper() )

	if args.test or logging.getLogger().isEnabledFor(logging.DEBUG):
		logging.debug('start test')
		tester()
		logging.debug('end test')
		if args.test:
			sys.exit(0)

	filename='stdin'
	if len(args.input) > 1:
		filename = args.input
		with open(filename,encoding='utf-8') as file:
			inputtext = file.read()
	else:
		inputtext = sys.stdin.read()


	if can_decode and args.decode:
		logging.debug('start %s decoding', name)
		outputtext = decoder(json.loads(inputtext))
		logging.debug('end %s decoding', name)
		if args.output:
			with open(args.output, 'w', encoding='utf-8') as file:
				file.write(outputtext)
		else:
			print(outputtext)
		sys.exit(0)

	logging.debug('start %s factorization', name)
	lz78phrases = compressor(inputtext)
	logging.debug('end %s factorization', name)
	if args.output:
		with open(args.output, 'w', encoding='utf-8') as file:
			json.dump(lz78phrases, file)
	elif not args.quiet:
		print(json.dumps(lz78phrases))

	if logging.getLogger().isEnabledFor(logging.DEBUG):
		assert inputtext == decodetester(lz78phrases,inputtext), f'{inputtext} != {decodetester(lz78phrases, inputtext)}'
	if args.stats:
		print(f'file={filename} length={len(inputtext)} factors={len(lz78phrases)}')
