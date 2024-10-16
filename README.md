# Technical Document Assistant

An AI-powered assistant for interacting with technical PDF documents. Upload PDFs, ask questions about their content, and engage in general AI chat.

## Features

- **Upload PDFs**: Process and analyze PDF documents.
- **Ask Questions**: Query the content of uploaded PDFs.
- **AI Chat**: Engage in general conversations with the AI assistant.
- **Clear History**: Reset chat history and database.

## Prerequisites

- Python >= 3.8
- pip
- Ollama (for running local LLM models)
- ChromaDB (for vector storage)
- LLM Model: llama2 or compatible model for Ollama

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/Shubhamjoshi-root/qp-ai-assessment.git
    cd qp-ai-assessment
    ```

2. **Create a Virtual Environment (Optional)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

    If `requirements.txt` is missing, install:

    ```bash
    pip install fastapi uvicorn langchain streamlit requests pdfplumber chromadb
    ```

4. **Install Ollama**

    Follow the Ollama Installation Guide. For macOS users:

    ```bash
    brew install ollama
    ```

5. **Download the LLM Model**

    ```bash
    ollama pull llama2
    ```

6. **Install ChromaDB**

    ```bash
    pip install chromadb
    ```

## Running the Application

1. **Start Ollama**

    ```bash
    ollama serve
    ```

2. **Run the FastAPI Backend**

    ```bash
    python fastapi_app.py
    ```

3. **Run the Streamlit Frontend**

    ```bash
    streamlit run streamlit_app.py
    ```

## Usage

- **Upload PDF**: Go to the "Upload PDF" tab, choose a PDF file, and upload.
- **Ask a Question**: Navigate to "Ask a Question", enter your query, and submit.
- **General AI Chat**: Use the "General AI Chat" tab to converse with the assistant.
- **Clear History**: In the "Clear History" tab, click "Clear History" to reset.

## Troubleshooting

- **Import Errors**: Ensure all necessary packages are installed and imports are correct.
- **Ollama Issues**: Verify Ollama is running and the model is correctly installed.
- **Port Conflicts**: Change the ports in [fastapi_app.py](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22e%3A%5C%5Cexperiment%5C%5Clangflow%5C%5CDocumention-workflow%5C%5Cfastapi_app.py%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2Fe%3A%2Fexperiment%2Flangflow%2FDocumention-workflow%2Ffastapi_app.py%22%2C%22scheme%22%3A%22file%22%7D%7D) and Streamlit if needed.

## License

This project is licensed under the MIT License.