import argparse


def setup_available_options(argv):
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-h', '--help',
                        action='help',
                        help='Display this message.')

    return parser.parse_args(argv)
