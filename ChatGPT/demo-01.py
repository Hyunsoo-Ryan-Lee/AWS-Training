import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.environ.get("GPT_API_KEY")
completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "say one word"}]
)
print(completion.usage)
print(completion.choices[0].message.content)