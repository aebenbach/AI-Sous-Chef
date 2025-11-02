import os 

from langchain.tools import tool

NOTES_PATH = "recipes/notes"

@tool
def add_note(recipe: str, note: str) -> None:
    """
    Saves a note on a recipe

    recipe: Name of the recipe 
    note: The note that should be saved
    """

    try:
        os.makedirs(NOTES_PATH, exist_ok=True) 

        file_path = os.path.join(NOTES_PATH, f"{recipe}.txt")

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"• {note}\n")

    except Exception as e:
        print(f"something went wrong: {e}")
        raise            

@tool
def read_notes(recipe: str) -> str:
    """Returns all notes for a recipe"""
    try:

        file_path = os.path.join(NOTES_PATH, f"{recipe}.txt")

        with open(file_path, "r", encoding="utf-8") as f:
            notes = f.read()

        return notes

    except Exception as e:
        print(f"something went wrong: {e}")
        raise         

