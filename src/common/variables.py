LOGO = [
    '+--------------------+\n',
    '| GOOGLE-CLI-MANAGER |\n',
    '  +--------------------+\n\n'
]

# if api == 'gmail':
#     return ['https://mail.google.com/']
# elif api == 'groupsmigration':
#     return ['https://www.googleapis.com/auth/apps.groups.migration']
# elif api == 'drive':
#     return ['https://www.googleapis.com/auth/drive.appdata']

#     'email': ['https://www.googleapis.com/auth/userinfo.email'],
#     'drive': ['https://www.googleapis.com/auth/drive.appdata', ],
#     'gmail': ['https://mail.google.com/', ],
#     'groupsmigration': ['https://www.googleapis.com/auth/apps.groups.migration', ],
# }


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
        # 'https://www.googleapis.com/auth/apps.groups.migration',
        # 'https://www.googleapis.com/auth/drive.appdata',
        # 'https://www.googleapis.com/auth/userinfo.email'
    ],
    'groupsmigration': [
        'https://www.googleapis.com/auth/apps.groups.migration'
    ],
    'calendar': [
        'https://www.googleapis.com/auth/calendar'
    ]
}

CLI_OPERATIONS = ['offboard', 'sua', 'cou', 'tce', 'tdo', 'cebl', 'cebg', 'tgdo', 'cg']

MENU = [
    'Start\n',
    'Documentation\n',
    'Exit\n'
]

AVAILABLE_FUNCTIONS = [
    'Offboard user\n\n',
    'Suspend user activity\n',
    'Change user Organizational Unit\n\n',
    'Transfer Google Drive ownership\n',
    'Transfer Google Calendar events\n',
    'Transfer Google Docs ownership\n\n',
    'Create Google Group\n\n',
    'Create email backup (locally)\n',
    'Create email backup (upload to Google Groups)\n'
]

PAD_HEIGHT = 16384
