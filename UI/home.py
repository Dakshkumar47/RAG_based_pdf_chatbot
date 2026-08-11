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
import io
import streamlit as st
from backend import prepare_to_chat, InvalidPdfError
# from backend import save_uploaded_file
# the code above is needed if we save the file to disk and then access it

def render_home():
    st.title("Welcome to the pdf chatbot!!!! ")
    st.header("Please use textual PDFs only")
    info = """ 1. please upload textual files only \n 2. Currently we don't have support for scanned pdfs \n 3.  More updates are on the way!!! """
    st.info(body=info)
    
    # --- 1. NORMAL FILE UPLOAD SECTION ---
    file_uploader_result = st.file_uploader(label='Please choose your file', type='pdf', key='file_uploader', max_upload_size=5)
    
    if file_uploader_result:
        st.session_state['file_object'] = file_uploader_result

    if st.button('Chat'):
        if st.session_state['file_object'] == '':
            st.warning("Please upload a file first!")
        else:
            try:
                with st.spinner(text='Getting your chatbot ready!!'):
                    prepare_to_chat()
                st.session_state['state'] = 'chat'
                st.rerun()
            except InvalidPdfError as e:
                st.error(e, icon="⚠️")

    st.divider()

    # --- 2. DEMO PDFS SECTION ---
    st.subheader("Or try one of these demo PDFs:")
    
    # Using columns side-by-side for a cleaner UI layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🏏 Virat Kohli Biography")
        if st.button("Use Virat PDF", use_container_width=True):
            
            # Read the local file using a relative path
            with open("demo_pdfs/virat_kohli.pdf", "rb") as f:
                raw_bytes = f.read()
                # Wrap it in BytesIO so it acts exactly like an uploaded file
                st.session_state['file_object'] = io.BytesIO(raw_bytes)
            
            # Trigger the exact same processing pipeline
            try:
                with st.spinner(text='Getting your demo chatbot ready!!'):
                    prepare_to_chat()
                st.session_state['state'] = 'chat'
                st.rerun()
            except InvalidPdfError as e:
                st.error(e, icon="⚠️")
                
    with col2:
        st.info("🔭 Theory of Relativity")
        if st.button("Use Relativity PDF", use_container_width=True):
            
            with open("demo_pdfs/theory_of_relativity_pdf.pdf", "rb") as f:
                raw_bytes = f.read()
                st.session_state['file_object'] = io.BytesIO(raw_bytes)
            
            try:
                with st.spinner(text='Getting your demo chatbot ready!!'):
                    prepare_to_chat()
                st.session_state['state'] = 'chat'
                st.rerun()
            except InvalidPdfError as e:
                st.error(e, icon="⚠️")
