LOGO = [
    '+---------------+\n',
    '| GOOGLE-MERGER |\n',
    '+---------------+\n\n'
]

SCOPES = {
    'admin': ['https://www.googleapis.com/auth/admin.directory.user'],
    'drive': ['https://www.googleapis.com/auth/drive'],
    'gmail': [
        'https://mail.google.com/',
        'https://www.googleapis.com/auth/gmail.settings.basic',
        'https://www.googleapis.com/auth/gmail.settings.sharing',
        'https://www.googleapis.com/auth/apps.groups.migration',
        'https://www.googleapis.com/auth/drive.appdata',
        'https://www.googleapis.com/auth/userinfo.email'
    ],
    'calendar': ['https://www.googleapis.com/auth/calendar']
}

CLI_OPERATIONS = ['sua', 'tce', 'tdo', 'ef']

MENU = [
    'Start\n',
    'Documentation\n',
    'Exit\n'
]

AVAILABLE_FUNCTIONS = [
    'Suspend user activity\n',
    'Change user Organizational Unit\n',
    'Transfer GDrive ownership\n',
    'Transfer Google Calendar events\n',
    'Enable email forwarding\n'
]

PAD_HEIGHT = 16384


def pad_refresh(pad, pad_pos, height, width):
    pad.refresh(pad_pos, 0, 0, 0, height - 1, width)


def navigation_control(pad, y, height, width):
    key_up, key_down = 'AB'

    for c in iter(pad.getkey, 'q'):
        if c in '\x1b\x5b':
            continue
        y -= (c == key_up)
        y += (c == key_down)
        pad_refresh(pad, y, height, width)