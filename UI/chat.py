#---------- simplest implementation with session_state-----------------------------
"""import streamlit as st

def chat():
    if st.button("home"):
        st.session_state['state'] = 'home'
        st.rerun()

    st.success("done")"""


import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from backend import chat_to_llm
# from backend import remove_temp_files
# the code above is needed if we save the file to disk and then access it

def render_preview():
    """The UploadedFile class is a subclass of BytesIO, and therefore is "file-like". This means you can pass an instance of it anywhere a file is expected."""

    if st.button(label='Home',icon='🏡'):
        st.session_state['state'] = 'home'
        st.session_state['loaded_pdf'] = ''
        st.session_state['vector_store'] = ''
        st.session_state['file_object'] = ''
        st.session_state['retriever'] = ''
        st.session_state.messages = []
        # remove_temp_files()
        # the code above is needed if we save the file to disk and then access it
        st.rerun()

        
    pdf_col,chatbot_col = st.columns(spec=[0.7,0.3])

    with pdf_col:
        try:
            # with open(st.session_state['pdf_path'],'rb') as pdf_file:
            #     binary_data = pdf_file.read()
            # the code above is needed if we save the file to disk and then access it
            binary_data = st.session_state['file_object'].getvalue()
            pdf_viewer(input=binary_data, height=800, zoom_level=0.75)

        except AttributeError:
            st.warning("please select a pdf before proceeding to chat!!!")
            raise


    with chatbot_col:
        # 1. Initialize message history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # 2. Create a fixed-height, scrollable container
        chat_container = st.container(height=700)

        # 3. Render past messages INSIDE the container
        for message in st.session_state.messages:
            with chat_container.chat_message(message["role"]):
                st.markdown(message["content"])

        # 4. The chat input sits outside the container, pinned to the bottom
        if prompt := st.chat_input("How may I help you??"):
            
            # Display user message instantly
            with chat_container.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Fetch the LLM response
            st.session_state['user_query'] = prompt
            try:
                response = chat_to_llm()
                # Display the AI response
                with chat_container.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception as e:
                st.error(f"sorry, some error occured \n {e}")



    
