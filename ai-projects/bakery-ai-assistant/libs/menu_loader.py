import os
import json

def load_menu():
    # Get path to the current file (menu_loader.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Go up one directory and access menu.json
    menu_path = os.path.join(current_dir, "..", "menu.json")

    with open(menu_path, "r") as f:
        json_data = json.load(f)
        menu_text = ""
        for name, price in json_data.items():
            menu_text += f"- {name} : AED {price}\n"
        return menu_text
