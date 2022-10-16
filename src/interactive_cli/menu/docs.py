commands_docs = {
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
    ]
}
