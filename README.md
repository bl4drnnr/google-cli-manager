# Table of Contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
   1. [Creating project](#creating-project)
   2. [Creating service account](#creating-service-account)
   3. [Delegating domain-wide authority to the service account](#delegating-domain-wide-authority-to-the-service-account)
3. [Installation](#installation)
4. [Types of execution](#types-of-execution)
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

It's important to mention, that depending on what you want to do, you will have to create and
provide different types of credentials.

So, there are 2 options:
- If you want to use **API** only for managing your own account, what you need to do, is just [create project](#creating-project) and get `OAuth 2.0` credentials.
- If you want to access other users' data (within same organization) you need [create project](#creating-project), get `OAuth 2.0` credentials, [Create service account](#creating-service-account) and [delegate domain wide authority to the service account](#delegating-domain-wide-authority-to-the-service-account).

#### Creating project

In order to obtain those credentials you need to create project on [Google Cloud](https://console.cloud.google.com/).
If you want to use functionality to manage users' accounts within **Google Workspace**,
just skip next steps, dedicated creating of project and go to [Creating service account](#creating-service-account) section.

1. Go to [Google Cloud project creation page](https://console.cloud.google.com/projectcreate).
2. Provide project name and click `Create`.
3. On the left side bard click `APIs & Services` and then `Credentials`.
4. At the top click `Create Credentials` and select `OAuth client ID`.
5. There, if you didn't it before, you will be invited to configure `OAuth consent screen`. If you already did that, go to next steps.
   1. There, in `User Type` select `External` and click `Create`.
6. Then, you'll be provided to type the `App name`, `User support email` and `Developer email`. After you have done it, click `Save and Continue`.
7. On the next page, **it will be very important** to set scopes, in order to make things work. Click `Add or Remove Scopes` and select scopes you need. If you think, that there are no scopes you need [OAuth 2.0 Scopes for Google APIs](https://developers.google.com/identity/protocols/oauth2/scopes).
8. Click `Update` and then, at the bottom, `Save and Continue`.
9. Provide test users (**not necessary**)
10. At the **Summary** page, at the bottom, click `Back to Dashboard`.
11. On the left side bard click `APIs & Services` and then `Credentials` and select `OAuth client ID`.
12. As the `Application type` set `Desktop app` and provide name for it.
13. You have got your `Client ID` and `Client Sercret`. Copy it or download as `JSON` file.

#### Creating service account

If you already have project on Google Cloud and you want to manage other users' data (within organization)
what you need to do, is to create **Service Account** and then [delegate authority](#delegating-domain-wide-authority-to-the-service-account).

**Service Account** - is a type of account, that allows administrators to manager
other users' accounts (within same organization) without strict access to their account.
Purpose of **Service Account** is to be _"proxy"_ account, that will escalate and execute
commands from administrator (through **API**, in this case).

1. On the left side bard click `APIs & Services` and then `Credentials`.
2. At the top click `Create Credentials` and select `Create service account`.
3. At the next page grant `Owner` access.
4. On the last page, provide email of user, who will have access for managing other users' data or **delegated user**.
5. Click `Done`.
6. Next, click the email address for the service account you created.
7. Click the `Keys` tab.
8. In the `Add key` drop-down list, select `Create new key`.
9. Click `Create`.

#### Delegating domain-wide authority to the service account

If you have a Google Workspace account, an administrator of the organization can authorize an application to access user data on behalf of users in the Google Workspace domain. For example, an application that uses the Google Calendar API to add events to the calendars of all users in a Google Workspace domain would use a service account to access the Google Calendar API on behalf of users. Authorizing a service account to access data on behalf of users in a domain is sometimes referred to as "delegating domain-wide authority" to a service account.

To delegate domain-wide authority to a service account, a super administrator of the Google Workspace domain must complete the following steps:

1. From your Google Workspace domain's Admin console, go to **Main menu > Security > Access and data control > API Controls**.
2. In the **Domain wide delegation** pane, select **Manage Domain Wide Delegation**.
3. Click **Add new**.
4. In the **Client ID** field, enter the service account's **Client ID**. You can find your service account's client ID in the Service accounts page.
5. In the **OAuth scopes (comma-delimited)** field, enter the list of scopes that your application should be granted access to. For example, if your application needs domain-wide full access to the Google Drive API and the Google Calendar API, enter: `https://www.googleapis.com/auth/drive, https://www.googleapis.com/auth/calendar`.
6. Click **Authorize**.

For more information see [Using OAuth 2.0 for Server to Server Applications](https://developers.google.com/identity/protocols/oauth2/service-account).

---

### Installation

For **MacOS** and **Linux** systems:

To install `Google Manager CLI` on your computer, open terminal and paste next command:

```
bash <(curl -s -S -L https://raw.githubusercontent.com/bl4drnnr/google-cli-manager/master/install.sh)
```

Then hit `ENTER`, and after installation is done, quit and reopen terminal.

Type `gmcli -h` to check if everything was installed correctly. 

---

### Types of execution

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
- [Using OAuth 2.0 for Server to Server Applications](https://developers.google.com/identity/protocols/oauth2/service-account) - how to create Service Account and delegate authority to it  
- [OAuth 2.0 Scopes for Google APIs](https://developers.google.com/identity/protocols/oauth2/scopes) - list of all OAuth 2.0 scopes

---

### License

Licensed by [MIT License](LICENSE).
