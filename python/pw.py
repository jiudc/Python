#! python3
# pw.py - An insecure password locker program.

PASSWORDS = {'email': 'FDGDG46463dgs',
             'blog': 'gsdgs22242',
             'luggage': '12345'}

import sys, pyperclip

if len(sys.argv) < 2:
    print('Usage:python pw.py [account] - copy account password')
    sys.exit()

accout = sys.argv[1]
if accout in PASSWORDS:
    pyperclip.copy(PASSWORDS[accout])
    print('Passwrod for ' + accout + ' copied to clipboard.' + pyperclip.paste(PASSWORDS[accout]))
else:
    print('There is no account name' + accout)
