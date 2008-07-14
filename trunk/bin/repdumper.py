from optparse import OptionParser

from pyreplib import replay


VERSION = (0, 1, 0)

def version_to_string(seq):
    return '.'.join(map(str, seq))

def make_parser():
    parser = OptionParser(usage='%prog [options] <replay file>',
                          version=version_to_string(VERSION))
    parser.set_defaults(format='json')
    parser.add_option('-f', '--format', dest='format',
                      choices=['json', 'xml', 'yaml'], metavar='FORMAT',
                      help='Output FORMAT (json, xml, yaml)')
    return parser


def main():
    parser = make_parser()
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error('no replay file specified.')
    elif len(args) > 1:
        parser.error('only one replay file may be dumped at a time.')

if __name__ == '__main__':
    main()
