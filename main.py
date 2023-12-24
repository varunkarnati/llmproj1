import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv() 
from lang import get_few_shot_db_chain
st.title("ChatDB")
from langchain.llms import OpenAI,GooglePalm, LlamaCpp
import pandas as pd
#from exp import write_string_to_pdf
import json
from table import table

question = st.text_input("Question: ")
llm=OpenAI(openai_api_key=os.environ["OPENAI_API_KEY"],model_name='gpt-3.5-turbo-1106',temperature=0.5)

if question:
    chain = get_few_shot_db_chain()
    try:
        response = chain.run(question)
    
        response=llm(f"describe this statement as a table for the question {question} and the response is{response} ")
    except Exception as e:
        print(e)
        response = 'Something went Wrong. '
    st.header("Answer")
    # if(llm(f"if you this this response {response} for the question {question} is appropriate return 0 else return 1")):
    #     response=chain.run(question)
    st.write(response)
    
    llm_response = llm(f"convert this response to a json {response}")

    # Convert the LLM response to a pandas DataFrame (replace this with your actual data processing logic)
    #result_dict = json.loads(llm_response)
    

    # Display the DataFrame in Streamlit
    
    
    # Add a download button to download the DataFrame as a CSV file
    #csv_data = pd.DataFrame(result_dict).to_csv(index=False).encode('utf-8')
    try:
        st.download_button(label="Download CSV", data=table(llm_response).encode('utf-8'), file_name="llm_response.csv", key="download_csv")
        # llm_response=llm(f"write an beautiful interpretation of this response {llm_response} to present it in a pdf formt")
        
        # st.download_button(
        # label="Download PDF",
        # data=write_string_to_pdf('download.pdf',llm_response),
        # file_name="download.pdf",
        # key="download_pdf")
    
    except Exception as e:
        pass
        # llm_response=llm(f"write an beautiful interpretation of this response {llm_response} to present it in a pdf formt")
        # st.write( 'Only PDF format is available')
        # st.download_button(
        # label="Download PDF",
        # data=write_string_to_pdf('download.pdf',llm_response),
        # file_name="download.pdf",
        # key="download_pdf"
    








