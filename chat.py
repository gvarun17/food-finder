"""Terminal chat: python chat.py [-v]"""
import sys

from app.llm import chat_turn


def main() -> None:
    verbose = "-v" in sys.argv
    messages: list[dict] = []
    print("Hyderabad Food Finder (dev data). Type 'quit' to exit.\n")
    while True:
        try:
            user = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user.lower() in {"quit", "exit", ""}:
            if user:
                break
            continue
        messages.append({"role": "user", "content": user})
        print("\nbot>", chat_turn(messages, verbose=verbose), "\n")


if __name__ == "__main__":
    main()
