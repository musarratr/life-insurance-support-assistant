import os
from typing import Optional

import requests
from dotenv import load_dotenv


load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def post_chat(session_id: str, message: str) -> Optional[str]:
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"session_id": session_id, "message": message},
            timeout=60,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        return None

    return response.json()["response"]


def reset_session(session_id: str) -> None:
    try:
        response = requests.post(f"{API_BASE_URL}/reset/{session_id}", timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Reset failed: {exc}")
        return

    print(f"Session '{session_id}' reset.")


def main() -> None:
    print("Life Insurance Support Assistant CLI")
    print("Type 'exit' or 'quit' to leave. Type 'reset' to clear this session.")
    print(f"API: {API_BASE_URL}")

    session_id = input("Session ID [default]: ").strip() or "default"

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue

        command = user_input.lower()
        if command in {"exit", "quit"}:
            print("Goodbye.")
            break

        if command == "reset":
            reset_session(session_id)
            continue

        assistant_response = post_chat(session_id, user_input)
        if assistant_response:
            print(f"\nAssistant: {assistant_response}")


if __name__ == "__main__":
    main()
