# Secret leak demo

This tiny demo is intentionally simple and safe. It shows how a fake secret can be committed, discovered, and revoked in a local environment.

## What it demonstrates

- a developer commits a secret to a local repo
- the secret is later found in Git history
- a mock API accepts the leaked token
- the credential is revoked and stops working
- the project is cleaned up with a safer workflow

## Files

- `server.py`: tiny local mock API that accepts a bearer token
- `vulnerable_app.py`: reads `PAYMENT_API_KEY` from `.env` and calls the API
- `.env`: demo secret used intentionally for the talk
- `.gitignore`: keeps local secrets out of version control
- `.env.example`: safe example to copy from

## Run it locally

1. Start the mock API:
   ```bash
   python3 server.py
   ```

2. In a second terminal, run the app:
   ```bash
   python3 vulnerable_app.py
   ```

   Expected result: the app successfully gets customer data because the fake token is still valid.

3. Show the secret in Git history:
   ```bash
   git status
   git log --oneline
   git show HEAD:.env
   ```

4. Revoke the token:
   ```bash
   curl -X POST http://127.0.0.1:9000/revoke -H "Content-Type: application/json" -d '{"token":"demo_live_key_do_not_use"}'
   ```

5. Run the app again:
   ```bash
   python3 vulnerable_app.py
   ```

   Expected result: `401 unauthorized` because the credential has been revoked.

## Important

This repository is intentionally using a clearly fake secret for demonstration purposes only. The point is to show the process, not to use a real credential.
