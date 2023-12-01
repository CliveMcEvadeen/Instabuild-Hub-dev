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
        instructions="""you are a software developer
                        you are supposed to write code or a project needed by the user,
                        reply where necessary and name each script written,
                        be more lengthy and meaningfull in the code,
                        the code must be given in the language need by the user only,
                        each code should atleast contain not less that 500 line os code and should be in the oop concept
                        """
        
        completion = palm.generate_text(
                                        model='models/text-bison-001',
                                        prompt=prompt+instructions,
                                        temperature=0.1,
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