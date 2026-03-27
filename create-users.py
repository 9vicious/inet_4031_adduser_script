#!/usr/bin/python3

# INET4031
# Abdirahman S
# Date Created: 3/26/26
# Date Last Modified: 3/26/26

import os      # To execute system-level commands like adduser and passwd
import re      # To filter input lines using regular expressions
import sys     # To read input from standard input (stdin)

def main():
    for line in sys.stdin:
        # Skip comment lines starting with '#'
        if re.match("^#", line):
            continue

        # Remove whitespace and split fields by ':'
        fields = line.strip().split(':')

        # Skip any lines that do not have exactly 5 fields
        if len(fields) != 5:
            continue

        # Extract user info
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])  # Full name field for adduser
        groups = fields[4].split(',')  # Split comma-separated groups

        # --- Create the user account ---
        print("==> Creating account for %s..." % username)
        cmd_create = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
        print(cmd_create)  # Optional: see what command will run
        os.system(cmd_create)  # Run the command as root

        # --- Set the user password ---
        print("==> Setting the password for %s..." % username)
        cmd_passwd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
        print(cmd_passwd)  # Optional: see what command will run
        os.system(cmd_passwd)

        # --- Assign groups ---
        for group in groups:
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd_group = "/usr/sbin/adduser %s %s" % (username, group)
                print(cmd_group)  # Optional: see what command will run
                os.system(cmd_group)

if __name__ == '__main__':
    main()
