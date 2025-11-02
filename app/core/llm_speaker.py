import pyttsx3
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, AIMessage, SystemMessage

from app.config.prompts import SOUS_CHEF


class LLMSpeaker:
    _MODEL: str = "gpt-4o"  

    def __init__(self, recipe: str):
        self.client = ChatOpenAI(model=self._MODEL)
        # self.client = self.client.bind_tools(tools=[])

        self.system_prompt = SOUS_CHEF + recipe
        self.conversation_history: list = [
            SystemMessage(self.system_prompt)
        ]

    def _get_response(self, prompt: str) -> str:
        self.conversation_history.append(HumanMessage(prompt))

        try:
            response = self.client.invoke(self.conversation_history)

            self.conversation_history.append(response)

        except Exception as e:
            return f"API error: {e}"

        return response.content

    def _say_text(self, txt: str):
        engine = pyttsx3.init()
        engine.setProperty('rate', 165)
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
    

