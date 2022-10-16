import argparse


def setup_available_options(argv):
    parser = argparse.ArgumentParser(add_help=False)
    required = parser.add_argument_group('required arguments')

    parser.add_argument('-h', '--help',
                        action='help',
                        help='Display this message.')

    required.add_argument('-f', '--email-from',
                          metavar='email-from',
                          required=True,
                          help='Email of data sender user (offboarded user).')
    required.add_argument('-t', '--email-to',
                          metavar='email-to',
                          required=True,
                          help='Email of data transfer receiver.')
    required.add_argument('-a', '--admin',
                          metavar='admin',
                          required=True,
                          help='Admin email. Used to use Service Account.')

    parser.add_argument('--offboard',
                        help='General user offboard. Triggers a couple of functions (see documentation).',
                        action='store_true')
    parser.add_argument('--sua',
                        help='Suspend user activity.',
                        action='store_true')
    parser.add_argument('--cou',
                        help='Change user organizational unit.',
                        action='store_true')
    parser.add_argument('--tdo',
                        help='Transfer Google Drive ownership.',
                        action='store_true')
    parser.add_argument('--tce',
                        help='Transfer calendar events.',
                        action='store_true')
    parser.add_argument('--tgdo',
                        help='Transfer Google Docs ownership',
                        action='store_true')
    parser.add_argument('--cebl',
                        help='Create email backup (locally).',
                        action='store_true')
    parser.add_argument('--cebg',
                        help='Create email backup (upload to Google Groups)',
                        action='store_true')
    parser.add_argument('-o', '--org-unit',
                        metavar='',
                        help='Used for Google Admin Workspace. Organizational unit. Set for --email-from')
    parser.add_argument('-c', '--client-id',
                        metavar='',
                        help='OAuth 2.0 client ID. Set only during first execution or if credentials were changed.')
    parser.add_argument('-s', '--client-secret',
                        metavar='',
                        help='OAuth 2.0 client secret. Set only during first execution or if credentials were changed.')
    parser.add_argument('-p', '--project-id',
                        metavar='',
                        help='Used for Google Admin Workspace. Set only during first execution or if credentials were changed.')

    return parser.parse_args(argv)
