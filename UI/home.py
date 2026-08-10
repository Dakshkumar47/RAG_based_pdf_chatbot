#---------- simplest implementation with session_state-----------------------------
"""import streamlit as st

def home():
    file_path = st.text_input(label='file_path',placeholder='enter the file path')
    st.session_state['file_path'] = file_path
    st.write(st.session_state['file_path'])

    if st.button('upload'):
        st.session_state['state'] = 'preview'
        st.rerun()
"""

"""The UploadedFile class is a subclass of BytesIO, and therefore is "file-like". This means you can pass an instance of it anywhere a file is expected."""

import streamlit as st
from backend import prepare_to_chat
# from backend import save_uploaded_file
# the code above is needed if we save the file to disk and then access it

def render_home():
    st.title("Welcome to the pdf chatbot!!!! ")
    file_uploader_result = st.file_uploader(label='please choose your file',type='pdf',key='file_uploader',max_upload_size=5)
    if file_uploader_result:
        st.session_state['file_object'] = file_uploader_result

    if st.button('chat'):
        #save_uploaded_file(st.session_state['file_object'])
        # the code above is needed if we save the file to disk and then access it
            
        if st.session_state['file_object'] == '':
            st.warning("please upload a file first")
        else:
            st.session_state['state'] = 'chat'
            with st.spinner(show_time=True,text='getting your chatbot ready!!'):
                prepare_to_chat()
            st.rerun()
