import argparse


def setup_available_options(argv):
    parser = argparse.ArgumentParser(add_help=False)
    first_execution = parser.add_argument_group('First execution credentials')
    services = parser.add_argument_group('Service')

    parser.add_argument('-h', '--help',
                        action='help',
                        help='Display this message.')

    parser.add_argument('-f', '--email-from',
                        metavar='',
                        help='Email of data sender user (offboarded user).')
    parser.add_argument('-t', '--email-to',
                        metavar='',
                        help='Email of data transfer receiver.')
    parser.add_argument('-a', '--admin',
                        metavar='',
                        help='Admin email. Used to use Service Account.')
    parser.add_argument('-g', '--group',
                        metavar='',
                        help='Name of the group.')
    parser.add_argument('-o', '--org-unit',
                        metavar='',
                        help='Used for Google Admin Workspace organizational unit.')
    parser.add_argument('-r', '--customer-id',
                        metavar='',
                        help='In order to obtain Customer ID see README docs.')
    parser.add_argument('-u', '--users',
                        metavar='',
                        help='List of users. who has access to group in next format: user1@domain.com,user2@domain.com')

    parser.add_argument('--offboard',
                        help='General user offboard. See docs to know what is triggered.',
                        action='store_true')
    parser.add_argument('--sua',
                        help='Suspend user activity.',
                        action='store_true')
    parser.add_argument('--aua',
                        help='Archive user account.',
                        action='store_true')
    parser.add_argument('--cou',
                        help='Change user organizational unit.',
                        action='store_true')
    parser.add_argument('--tdo',
                        help='Transfer Google Drive ownership.',
                        action='store_true')
    parser.add_argument('--tce',
                        help='Transfer Google Calendar events.',
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
    parser.add_argument('--cg',
                        help='Create Google Group (use "-g" or "--group" in order to set group name)',
                        action='store_true')
    parser.add_argument('--get-user',
                        help='Get and print information about user.',
                        action='store_true')

    first_execution.add_argument('-c', '--client-id',
                                 metavar='',
                                 help='OAuth 2.0 client ID.')
    first_execution.add_argument('-s', '--secret',
                                 metavar='',
                                 help='OAuth 2.0 client secret.')
    first_execution.add_argument('-p', '--project-id',
                                 metavar='',
                                 help='Used for Google Admin Workspace.')
    first_execution.add_argument('-d', '--delegate',
                                 metavar='',
                                 help='Email to delegate Google Service Account.')

    services.add_argument('-i', '--init-cred',
                          help='Init or reinit credentials.',
                          action='store_true')

    return parser.parse_args(argv)
