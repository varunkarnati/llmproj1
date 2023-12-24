from langchain.llms import OpenAI,GooglePalm
import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env (especially openai api key)

s='who is walter white'
c=0
llm1=GooglePalm(google_api_key=os.environ['GOOGLE_API_KEY'],temperature=0.5)
llm2=GooglePalm(google_api_key=os.environ['GOOGLE_API_KEY'],temperature=0.5)
while(1):
    print("llm1",end=' ')
    s=llm1("ask me a new question about walter white and answer if i ask a question and the question is {s}")
    print(s)
    print("llm2:",end=' ')
    print(c)
    c+=1
    s=llm2("ask me a question about walter white and answer if i ask a question and the question is {s}")
    print(s)