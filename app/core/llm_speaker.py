import pyttsx3
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage, AIMessage

from app.config.prompts import SOUS_CHEF
from app.core.tools import add_note, read_notes, set_timer


class LLMSpeaker:
    _MODEL: str = "gpt-4o"  

    def __init__(self, recipe: str):

        self.system_prompt = SOUS_CHEF + recipe
        self.client = create_agent(
                ChatOpenAI(model=self._MODEL),
                tools=[add_note, read_notes, set_timer],
                system_prompt=self.system_prompt,
                )
        self.conversation = []
        

    def _get_response(self, prompt: str) -> str:
        self.conversation.append(HumanMessage(prompt))
        input = {"messages": self.conversation}

        response = None
        try:
            response = self.client.invoke(input)["messages"][-1]
            assert isinstance(response, AIMessage)
            self.conversation.append(response)
            return response.content

        except Exception as e:
            from pprint import pprint
            print(e)
            pprint(response)
            return "I'm sorry, something went wrong with my response"

        

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
    

