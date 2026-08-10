#---------- simplest implementation with session_state-----------------------------
"""import streamlit as st

from UI.home import home
from UI.chat import chat
from UI.preview import render_preview

if 'state' not in st.session_state:
    st.session_state['state'] = 'home'

if 'file_path' not in st.session_state:
    st.session_state['file_path'] = ''

if st.session_state['state'] == 'home':
    home()
elif st.session_state['state'] == 'preview':
    render_preview()
else:
    chat()"""


import streamlit as st


from UI.home import render_home
from UI.chat import render_preview

st.set_page_config(
    layout="wide" 
)


if 'state' not in st.session_state:
    st.session_state['state'] = 'home'

if 'loaded_pdf' not in st.session_state:
    st.session_state['loaded_pdf'] = ''

if 'file_object' not in st.session_state:
    st.session_state['file_object'] = ''

if 'pdf_path' not in st.session_state:
    st.session_state['pdf_path'] = ''

if 'pdf_chunks' not in st.session_state:
    st.session_state['pdf_chunks'] = ''

if 'vector_store' not in st.session_state:
    st.session_state['vector_store'] = ''

if 'user_query' not in st.session_state:
    st.session_state['user_query'] = ''

if 'output_parser' not in st.session_state:
    st.session_state['output_parser'] = ''

if 'retriever' not in st.session_state:
    st.session_state['retriever'] = ''

if 'prompt_template' not in st.session_state:
    st.session_state['prompt_template'] = ''

if st.session_state['state'] == 'home':
    render_home()
else:
    render_preview()
