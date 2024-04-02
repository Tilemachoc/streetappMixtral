from openai import OpenAI
from dotenv import load_dotenv
from os import getenv
import openai

load_dotenv()
api_key = getenv("OPENAI_API_KEY")
openai.api_key = api_key
client = OpenAI()