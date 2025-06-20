import os
import json
import base64
import string
import random
from cryptography.fernet import Fernet
from getpass import getpass

DATA_FILE = "vault.json"
KEY_FILE = "key.key"

# ---------------------------------------------
# Utility Functions
# ---------------------------------------------

def generate_key(master_password: str) -> bytes:
    return base64.urlsafe_b64encode(master_password.encode().ljust(32, b'0'))

def load_key(master_password):
    return Fernet(generate_key(master_password))

def save_data(data, fernet):
    encrypted_data = fernet.encrypt(json.dumps(data).encode())
    with open(DATA_FILE, 'wb') as f:
        f.write(encrypted_data)

def load_data(fernet):
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'rb') as f:
        encrypted_data = f.read()
        try:
            decrypted = fernet.decrypt(encrypted_data)
            return json.loads(decrypted.decode())
        except:
            print("[!] Invalid Master Password or Corrupt Vault")
            return None

# ---------------------------------------------
# Password Generator
# ---------------------------------------------

def generate_password(length=12, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    chars = ''
    if use_upper:
        chars += string.ascii_uppercase
    if use_lower:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_symbols:
        chars += string.punctuation

    if not chars:
        return ''
    
    return ''.join(random.choice(chars) for _ in range(length))

def password_strength(password):
    length = len(password)
    types = sum([any(c in string.ascii_uppercase for c in password),
                 any(c in string.ascii_lowercase for c in password),
                 any(c in string.digits for c in password),
                 any(c in string.punctuation for c in password)])

    if length >= 12 and types == 4:
        return "Strong"
    elif length >= 8 and types >= 3:
        return "Medium"
    else:
        return "Weak"

# ---------------------------------------------
# Main Password Manager Functions
# ---------------------------------------------

def add_account(data, fernet):
    site = input("Enter account/site name: ").strip()
    username = input("Enter username/email: ").strip()
    password = input("Enter password (leave blank to auto-generate): ").strip()
    if not password:
        length = int(input("Enter desired password length: "))
        password = generate_password(length)
        print(f"Generated Password: {password}")
    
    print(f"Password Strength: {password_strength(password)}")
    data[site] = fernet.encrypt(password.encode()).decode()
    save_data(data, fernet)
    print("[+] Account saved successfully.")

def retrieve_password(data, fernet):
    site = input("Enter site name to retrieve: ").strip()
    if site in data:
        decrypted = fernet.decrypt(data[site].encode()).decode()
        print(f"🔐 Password for {site}: {decrypted}")
    else:
        print("[!] No such account stored.")

def list_accounts(data):
    if data:
        print("\nStored Accounts:")
        for site in data:
            print(f"- {site}")
    else:
        print("[!] No accounts found.")

# ---------------------------------------------
# Entry Point
# ---------------------------------------------

def main():
    print("🔒 Welcome to Smart Password Manager 🔒")
    master_password = getpass("Enter your master password: ")

    fernet = load_key(master_password)
    data = load_data(fernet)

    if data is None:
        return

    while True:
        print("\nOptions:\n1. Add Account\n2. Retrieve Password\n3. List Accounts\n4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            add_account(data, fernet)
        elif choice == '2':
            retrieve_password(data, fernet)
        elif choice == '3':
            list_accounts(data)
        elif choice == '4':
            print("Exiting... 🔐")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
