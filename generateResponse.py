from dotenv import load_dotenv
from openai import OpenAI
import os
load_dotenv()

from config import model
from helpers import constructPrompt

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

def generateResponse(message, topic= "", includeRise = False):

    prompt = constructPrompt(message, topic=topic)
    #prompt = prompt + additional_context
    print("Generating Responses.....")
    with open("prompt.txt", "w") as file:
        file.write(prompt)

    completion = client.chat.completions.create(
        model=model,
        messages=[

            {
            "role": "user",
            "content": prompt,
            },
        ],
    )

    return completion.choices[0].message.content