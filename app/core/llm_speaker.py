import pyttsx3
from openai import OpenAI
from app.config.prompts import SOUS_CHEF


class LLMSpeaker:
    _MODEL: str = "gpt-4o"  

    def __init__(self, recipe: str):
        self.client = OpenAI()
        self.system_prompt = SOUS_CHEF + recipe
        self.conversation_history: list[dict] = [
            {"role": "system", "content": self.system_prompt}
        ]

    def _get_response(self, prompt: str) -> str:
        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self._MODEL,
                messages=self.conversation_history,
                temperature=0.7,  # controls creativity
                max_completion_tokens=500,  # replaces max_tokens
            )

            output = response.choices[0].message.content

        except Exception as e:
            return f"API error: {e}"

        self.conversation_history.append({"role": "assistant", "content": output})
        return output

    def _say_text(self, txt: str):
        engine = pyttsx3.init()
        engine.say(txt)
        engine.runAndWait()

    def q_and_a_callback(self, text: str):
        resp = self._get_response(text)
        print("LLM Response: ", resp)
        self._say_text(resp)



if __name__ == "__main__":
    test_recipe = "Boil pasta for 8 minutes"
    speaker = LLMSpeaker(test_recipe)

    speaker.q_and_a_callback("What does the recipe say to do?")

    speaker.q_and_a_callback("Anything else?")
    

