import argparse


def setup_available_options(argv):
    parser = argparse.ArgumentParser(add_help=False)
    required = parser.add_argument_group('required arguments')

    parser.add_argument('-h', '--help',
                        action='help',
                        help='Display this message.')
    required.add_argument('-f', '--email-from',
                          metavar='',
                          required=True,
                          help='Email of offboarded user.')
    required.add_argument('-t', '--email-to',
                          metavar='',
                          required=True,
                          help='Email of data transfer receiver.')
    parser.add_argument('--offboard',
                        help='General user offboard. Triggers all functions below.',
                        action='store_true')
    parser.add_argument('--sua',
                        help='Suspend user activity.',
                        action='store_true')
    parser.add_argument('--cou',
                        help='Change user organizational unit.',
                        action='store_true')
    parser.add_argument('--tdo',
                        help='Transfer GDrive ownership.',
                        action='store_true')
    parser.add_argument('--tce',
                        help='Transfer calendar events.',
                        action='store_true')
    parser.add_argument('--ceb',
                        help='Create email backup.',
                        action='store_true')

    return parser.parse_args(argv)
