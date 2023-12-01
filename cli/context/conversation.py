from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import tqdm
from langchain.llms import GooglePalm
import typer
import argparse
import palm_engine as palm
import palm_engine
import os
from dotenv import load_dotenv
load_dotenv()


os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
# app = typer.Typer()

class Conversation:
    
    # request=palm_engine.PalmEngine()
    def __init__(self, _):
        self.memory = ConversationBufferMemory()
        self.llm=GooglePalm()
        request=palm_engine.PalmEngine()
        self.response=request.api(_)

    def context(self):
        user_prompt=self.response
        conversation = ConversationChain(
                                llm=self.llm,
                                memory=self.memory,
                                verbose=True
                                )
        output=conversation.predict(input=user_prompt)
        self.memory.save_context({"input": user_prompt},
                                {"output": self.response})

        return output

while True:
     
     user_message=input('>>: ')
     ist=Conversation(user_message)
     output=ist.context()
     print(output)
     
     if user_message=='exit':
         break