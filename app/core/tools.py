import os 
from contextvars import ContextVar
import threading
import time 

from langchain.tools import tool

NOTES_PATH = "recipes/notes"

# Tools context 
active_recipe = ContextVar('recipe')

@tool
def add_note(note: str) -> None:
    """
    Saves a note on a recipe

    note: The note that should be saved
    """

    try:
        os.makedirs(NOTES_PATH, exist_ok=True) 

        file_path = os.path.join(NOTES_PATH, f"{active_recipe.get()}.txt")

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"• {note}\n")

    except Exception as e:
        print(f"something went wrong: {e}")
        raise            

@tool
def read_notes() -> str:
    """Returns all notes for a recipe"""
    try:

        file_path = os.path.join(NOTES_PATH, f"{active_recipe.get()}.txt")

        with open(file_path, "r", encoding="utf-8") as f:
            notes = f.read()

        return notes

    except Exception as e:
        print(f"something went wrong: {e}")
        raise         

@tool
def set_timer(seconds: int) -> None:
    """
    Sets a timer for specified time
    
    seconds: number of seconds to set time
    """
    print(f"Setting {seconds} second timer")

    try:
        def _play():
            for _ in range(10):
                os.system(f'afplay "/System/Library/Sounds/Ping.aiff"')
                time.sleep(.3)
        
        threading.Timer(seconds, _play).start()
    except Exception as e:
        print(f"something went wrong: {e}")
        raise  


