# instabuildhub/config.py
import os
from dotenv import load_dotenv

class Config:
    DEFAULT_OUTPUT_DIRECTORY = "output"
    PALM_API_KEY_ENV_VAR = "PALM_API_KEY"

    @classmethod
    def load_from_environment(cls):
        load_dotenv()
        cls.PALM_API_KEY = os.getenv(cls.PALM_API_KEY_ENV_VAR)

    @classmethod
    def set_api_key(cls, api_key):
        cls.PALM_API_KEY = api_key

    @classmethod
    def set_output_directory(cls, output_directory):
        cls.DEFAULT_OUTPUT_DIRECTORY = output_directory

    @classmethod
    def validate_config(cls):
        if not cls.PALM_API_KEY:
            raise ValueError("PALM API key is missing. Set it using set_api_key or through environment variables.")

    @classmethod
    def configure_from_file(cls, file_path):
        #logic to read configuration from a file, if needed
        pass
