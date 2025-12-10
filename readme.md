# Environments :

For the "Pygame" user interface library to work, you must launch 
the project with Python version 3.12.

## Windows

1. Get Python 3.12 : <a href="https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe">Windows installer (direct link)</a>
2. Go to the root of the project and create a new environment based on the 3.12 Python version :
`py -3.12 -m venv .venv`
3. Select the 3.12 version in your IDE (generally at bottom right for VSCode or IntelliJ)
4. (Optional) Execute this command to allow scripts execution in PowerShell `Set-ExecutionPolicy Unrestricted -Scope Process`
5. Activate the environment : `.\.venv\Scripts\Activate`
6. Check the Python version : `python --version`
7. Install the required modules : `pip install -r requirements.txt`

You should have now your environment specified in your CLI in parentheses.