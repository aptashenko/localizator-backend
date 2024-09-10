import os
from openai import OpenAI
from dotenv import dotenv_values

# getting env variables
config = dotenv_values(".env")

openai_client = OpenAI(api_key=config.get("OPENAI_API_KEY"))