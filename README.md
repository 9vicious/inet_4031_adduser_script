# inet_4031_adduser_script

## Description
A Python script to automate creating multiple Linux users and assigning them to groups using an input file. This saves time and reduces errors compared to manually adding users.

## How It Works
- Reads `create-users.input` line by line  
- Skips comments or invalid lines  
- Extracts username, password, full name, and groups  
- Creates each user account and sets the password  
- Assigns users to the specified groups  

## How to Run
1. Make the script executable:
```bash
chmod +x create-users.py
