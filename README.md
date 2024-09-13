## Flexible Parsing of Lempel-Ziv 78

Implementation of the flexible parsing (FP) and the alternative flexible parsing (FPA)
for Lempel-Ziv 78 (LZ78).

There are three executables for computing the LZ78, LZ78-FP and LZ78-FPA factorization:

 - lz78.py
 - fp78.py
 - fpa78.py

All three have the same command line interface.

```console
usage: lz78.py [-h] [-o [filename]] [-d] [-q] [-s] [-t] [-l LOGLEVEL] [filename]

LZ78 Compressor

positional arguments:
  filename              input filename (otherwise STDIN)

options:
  -h, --help            show this help message and exit
  -o [filename], --output [filename]
                        output filename (otherwise STDOUT)
  -d, --decode          decode instead of compress
  -q, --quiet           do not produce a compressed output
  -s, --stats           output statistics on the number of factors
  -t, --test            runs tests and quit
  -l LOGLEVEL, --loglevel LOGLEVEL
                        Provide logging level. Example --loglevel debug, default=warning
```

## Caveat

For FP/FPA, there is no decompressor yet implemented.
The validity of the compressed text is verified by using the uncompressed text.


## References

- [Flexible parsing for LZW](https://www.dcs.warwick.ac.uk/~nasir/work/fp)
