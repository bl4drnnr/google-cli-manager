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
