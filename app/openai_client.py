import os
from openai import OpenAI
from dotenv import dotenv_values

# getting env variables
env = dotenv_values(".env")

openai_client = OpenAI(api_key=env.get("OPENAI_API_KEY"))