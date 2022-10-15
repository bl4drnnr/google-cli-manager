# Table of Contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
   1. [Creating project](#creating-project)
   2. [Service account](#service-account)
3. [Installation](#installation)
4. [Documentation](#documentation)
   1. [Interactive CLI](#interactive-cli)
   2. [Classic terminal application](#classic-terminal-application)
5. [Available endpoints](#available-endpoints)
   1. [Admin workspace](#admin-workspace)
   2. [Calendar](#calendar)
   3. [Docs](#docs)
   4. [Drive](#drive)
   5. [Gmail](#gmail)
6. [References](#references)
7. [License](#license)

---

### Introduction
**Google Manager** - is the simple _**Python application**_ that allows to manage Google account(s) via _**CLI**_. 

The application is available in 2 versions:
- Interactive **CLI**
- Classic terminal application

Documentation for both of them will be written below. In order to obtain more information about 
`Google API` (Python SDK, in this case) see [references](#references).

---

### Requirements 

Depending on functionality you want to use, you'll have to provide different type of authentication data.
Every action requires to be authenticated using `OAuth 2.0`.

In order to obtain those credentials you need to create project on [Google Cloud](https://console.cloud.google.com/).
If you want to use functionality to manage users' accounts within **Google Workspace**,
just skip next steps, dedicated creating of project and go to [Service Account](#service-account) section.

#### Creating project
1. Go to [Google Cloud project creation page](https://console.cloud.google.com/projectcreate).

If you already have project on Google Cloud and you want to manage other users' data
what you need to do, is to create **Service Account**.

**Service Account** - is a type of account, that allows administrators to manager
other users' accounts (within same organization) without strict access to their account.
Purpose of **Service Account** is to be _"proxy"_ account, that will escalate and execute
commands from administrator (through **API**, in this case).

#### Service account

---

### Installation

To install `Google Manager CLI` on your computer, open terminal and paste next command:

```
bash <(curl -s -S -L https://raw.githubusercontent.com/bl4drnnr/google-cli-manager/master/install.sh)
```

Then hit `ENTER`, and after installation is done, quit and reopen terminal.

Type `gmcli -h` to check if everything was installed correctly. 

---

### Documentation

The program works in 2 modes. As Interactive terminal-based application and classic terminal application.

#### Interactive CLI

To execute program as Interactive CLI, type `gmcli`. Use arrows on a keyboard to navigate menu and `ENTER` to
confirm select.

#### Classic terminal application

If you want to execute program in classic terminal application mode, it'll be enough to type
`gmcli -h` to list all possible commands.

---

### Available endpoints

#### Admin workspace
#### Calendar
#### Docs
#### Drive
#### Gmail

---

### References

- Developer contact - [mikhail.bahdashych@protonmail.com](mailto:mikhail.bahdashych@protonmail.com)
- [Google Developers](https://developers.google.com/) - Official SDKs by Google
- [Google Calendar API](https://developers.google.com/calendar/api) - **Google Calendar** for developers
- [Google Gmail API](https://developers.google.com/gmail/api) - **Google Gmail** for developers
- [Google Drive API](https://developers.google.com/drive/api) - **Google Drive** for developers
- [Google Docs API](https://developers.google.com/docs/api) - **Google Docs** for developers
- [Google Workspace Admin SDK](https://developers.google.com/admin-sdk) - **Google Admin** for developers

---

### License

Licensed by [MIT License](LICENSE).
