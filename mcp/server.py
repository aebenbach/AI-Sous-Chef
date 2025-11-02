import os 

from fastmcp import FastMCP

mcp = FastMCP("Cooking Tools")

@mcp.tool
def add_note(recipe: str, note: str) -> None:
    NOTES_PATH = "recipes/notes"
    os.makedirs(NOTES_PATH, exist_ok=True) 

    file_path = os.path.join(NOTES_PATH, f"{recipe}.txt")

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"• {note}\n")

if __name__ == "__main__":
    mcp.run()
