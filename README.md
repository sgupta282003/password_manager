# 🔐 Smart Password Generator and Manager (Local)

A secure, local password generator and manager built with Python. This application allows users to generate strong, customizable passwords, assess password strength, and store/retrieve credentials securely using local encryption and a master password.

---

## 📌 Features

- **🔑 Master Password Authentication**  
  All passwords are encrypted and decrypted using a user-defined master password.

- **🔐 Secure Local Storage**  
  Stores account credentials locally in an encrypted JSON file using the `cryptography` library.

- **⚙️ Customizable Password Generation**  
  Generate strong passwords with user-defined settings:
  - Length
  - Uppercase Letters
  - Lowercase Letters
  - Digits
  - Special Symbols

- **🛡️ Password Strength Indicator**  
  Quickly assess whether a password is Strong, Medium, or Weak based on its composition and length.

- **💾 Account Management**  
  - Save new account credentials
  - Retrieve stored passwords
  - List all stored account names
  - Search for specific account credentials

---

## 🚀 Getting Started

### ✅ Prerequisites

Ensure you have Python 3.6 or later installed.

Install the required dependency:
```bash
pip install cryptography
