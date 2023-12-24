from langchain.llms import OpenAI,GooglePalm
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from few_shot import few_shots

import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env (especially openai api key)


def get_few_shot_db_chain():
    db_user = "root"
    db_password = "root"
    db_host = "localhost"
    db_name = "employeedetails"

    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
                              sample_rows_in_table_info=3)
    
    llm=OpenAI(openai_api_key=os.environ["OPENAI_API_KEY"],model_name='gpt-3.5-turbo',temperature=0.05)
    #llm = ChatGoogleGenerativeAI(google_api_key=os.environ['GOOGLE_API_KEY'],model="gemini-pro",temperature=0.7)
    embeddings=OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    to_vectorize = [" ".join(example.values()) for example in few_shots]
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2,
    )
    mysql_prompt = """You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run, then look at the results of the query and return the answer to the input question.
{top_k}. You can order the results to return the most informative data in the database.
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
 And you should always count using the sql query only.You shold use GroupBy when you have to group multiple querys.
Pay attention to count the entries where you should count only using COUNT keyword in query while using groupby if there are multiple querys.when adding an employee details you should check if the employee id is mentioned , if not you should add 1 to the max integer value given to an existing employee
When a direct MYSQL query is given as a question you should execute that query directly and return the result and do nothing else. WHen you have to provide the information of an employee, You have to describe the information with column names and should not use directly the same name but describe more about it .
ANd Remember When you are instructed to insert an entry you should just display the table that has been updated .STrictly remeber You should not use any limit when required to display all the entries.
Use the following format:

Question: Question here
SQLQuery: Query to run with no pre-amble
SQLResult: Result of the SQLQuery
Answer: Result of the SQLQuery

No pre-amble.
"""

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=mysql_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
    )
    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True,use_query_checker=True, prompt=few_shot_prompt)
    return chain
