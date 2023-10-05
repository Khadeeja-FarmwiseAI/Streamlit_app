import streamlit as st
import openai
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_hub.youtube_transcript import YoutubeTranscriptReader
from pathlib import Path
from llama_index import download_loader
from pytesseract import pytesseract
from htmlTemplate import css, bot_template, user_template

pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
openai.api_key = "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"


def chat_pdf():
    docs = SimpleDirectoryReader(r"C:/Users/RBT/Desktop/data/pdf").load_data()
    print("loaded ")

    if 'chat_chain' not in st.session_state:
        st.session_state.chat_chain = []

    st.write(css, unsafe_allow_html=True)

    index = VectorStoreIndex.from_documents(docs)
    print("finished ")

    st.subheader("PDF ChatBot :books:")

    def handle_output(user_input):
        query_engine = index.as_query_engine()
        result = query_engine.query(user_input)
        st.session_state.chat_chain.append({user_input: result.response})
        # st.write('inside', st.session_state.chat_chain)
        for i in st.session_state.chat_chain:
            questions = list(i.keys())
            answers = list(i.values())
            st.write(user_template.replace(
                "{{MSG}}", questions[0]), unsafe_allow_html=True)
            st.write(bot_template.replace(
                "{{MSG}}", answers[0]), unsafe_allow_html=True)

    question = st.chat_input("Ask your question here :")
    if question:
        handle_output(question)


def chat_script():
    loader = YoutubeTranscriptReader()
    documents = loader.load_data(ytlinks=['https://www.youtube.com/watch?v=i3OYlaoj-BM'])
    print(documents)

    if 'chat_chain' not in st.session_state:
        st.session_state.chat_chain = []

    st.write(css, unsafe_allow_html=True)

    index = VectorStoreIndex.from_documents(documents)

    st.subheader("Youtube Transcript ChatBot ")

    def handle_output(user_input):
        query_engine = index.as_query_engine()
        result = query_engine.query(user_input)
        st.session_state.chat_chain.append({user_input: result.response})
        # st.write('inside', st.session_state.chat_chain)
        for i in st.session_state.chat_chain:
            questions = list(i.keys())
            answers = list(i.values())
            st.write(user_template.replace(
                "{{MSG}}", questions[0]), unsafe_allow_html=True)
            st.write(bot_template.replace(
                "{{MSG}}", answers[0]), unsafe_allow_html=True)

    question = st.chat_input("Ask your question here :")
    if question:
        handle_output(question)


def chat_image():
    ImageReader = download_loader("ImageReader")

    loader = ImageReader(text_type="plain_text")
    documents = loader.load_data(file=Path(r"C:/Users/RBT/Desktop/data/images/img_1.jpg"))
    print("loaded 2")

    if 'chat_chain' not in st.session_state:
        st.session_state.chat_chain = []

    st.write(css, unsafe_allow_html=True)

    index = VectorStoreIndex.from_documents(documents)
    print("finished ")

    st.subheader(" Images ChatBot  ")

    def handle_output(user_input):
        query_engine = index.as_query_engine()
        result = query_engine.query(user_input)
        st.session_state.chat_chain.append({user_input: result.response})
        # st.write('inside', st.session_state.chat_chain)
        for i in st.session_state.chat_chain:
            questions = list(i.keys())
            answers = list(i.values())
            st.write(user_template.replace(
                "{{MSG}}", questions[0]), unsafe_allow_html=True)
            st.write(bot_template.replace(
                "{{MSG}}", answers[0]), unsafe_allow_html=True)

    question = st.chat_input("Ask your question here :")
    if question:
        handle_output(question)


st.title(" AI ChatBot")

col1, col2, col3 = st.columns(3)

with col1:
    st.title(" 📚")

with col2:
    st.title("📜")

with col3:
    st.title("🖼️")

with st.sidebar:
    option = st.selectbox(
        'What would you like to be chat with?',
        ('Select', 'Pdfs', 'Youtube Scripts', 'Images'))

    if option == 'Select':
        st.write('You selected: None')
    else:
        st.write('You selected:', option)

with st.spinner("Processing"):
    if option == 'Pdfs':
        chat_pdf()
    elif option == 'Youtube Scripts':
        chat_script()
    elif option == 'Images':
        chat_image()


