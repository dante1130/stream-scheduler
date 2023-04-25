# stream-scheduler

A simple stream scheduler for YouTube.

## Table of Contents

- [stream-scheduler](#stream-scheduler)
  - [Table of Contents](#table-of-contents)
  - [Creating OAuth Credentials](#creating-oauth-credentials)
  - [Installing Dependencies](#installing-dependencies)
    - [Installing Python](#installing-python)
      - [Windows](#windows)
    - [Setting up virtualenv](#setting-up-virtualenv)
    - [Installing Libraries](#installing-libraries)
  - [Running the program](#running-the-program)

## Creating OAuth Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Select a project, or create a new one.
3. In the Credentials tab, select the Create credentials drop-down list, and choose OAuth client ID.
4. Under Application type, choose Desktop app. You can give it any name you like.
5. Download the JSON file and rename it to `client_secret.json`. **Important: Do not share this file with anyone or check it into public source control.**
6. Copy the file to the root of the project.

## Installing Dependencies

### Installing Python

#### Windows

Install `Chocolatey` by following the instructions [here](https://chocolatey.org/install).

Then run the following command in an elevated command prompt:

```bash
choco install python
```

### Setting up virtualenv

```bash
pip install virtualenv
virtualenv venv
venv\Scripts\activate
```

### Installing Libraries

```bash
pip install -r requirements.txt
```

## Running the program

```bash
venv/Scripts/python main.py
```
