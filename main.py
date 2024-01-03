# Import dependecies
import textwrap
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, load_tools, AgentType
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.llms import LlamaCpp
## text to feed
file_path ='data/finder_company_profile.txt'
with open(file_path ,'r') as file:
    finder_company_text = file.read()


embeddings = OpenAIEmbeddings()

### setting up keys for the openai
from dotenv import load_dotenv
load_dotenv()

# 1. convert text data into vector form
def text2vector(input_text_path):
    input_text = TextLoader(input_text_path).load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
    docs = splitter.split_documents(input_text)
    db = FAISS.from_documents(docs, embeddings)
    return db

# 2. receive the ranking from structuring.py
import json
def read_json_file(url='company_data.json'):
    file = open(url,)
    score_data = json.load(file)
    return score_data
    


# 3. Agent to input query and vector data to do task of recommendation


def recommender_agent(query,vdb_of_company_data,ranking,batch=4):
    docs = vdb_of_company_data.similarity_search(query)
    docs_content = " ".join([doc.page_content for doc in docs])
    llm = OpenAI()
                              
    prompt = PromptTemplate(input_variables=['query','docs','ranking'],
    template= """<s>[INST]You are a world class company recommender system that will recommend a best company \n
        
        Requirement of client company is as follows : {query}
        The information of company that you have to recommend to user is : {docs}
        The Ranking of company on various aspects is as follows : {ranking}

        Now recommend the company based on information you have i.e{docs} and {ranking}
        
        If you feel like you don't have enough information to answer the question, say "I don't know".
        
        Your answers should be verbose and detailed /n
        
        Also provide {ranking} of company in points .
        [/INST]""")
    chain = LLMChain(prompt = prompt, llm=llm)
    response = chain.run(query=query,docs= docs_content,ranking=ranking)
    return response

#### Web app implementation
import streamlit as st

st.title("Company Recommender")

json_data = read_json_file()
searching_company_data = finder_company_text
with st.sidebar:
    with st.form(key="my_form"):
        searching_company_data = st.text_area(label=" Enter your company requirements")
        sumbit_button = st.form_submit_button(label="submit")
if not searching_company_data:
    st.info("please enter your company data")
    st.stop()
else:
    vdb_of_company_data = text2vector('data/company_profile.txt')
    response = recommender_agent(query=searching_company_data,vdb_of_company_data=vdb_of_company_data,ranking=json_data)
    st.subheader("Recommendation : ")
    st.write(textwrap.fill(response))
    
## Adding more data to company profile
with open('data/company_profile_list.txt' , 'r') as file:
    company_profile = file.read()


## Adding new data to company_profile
import ast
def add_company_profile( company_profile_new, file_path):
    # Read the existing content from the file and safely evaluate it as a list
    with open(file_path, 'r') as file:
        existing_data = file.read()
        company_profile = ast.literal_eval(existing_data)

    # Append the new data (as a string) to the list
    company_profile.append(company_profile_new)

    # Write the updated list back to the file
    with open(file_path, 'w') as file:
        file.write(str(company_profile))

# Input new data from the user
new_data = st.sidebar.text_input("Enter new data for the company profile:")
    
# Button to add new data
if st.button("Add New Data"):
    if new_data:
        add_company_profile(new_data,file_path='data/company_profile.txt')
        st.success("New data added successfully!")
