# streamlit_app.py

import streamlit as st
import requests

# Set the FastAPI endpoint
API_URL = "http://localhost:8080"

st.set_page_config(page_title="Technical Document Assistant", layout="wide")

st.title("📄 Technical Document Assistant")

# Use tabs for navigation
tabs = st.tabs(["Upload PDF", "Ask a Question", "General AI Chat", "Clear History"])

with tabs[0]:
    st.header("Upload a PDF Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file is not None:
        # Send the file to the FastAPI backend
        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')}
        with st.spinner('Uploading and processing...'):
            response = requests.post(f"{API_URL}/pdf", files=files)

        if response.status_code == 200:
            st.success("File uploaded and processed successfully!")
            st.json(response.json())
        else:
            st.error("An error occurred while uploading the file.")
            st.json(response.json())

with tabs[1]:
    st.header("Ask a Question About the PDF")
    query = st.text_input("Enter your question here:", key="pdf_question_input")

    if st.button("Submit", key="submit_pdf_question") and query:
        params = {'query': query}
        with st.spinner('Getting the answer...'):
            response = requests.post(f"{API_URL}/ask_pdf", params=params)

        if response.status_code == 200:
            result = response.json()
            st.subheader("Answer:")
            st.write(result.get("answer", "No answer found."))

            st.subheader("Sources:")
            sources = result.get("sources", [])
            if sources:
                for idx, source in enumerate(sources, 1):
                    with st.expander(f"Source {idx}: {source['source']}"):
                        st.write(source['page_content'])
            else:
                st.write("No sources available.")
        else:
            st.error("An error occurred while retrieving the answer.")
            st.json(response.json())

with tabs[2]:
    st.header("General AI Chat")
    query = st.text_input("Enter your message here:", key="ai_chat_input")

    if st.button("Send", key="send_ai_chat") and query:
        params = {'query': query}
        with st.spinner('Getting the response...'):
            response = requests.post(f"{API_URL}/ai", params=params)

        if response.status_code == 200:
            result = response.json()
            st.subheader("Assistant's Response:")
            st.write(result.get("answer", "No response."))
        else:
            st.error("An error occurred while communicating with the assistant.")
            st.json(response.json())

with tabs[3]:
    st.header("Clear Chat History and Database")
    st.warning("This will clear all chat history and delete the database.")
    if st.button("Clear History", key="clear_history"):
        with st.spinner('Clearing history and database...'):
            response = requests.get(f"{API_URL}/clear")

        if response.status_code == 200:
            st.success("Chat history and database cleared successfully!")
            try:
                st.json(response.json())
            except requests.exceptions.JSONDecodeError:
                st.write("Response is not in JSON format.")
        else:
            st.error("An error occurred while clearing history.")
            try:
                st.json(response.json())
            except requests.exceptions.JSONDecodeError:
                st.write("Response is not in JSON format.")
                
if __name__ == "__main__":
    #run streamlit app
    st.write("Running streamlit app")
    
