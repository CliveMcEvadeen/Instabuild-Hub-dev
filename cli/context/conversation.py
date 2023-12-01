from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import tqdm
from langchain.llms import GooglePalm
import typer
import argparse
import palm_engine
import os
from dotenv import load_dotenv
load_dotenv()


os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
# app = typer.Typer()

class Conversation:
    
    request = palm_engine.PalmEngine()
    
    def __init__(self):
        self.memory = ConversationBufferMemory()
        self.llm = GooglePalm()

    def context(self, user_prompt):
        response = self.request.api(user_prompt)
        conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True
        )
        output = conversation.predict(input=user_prompt)
        self.memory.save_context({"input": user_prompt}, {"output": response})
        return output

conversation = Conversation()

while True:
    user_prompt = input("User: ")
    if user_prompt.lower() == "exit":
        break
    output = conversation.context(user_prompt)
    print("Assistant:", output)