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

    def read_prompt_from_file(self, prompt_file):
        """
        Read user prompts from a file.

        Parameters:
            - prompt_file (str): Path to the file containing user prompts.

        Returns:
            - list: List of user prompts.
        """
        user_queries = []
        try:
            if prompt_file:
                with open(prompt_file, 'r') as file:
                    instructions = [line.strip() for line in file]
                    for instruction in instructions:
                        user_queries.append(instruction)
            return user_queries
        except FileNotFoundError:
            return []
        
    def process_prompt_file(self, prompt_file):
        """
        Process user prompts from a file and interact with the assistant.

        Parameters:
            - prompt_file (str): Path to the file containing user prompts.
        """
        user_queries = self.read_prompt_from_file(prompt_file)

        if not user_queries:
            print("No valid user prompts found in the file.")
            return

        for user_prompt in user_queries:
            output = self.context(user_prompt)
            print(f"User: {user_prompt}")
            print(f"Assistant: {output}")
            print("=" * 50)

    def save_memory(self, filename="memory.json"):
        """
        Save the conversation memory to a file.

        Parameters:
            - filename (str): Name of the file to save the memory.
        """
        self.memory.save_to_file(filename)

    def load_memory(self, filename="memory.json"):
        """
        Load conversation memory from a file.

        Parameters:
            - filename (str): Name of the file to load the memory.
        """
        self.memory.load_from_file(filename)

    def clear_memory(self):
        """Clear the conversation memory."""
        self.memory.clear()

    def format_output(self, user_prompt, assistant_response):
        """
        Format the output for better presentation.
        
        Parameters:
            - user_prompt (str): User's input.
            - assistant_response (str): Assistant's generated response.

        Returns:
            - str: Formatted output.
        """
        return f"User: {user_prompt}\nAssistant: {assistant_response}"


conversation = Conversation()
    
while True:
    
    user_prompt = input("User: ")
    if user_prompt.lower() == "exit":
        break
    output = conversation.context(user_prompt)
    print("Assistant:", output)