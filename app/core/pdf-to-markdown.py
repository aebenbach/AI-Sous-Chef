import os 

from app.config.prompts import PDF_TO_MARKDOWN

from openai import OpenAI

class PDFToMarkdown():
    PDF_BASE: str = 'recipes/markdown'
    MD_BASE: str = 'recipes/markdown'
    _MODEL: str = 'gpt-4o'

    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def _upload_pdf(self, path: str) -> str:
        with open(path, "rb") as f:
            file = self.client.files.create(
                file=f,
                purpose='vision' 
            )
        file_id = file.id
        return file_id 

    def _extract_txt(self, file_id: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PDF_TO_MARKDOWN},
                        {"type": "image_file", "image_file": {"file_id": file_id, "detail": "high"}}
                    ]
                }
            ]
        )
        return response.choices[0].message.content

    def _save_as_md(self, text: str, path: str):

        os.makedirs(os.path.dirname(path), exist_ok=True)


        if not path.endswith(".md"):
            path += ".md"

        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

def pdf_to_md(self, fname: str):
    if not fname.lower().endswith(".pdf"):
        pdf_filename = f"{fname}.pdf"
    else:
        pdf_filename = fname

    pdf_path = os.path.join(self.PDF_BASE, pdf_filename)
    file_id = self._upload_pdf(pdf_path)
    markdown_text = self._extract_txt(file_id)
    base_name = os.path.splitext(fname)[0]
    md_path = os.path.join(self.MD_BASE, f"{base_name}.md")
    self._save_as_md(markdown_text, md_path)

if __name__ == "__main__":
    reader = PDFToMarkdown()
    file = "Garlic Noodles"
    reader.pdf_to_md(file)
