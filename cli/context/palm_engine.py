import google.generativeai as palm
from dotenv import load_dotenv
import os
import pathlib

load_dotenv()

palm.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class PalmEngine:
    def __init__(self):
        pass
    @staticmethod
    def api(prompt):
        
        completion = palm.generate_text(
                                        model='models/text-bison-001',
                                        prompt=prompt,
                                        temperature=1,
                                        max_output_tokens=800,
                                        )
        if not prompt:
            return None
        else:
            # prompt = prompt
            return completion.result
    
# while True:
#     prompt=input('>:')
#     print(PalmEngine.api(prompt))