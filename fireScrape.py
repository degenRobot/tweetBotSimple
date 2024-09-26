from firecrawl import FirecrawlApp
from openai import OpenAI
from together import Together

#@model = "meta-llama/llama-3.1-70b-instruct"

model = "anthropic/claude-3.5-sonnet"
togetherModel = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"

import os
from dotenv import load_dotenv
load_dotenv()

FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
together = Together(api_key=TOGETHER_API_KEY)

app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

cleanPrompt = """
You are given raw output from a website that has been scraped using a webscraper.

Take this information and create a clean summary of the information.
The summary should be in markdown format 

The summary should capture all the key points & details included in the scraped information

You should seperate each section with a header 

Key sections to include in the summary are 
# Introduction
(Key summary of the content in question i.e. what is being discussed in the content)  
# Summary:
(list out key insights from the content - this section should be details & capture all key points along with stats / references / quotes etc.)
# Additional Notes
(note any additional information that is not covered in the other sections i.e. anything informative ) 

"""

def getInfo(url, useOpenAI = False):
    scrape_result = app.scrape_url(url, params={'formats': ['markdown', 'html']})
    print("Scraping Data...")
    if useOpenAI : 
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": cleanPrompt},
                {"role": "user", "content": str(scrape_result)}
            ]
        )
    else : 
        response = together.chat.completions.create(
            model=togetherModel,
            messages=[
                {"role": "system", "content": cleanPrompt},
                {"role": "user", "content": str(scrape_result)}
            ]
        )
    print("Summary Complete.....")
    print(response.choices[0].message.content)
    return response.choices[0].message.content
    #print(scrape_result)

