LOGO = [
    '+--------------------+\n',
    '| GOOGLE-CLI-MANAGER |\n',
    '  +--------------------+\n\n'
]

SCOPES = {
    'admin': [
        'https://www.googleapis.com/auth/admin.directory.user'
    ],
    'drive': [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.appdata'
    ],
    'gmail': [
        'https://mail.google.com/',
    ],
    'groupsmigration': [
        'https://www.googleapis.com/auth/apps.groups.migration'
    ],
    'calendar': [
        'https://www.googleapis.com/auth/calendar'
    ],
    'iam': [
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/cloud-identity.groups'
    ],
}

CLI_OPERATIONS = ['offboard', 'sua', 'cou', 'tce', 'tdo', 'cebl', 'cebg', 'tgdo', 'cg', 'init_cred', 'get_user', 'aua']

MENU = [
    'Start\n',
    'Documentation\n',
    'Exit\n'
]

AVAILABLE_FUNCTIONS = [
    'Offboard user\n\n',
    'Suspend user activity\n',
    'Archive user\n',
    'Change user Organizational Unit\n\n',
    'Transfer Google Drive ownership\n',
    'Transfer Google Calendar events\n',
    'Transfer Google Docs ownership\n\n',
    'Create Google Group\n\n',
    'Create email backup (locally)\n',
    'Create email backup (upload to Google Groups)\n\n',
    'Get user by email\n\n',
    'Initiate credentials files\n'
]

PAD_HEIGHT = 16384
