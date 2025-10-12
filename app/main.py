from app.core.pdf_to_markdown import PDFToMarkdown
from app.core.speech_manager import SpeechManager
from app.core.llm_speaker import LLMSpeaker

def main():
    reader = PDFToMarkdown()
    file = "Garlic Noodles"
    print("Converting Recipe")
    recipe = reader.pdf_to_md(file)

    speaker = LLMSpeaker(recipe)
    callback = lambda text : speaker.q_and_a_callback(text)

    try:
        with SpeechManager(callback) as listener:
            listener.listen()
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == '__main__':
    main()