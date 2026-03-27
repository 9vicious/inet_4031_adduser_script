#!/usr/bin/python3

# INET4031
# Abdirahman S
# Date Created: 3/26/26
# Date Last Modified: 3/26/26

import os      # To execute system-level commands like adduser and passwd
import re      # To filter input lines using regular expressions
import sys     # To read input from standard input (stdin)

def main():
    # --- Prompt for dry-run mode ---
    # Ask the user if they want to do a dry-run (test mode) instead of actually creating users
    dry_run_input = input("Run in dry-run mode? (Y/N): ").strip().upper()
    dry_run = True if dry_run_input == 'Y' else False

    # Read each line from the input file provided via stdin
    for line_number, line in enumerate(sys.stdin, 1):
        line = line.rstrip()

        # --- Skip comment lines ---
        if re.match("^#", line):
            # Dry-run mode: print a message instead of silently skipping
            if dry_run:
                print(f"[Dry-run] Line {line_number} skipped (comment line)")
            continue

        # --- Split line into fields ---
        fields = line.strip().split(':')

        # --- Check for invalid lines ---
        if len(fields) != 5:
            # Dry-run: print an error message if the line is malformed
            if dry_run:
                print(f"[Dry-run] Line {line_number} skipped (not enough fields: {len(fields)} fields found)")
            continue

        # --- Extract user info ---
        username = fields[0]
        password = fields[1]
        # GECOS stores full name info for adduser
        gecos = "%s %s,,," % (fields[3], fields[2])
        # Groups field: comma-separated, can have '-' for no extra groups
        groups = fields[4].split(',')

        # --- Create the user account ---
        print(f"==> Creating account for {username}...")
        cmd_create = f"/usr/sbin/adduser --disabled-password --gecos '{gecos}' {username}"
        if dry_run:
            # Dry-run: show the command that would run instead of running it
            print(f"[Dry-run] Command: {cmd_create}")
        else:
            # Normal mode: execute the command
            os.system(cmd_create)

        # --- Set the user password ---
        print(f"==> Setting the password for {username}...")
        cmd_passwd = f"/bin/echo -ne '{password}\n{password}' | /usr/bin/sudo /usr/bin/passwd {username}"
        if dry_run:
            print(f"[Dry-run] Command: {cmd_passwd}")
        else:
            os.system(cmd_passwd)

        # --- Assign groups ---
        for group in groups:
            if group != '-':
                print(f"==> Assigning {username} to the {group} group...")
                cmd_group = f"/usr/sbin/adduser {username} {group}"
                if dry_run:
                    print(f"[Dry-run] Command: {cmd_group}")
                else:
                    os.system(cmd_group)


if __name__ == '__main__':
    main()
