### How to use 

1. Install dependencies via poetry 
poetry install
then enter virtual env
poetry shell

2. Create a .env file with the following variables 
OPENROUTER_API_KEY = "sk-or-api-key"

3. Adjust config files for your use case (i.e. persona, context ,etc)
config.py has persona details 

4. Run the script 
The script to generate output (i.e. draft texts using the context + LLM api)
python testResponse.py 


### Helpers

-> config.py :
    All the below can be adjusted for your use case 
    - persona 
    - context 
    - instructions 

-> helpers.py 
    - sampleRandomExamples
    - constructPrompt
    - generateResponse


topic.txt -> drop context here
scraping -> note can also scarpe content from URLS (to do this can run topic = getInfo(url) in testResponse.py -> currently commented out & instead loads content from topic.txt)