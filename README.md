# A simple CLI to manage your Gmail messages quickly

## Requirements

- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/) (You can also download the files of the repo [downloading the .zip](https://github.com/rodrigofcaba/Cleaning-Gmail/archive/refs/heads/master.zip))
- [Google account](https://support.google.com/accounts/answer/27441?hl=es)
- [Google application password](https://support.google.com/accounts/answer/185833?hl=es)
  

## Instructions

1. First you need to clone this repository into your own machine. To do so, you can use Git Bash or any console you like with git installed:

```bash
git clone https://github.com/rodrigofcaba/Cleaning-Gmail.git
```

2. After that, you have to install the necessary packages. To do so, in the terminal run:

```bash
pip install -r requirements.txt
```

3. Now you need to set up your google account to get the password to connect to your IMAP server. This you can do in your Google Account settings.

```
Your google account -> security -> Apps passwords
```
4. Generate a new password by selecting an application type (other), choose a name, for instance "IMAP CLIENT", click "Generate".
**NOTE:** **Save the password** you see on the screen, you will need it the first time you log into the server.


## Usage

1. Navigate to the folder in which you have the folder cloned from the repo. For example, if the folder is placed in your desktop:

```bash
cd ~/Desktop/Cleaning-Gmail
```
2. You need to have [python in your PATH](https://realpython.com/add-python-to-path/) or execute the binary using the full absolute path. **Use the "p" flag to introduce your password**.
   
    **NOTE:** It will be securely stored so you don't have to write it down in the future to connect to the server.

```bash
python clean-gmail.py your-email-account@gmail.com -p your-password 
```
3. Press enter and follow the instructions.

    **NOTE:** After first successful login, you just need to type your email to connect to the server:

```bash
python clean-gmail.py your-email-account@gmail.com
```
