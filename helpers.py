# Generic helper functions
import inquirer
from typing import List
from together import Together
from dotenv import load_dotenv
import os
import config
import chromadb
import json
import random

import config
from chromadb.config import Settings


chroma_db_path = os.path.join(os.getcwd(), "chromadb")
chroma = chromadb.Client(Settings(persist_directory=chroma_db_path, is_persistent=True))

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

togetherClient = Together()

def get_embeddings(texts: List[str], model: str) -> List[List[float]]:
    texts = [text.replace("\n", " ") for text in texts]
    outputs = togetherClient.embeddings.create(model=model, input=texts)
    return [outputs.data[i].embedding for i in range(len(texts))]

def dropdown_selection(options):
    questions = [
        inquirer.List('selection',
                      message="Select an option",
                      choices=options,
                     ),
    ]
    answers = inquirer.prompt(questions)
    return answers['selection']


def fetch_context(message, collection, n=3):
    ### Here we want to fetch any other relevant context from vector DB 
    collection = chroma.get_or_create_collection(collection)

    embedding = get_embeddings([message], model='togethercomputer/m2-bert-80M-8k-retrieval')

    results = collection.query(query_embeddings=embedding, n=3)
    docs = results['documents'][0]
    context = "<context>"    
    for doc in docs: 
        context += doc + "\n"
        #print(doc)
    context += "</context>"
    return context


def sampleRandomExamples(nExamples = 10):

    #Load 5 Random examples from json 
    samples = "/n Below are some examples of some previous tweets you sent - use these to help style your response. Note these cover a wide range of topics. "
    loadedExamples = json.load(open("exampleMessages.json"))
    #nExamples = 100
    for i in range(nExamples):
        samples += "/nExample " + str(i) + " : " + random.choice(loadedExamples["messages"])



    return samples


    

def constructPrompt(message, topic="", includeRise = False):
    samples = sampleRandomExamples(nExamples=50)
    persona = "<style>" + config.persona  + samples + "</style>" + config.additionalInstructions
    if topic == "":
        prompt = config.createPrompt() + persona + message
    else:
        prompt = config.createPrompt(topic) + persona + message
    return prompt