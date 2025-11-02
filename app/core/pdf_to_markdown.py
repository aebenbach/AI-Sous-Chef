import os 

from app.config.prompts import PDF_TO_MARKDOWN

from openai import OpenAI

class PDFToMarkdown():
    _MODEL: str = 'gpt-4o'
    PDF_BASE = 'recipes/pdf'
    MD_BASE = 'recipes/markdown'

    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def _upload_pdf(self, file: str) -> str:
        with open(f'{self.PDF_BASE}/{file}.pdf', "rb") as f:
            file = self.client.files.create(
                file=f,
                purpose='assistants' # 'vision' 
            )
        file_id = file.id
        return file_id 
    
    def _read_md(self, file: str) -> str | None:
        md_path = f'{self.MD_BASE}/{file}.md'
        if not os.path.exists(md_path):
            return None 
        
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        return content



    def _extract_txt(self, file_id: str) -> str:
        # TODO Responses API
        assistant = self.client.beta.assistants.create(
            name="PDF Extractor",
            instructions=PDF_TO_MARKDOWN,
            tools=[{"type": "file_search"}],
            model=self._MODEL,
        )

        thread = self.client.beta.threads.create()

        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=PDF_TO_MARKDOWN,
            attachments=[
                {
                    "file_id": file_id,
                    "tools": [{"type": "file_search"}]
                }
            ]
        )

        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        # Wait until the run completes (polling loop)
        while True:
            run_status = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run_status.status == "completed":
                break
            elif run_status.status in ["failed", "cancelled", "expired"]:
                error_info = getattr(run_status, "last_error", None)
                raise RuntimeError(
                    f"Run failed with status: {run_status.status}. "
                    f"Details: {error_info.code if error_info else 'No error code'} - "
                    f"{error_info.message if error_info else 'No error message'}"
                )
        
        # Get the assistant's response message
        messages = self.client.beta.threads.messages.list(thread_id=thread.id)
        for msg in reversed(messages.data):
            if msg.role == "assistant":
                return msg.content[0].text.value

        raise ValueError("No assistant message found in thread.")


    def _save_as_md(self, text: str, file: str):

        with open(f'{self.MD_BASE}/{file}.md', "w", encoding="utf-8") as f:
            f.write(text)

    def pdf_to_md(self, file: str, overwrite: bool = True) -> str:
        
        if not overwrite and (markdown_text := self._read_md(file)):
            return markdown_text

        file_id = self._upload_pdf(file)
        markdown_text = self._extract_txt(file_id)
        self._save_as_md(markdown_text, file)
        return markdown_text

if __name__ == "__main__":
    reader = PDFToMarkdown()
    file = "Garlic Noodles"

    reader.pdf_to_md(file)


