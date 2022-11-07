# A simple CLI to manage your Gmail messages quickly

## Requirements

- Python
- Git
- Google account
- Google application password
  

## Instructions

1. First you need to clone this repository into your own machine. To do so, you can use Git Bash or any console you like with git installed:

```bash
git clone https://github.com/rodrigofcaba/Cleaning-Gmail.git
```

2. After that, you have to install the necessary packages. To do so, in the terminal run:

```bash
pip install -r requirements.txt
```

Now you need to set up your google account to get the password to connect to your IMAP server. This you can do in your Google Account settings.

```
Your google account -> security -> Apps passwords
```
Generate a new password by selecting an application type (other), choose a name, for instance "IMAP CLIENT", click "Generate".

Save the password you see on the screen, you will need it the first time you log into the server.


## Usage

Now, to use the app, navigate to the folder in which you have the folder cloned from the repo. For example, if the folder is placed in your desktop:

```bash
cd ~/Desktop/Cleaning-Gmail
```
You need to have python in your PATH or execute the binary using the full absolute path. Use the "p" flag to introduce your password. It will be securely stored so you don't have to right it down in the future to connect.

```bash
python clean-Gmail.py your-email-account@gmail.com -p your-password 
```
Press enter and follow the instructions.

**NOTE:** After first successful login, you just need to type your email to connect to the server.
