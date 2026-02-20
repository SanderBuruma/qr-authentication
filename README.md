# QR Authentication PoC

A minimal CLI proof-of-concept for TOTP-based two-factor authentication (RFC 6238), compatible with any standard authenticator app (Google Authenticator, Authy, etc.).

## How it works

Generates a secret key and encodes it as a QR code. The authenticator app scans it once and then continuously derives 6-digit codes from the shared secret + current timestamp — no network communication involved.

## Usage

**Setup** — generate a secret and display the QR code:
```bash
./venv/bin/python totp.py setup
```
Scan the QR code with your authenticator app, or enter the printed base32 key manually.

**Authenticate** — verify a 6-digit code:
```bash
./venv/bin/python totp.py auth
```
Retries on failure until a valid code is entered. Ctrl+C to abort.

## Installation

```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

## Dependencies

- `pyotp` — TOTP implementation
- `qrcode` — terminal QR rendering
- `pillow` — required by qrcode

## Notes

- The secret is stored in `secret.txt` (gitignored). Keep it safe — anyone with it can generate valid codes.
- TOTP codes rotate every 30 seconds with a one-window tolerance on verification.
