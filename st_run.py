import streamlit as st
import os

from build_chain import chain_multimodal_rag as chain
from build_chain import retriever
from build_chain import split_image_text_types

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]

import requests

def get_external_ip():
    response = requests.get("https://api64.ipify.org?format=json")
    if response.status_code == 200:
        data = response.json()
        return data.get("ip")
    else:
        return "Unknown"

st.title('🏥 FellowsGPT')
external_ip = get_external_ip()
os.write(1,b"External IP: ", external_ip)

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] # st.sidebar.text_input('OpenAI API Key', type='password')

def generate_response(input_text):
    llm = chain
    st.info(llm.invoke(input_text))

def print_relevant_images(inputText):
    relevantDocs = retriever.get_relevant_documents(inputText, limit=6)
    relevantDocsSplit = split_image_text_types(relevantDocs)
    if "images" in relevantDocsSplit and isinstance(relevantDocsSplit["images"], list):
        for img_base64 in relevantDocsSplit["images"]:
            image_html = f'<img src="data:image/jpeg;base64,{img_base64}" />'
            st.image(image_html)

with st.form('my_form'):
    inputText = st.text_area('Enter text:', 'What are the EV / NTM and NTM rev growth for MongoDB, Cloudflare, and Datadog?')
    submitted = st.form_submit_button('Submit')
    if not OPENAI_API_KEY.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and OPENAI_API_KEY.startswith('sk-'):
        generate_response(inputText)
        print_relevant_images(inputText)
        




