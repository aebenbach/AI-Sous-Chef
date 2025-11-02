from app.core.pdf_to_markdown import PDFToMarkdown
from app.core.speech_manager import SpeechManager
from app.core.llm_speaker import LLMSpeaker

def main(file):
    reader = PDFToMarkdown()
    print("Converting Recipe")
    recipe = reader.pdf_to_md(file, overwrite=False)

    speaker = LLMSpeaker(recipe)
    callback = lambda text : speaker.q_and_a_callback(text)

    try:
        with SpeechManager(callback) as listener:
            listener.listen()
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == '__main__':
    from dotenv import load_dotenv
    import argparse

    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--recipe", required=True)
    args = parser.parse_args()

    main(args.recipe)