import streamlit as st
import os

# for debugging
from build_chain import OPENAI_API_KEY
from build_chain import MONGODB_CONN_STRING
from build_chain import DB_NAME
from build_chain import VECTOR_COLLECTION_NAME
from build_chain import KEYVALUE_COLLECTION_NAME
from build_chain import VECTOR_INDEX_NAME

print(OPENAI_API_KEY, MONGODB_CONN_STRING, DB_NAME, VECTOR_COLLECTION_NAME, KEYVALUE_COLLECTION_NAME, VECTOR_INDEX_NAME)


from build_chain import chain_multimodal_rag as chain


os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = st.secrets["LANGCHAIN_API_KEY"]

st.title('🏥 FellowsGPT')

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] # st.sidebar.text_input('OpenAI API Key', type='password')

def generate_response(input_text):
    llm = chain
    st.info(llm.invoke(input_text))

with st.form('my_form'):
    text = st.text_area('Enter text:', 'What are the EV / NTM and NTM rev growth for MongoDB, Cloudflare, and Datadog?')
    submitted = st.form_submit_button('Submit')
    if not OPENAI_API_KEY.startswith('sk-'):
        st.warning('Please enter your OpenAI API key!', icon='⚠')
    if submitted and OPENAI_API_KEY.startswith('sk-'):
        generate_response(text)