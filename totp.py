#!/usr/bin/env python3
"""
TOTP CLI PoC — compatible with Google Authenticator, Authy, etc.

Usage:
  python totp.py setup   — generate secret + QR code
  python totp.py auth    — verify a 6-digit code
"""

import sys
import os
import pyotp
import qrcode

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"

SECRET_FILE = "secret.txt"
ISSUER = "TOTP-PoC"
ACCOUNT = "demo@example.com"


def setup():
    secret = pyotp.random_base32()

    with open(SECRET_FILE, "w") as f:
        f.write(secret)

    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=ACCOUNT, issuer_name=ISSUER)

    # Render QR to terminal
    qr = qrcode.QRCode(border=1)
    qr.add_data(uri)
    qr.make(fit=True)
    qr.print_ascii(invert=True)

    print(f"\n{CYAN}Secret saved to {SECRET_FILE}{RESET}")
    print(f"{YELLOW}Manual entry key: {secret}{RESET}")
    print("\nScan the QR code above with your authenticator app.")


def auth():
    if not os.path.exists(SECRET_FILE):
        print(f"{RED}No secret found. Run 'python totp.py setup' first.{RESET}")
        sys.exit(1)

    with open(SECRET_FILE) as f:
        secret = f.read().strip()

    totp = pyotp.TOTP(secret)

    while True:
        code = input("Enter 6-digit code: ").strip()
        if totp.verify(code):
            print(f"{GREEN}✓ Authenticated{RESET}")
            break
        print(f"{RED}✗ Invalid code, try again.{RESET}")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("setup", "auth"):
        print(__doc__)
        sys.exit(1)

    {"setup": setup, "auth": auth}[sys.argv[1]]()
