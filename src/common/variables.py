LOGO = [
    '+--------------------+\n',
    '| GOOGLE-CLI-MANAGER |\n',
    '  +--------------------+\n\n'
]

SCOPES = {
    'admin': [
        'https://www.googleapis.com/auth/admin.directory.user',
        'https://www.googleapis.com/auth/admin.directory.group'
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
    'cloudidentity': [
        'https://www.googleapis.com/auth/cloud-identity.groups'
    ]
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

COMMAND_DOCS = {
    'Offboard user': [
        'User offboarding - general procedure (organizations only), that deactivates user\'s account by doing next:\n',
        '1. Suspend user\'s activity.\n',
        '2. Change user Organizational Unit\n',
        '3. Transfer Google Drive ownership.\n',
        '4. Transfer Google Calendar events.\n',
        '5. Create emails backup using Google Groups.\n\n'
    ],
    'Suspend user activity': [
        'Suspends user\'s activity\n',
        'Account isn\'t archiving, therefor activity can be restored at any moment.\n\n'
    ],
    'Archive user': [
        'Archives user account\n',
        'Used mostly in order to offboard user with suspending activity before.\n\n'
    ],
    'Change user Organizational Unit': [
        'Changes Organizational Unit user belongs to.\n',
        'Can be used from pool of existing ones.\n\n'
    ],
    'Transfer Google Drive ownership': [
        'Transfers ownership of all files on Google Drive.\n',
        'Ownership is transferred only for files that have been created by this user.\n\n'
    ],
    'Transfer Google Calendar events': [
        'Transfers events from one Google Calendar to another.\n',
        'Transfer is done by sending email with proposition to add events\n',
        'to person how has to receive events of sender person.\n\n'
    ],
    'Transfer Google Docs ownership': [
        'Transfers ownership of all Docs files.\n',
        'Ownership is transferred only for files that have been created by this user.\n\n'
    ],
    'Create email backup (locally)': [
        'Creates backup of emails locally.\n',
        'Files saved as database and can be used as local backup, but also with purpose\n',
        'of the restoration and creating Google Group with backuped email.\n\n'
    ],
    'Create email backup (upload to Google Groups)': [
        'Creates backup of emails and uploads it as Google Group.\n',
        'Before using this option, you need to have already created group on Google Groups.\n',
        'Read Documentation or see README file in order to obtain more information.\n\n'
    ],
    'Create Google Group': [
        'Creates Google Groups within organization.\n',
        'Mostly used for creating email backups, but can be created as empty group.\n\n'
    ],
    'Get user by email': [
        'Allows to get information about user by email.\n',
        'Option is available only for delegated users and requires proper accesses.\n\n'
    ],
    'Initiate credentials files': [
        'Allow to generate or regenerate credentials files (OAuth 2.0 for personal account and Service Account) ',
        'Use it in case if credentials were changed or wasn\'t generated at all.\n\n'
    ]
}
