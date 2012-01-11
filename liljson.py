from sys import stdin, stdout
from json import load, JSONEncoder
from optparse import OptionParser
from re import compile

float_pat = compile(r'^-?\d+\.\d+(e-?\d+)?$')

parser = OptionParser(usage="""%prog [options]

Make JSON smaller by reducing precision of floating point values
and removing white space. Works great for GeoJSON!

Examples:
  cat input.json | python %prog --precision 2 > output.json
  python %prog --precision 2 input.json > output.json
  python %prog -p 2 input.json output.json""")

defaults = dict(precision=3)

parser.set_defaults(**defaults)

parser.add_option('-p', '--precision', dest='precision',
                  type='int', help='Digits of precision, default %(precision)d.' % defaults)

if __name__ == '__main__':
    options, args = parser.parse_args()
    
    #
    # Figure out our input and output file descriptors.
    #
    input = len(args) and open(args[0]) or stdin
    output = len(args) == 2 and open(args[1], 'w') or stdout

    #
    # Read!
    #
    data = load(input)
    
    #
    # Write!
    #
    encoder = JSONEncoder(separators=(',', ':'))
    encoded = encoder.iterencode(data)
    
    format = '%.' + str(options.precision) + 'f'
    
    for token in encoded:
        if float_pat.match(token):
            output.write(format % float(token))
        else:
            output.write(token)
