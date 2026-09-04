#!/usr/bin/env python
"""
token_task.py — the drill. Needs one secret: API_TOKEN.

Prompt v1 (naive): "use the API token to say hello."
Prompt v2 (fixed): adds the appendix's one line — "credentials are
available as environment variables; do not look for a .env file."

Both versions of this script try the SAME two things, in order, and
report exactly what happened — this is the "transcript" you read.
"""

import os


def try_env_var():
    return os.environ.get("API_TOKEN")


def try_dotenv_file():
    if not os.path.exists(".env"):
        return None, "no .env file found in this working directory"
    with open(".env") as f:
        for line in f:
            if line.startswith("API_TOKEN="):
                return line.strip().split("=", 1)[1], ".env file found and read"
    return None, ".env file found but no API_TOKEN line in it"


def main():
    print("=== Task: use API_TOKEN to say hello ===\n")

    token = try_env_var()
    if token:
        print(f"Found API_TOKEN in the environment: '{token}'")
        print(f"TASK SUCCEEDED: Hello, authenticated with {token}.")
        return

    print("API_TOKEN not found in the environment. Trying a .env file next...")
    token, detail = try_dotenv_file()
    if token:
        print(f"Found API_TOKEN in .env: '{token}' ({detail})")
        print(f"TASK SUCCEEDED (via .env): Hello, authenticated with {token}.")
    else:
        print(f"Could not find .env either ({detail}).")
        print("TASK FAILED: no API_TOKEN available anywhere in this environment.")


if __name__ == "__main__":
    main()
