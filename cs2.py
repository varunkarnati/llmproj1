from langchain.agents import create_csv_agent
import pandas as pd
from langchain.agents import create_pandas_dataframe_agent
from langchain.chat_models import ChatOpenAIOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain.utilities import SQLDatabase
from langchain.agents.agent_types import AgentType
from dotenv import load_dotenv
import os
import streamlit as st


def main():
    load_dotenv()
    llm=ChatOpenAIOpenAI(openai_api_key=os.environ['OPENAI_API_KEY'],model_name='gpt-3.5-turbo',temperature=0.05)
    # Load the OpenAI API key from the environment variable
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")
    db_user = "root"
    db_password = "root"
    db_host = "localhost"
    db_name = "employeedetails"

    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
                              sample_rows_in_table_info=3)
    
    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
    

    st.set_page_config(page_title="Ask your CSV")
    st.header("Ask your CSV 📈")

    csv_file = st.file_uploader("Upload a CSV file", type="csv")
    if csv_file is not None:
        df = pd.read_csv(csv_file)
        # pd_agent = create_pandas_dataframe_agent(OpenAI(model_name='gpt-3.5-turbo',temperature=0), 
        #                  df, 
        #                  verbose=True)
        #prompt=llm(f"return a MYSQL query to create a table with table name NY and insert values from a dataframe{df} and check for the dates in the values")
        chain.run(f"create a table with table name NYtable and insert values from a dataframe{df} and check for the dates in the values")
        st.write("done importing")

        # user_question = st.text_input("Ask a question about your CSV: ")

        # if user_question is not None and user_question != "":
        #     with st.spinner(text="In progress..."):
        #         user_question=llm("return this string{user_question} with today's actual date")
        #         st.write(pd_agent.run(user_question))


if __name__ == "__main__":
    main()