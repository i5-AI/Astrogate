# handle_button.py
import sys

def handle_button(button_id):
    print(f"Handling button with ID: {button_id}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        handle_button(sys.argv[1])
