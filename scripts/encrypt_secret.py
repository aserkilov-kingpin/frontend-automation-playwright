import getopt
import sys

from common.secret import SecretManager

help_msg = f"""encrypt_secret.py usage:
Encrypts a password, token, etc and adds it to the secret.yaml file
    the script will update existing entries

Example:
    python3 encrypt_secret.py --name Xsecret.test.password --secret AsecretPassword

Required parameters:
    -n, --name        name of the secret to add, usually should start with Xsecret
    -s, --secret      the secret data to encrpyt and store in secret.yaml (password, etc)

Optional Parameters:
    -h, --help      Print this help message
"""

name = ""
secret = ""
# pull values from command line
try:
    opts, args = getopt.getopt(
        sys.argv[1:],
        "n:s:h",
        [
            "name=",
            "secret=",
            "help",
        ],
    )
except getopt.GetoptError as e:
    print(e)
    print("\n\n" + help_msg)
    sys.exit(1)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print(help_msg)
        sys.exit(0)
    elif opt in ("-n", "--name"):
        name = arg
    elif opt in ("-s", "--secret"):
        secret = arg

if not name:
    print(f"No name provided (-n or --name)\n\n{help_msg}")

    sys.exit(1)
if not secret:
    print(f"No secret provided (-s or --secret)\n\n{help_msg}")
    sys.exit(1)


sec_mgr = SecretManager()
print("Adding secret to yaml")
sec_mgr.add_password(name=name, password=secret)
print("secret added")
