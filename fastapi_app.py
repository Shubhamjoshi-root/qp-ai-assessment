from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever
import uvicorn
import os

app = FastAPI()

chat_history = []
folder_path = "db"

cached_llm = Ollama(model="llama3.2")

embedding = FastEmbedEmbeddings()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)

raw_prompt = PromptTemplate.from_template(
    """ 
    <s>[INST] You are a technical assistant good at searching documents.  If the answer is not in the context, say "I don't know the answer.". [/INST] </s>
    [INST] {input}
           Context: {context}
           Answer:
    [/INST]
"""
)


@app.post("/ai")
async def ai_post(query: str):
    print("Post /ai called")
    # json_content = await request.json()
    # query = json_content.get("query")

    print(f"query: {query}")

    response = cached_llm.invoke(query)

    print(response)

    response_answer = {"answer": response}
    return JSONResponse(content=response_answer)


@app.post("/ask_pdf")
async def ask_pdf_post(query: str):
    # print("Post /ask_pdf called")
    # json_content = await request.json()
    # query = json_content.get("query")

    print(f"query: {query}")

    print("Loading vector store")
    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)

    print("Creating chain")
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 3,
            "score_threshold": 0.1,
        },
    )

    retriever_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            (
                "human",
                "Given the above conversation, generate a search query to lookup in order to get information relevant to the conversation",
            ),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm=cached_llm, retriever=retriever, prompt=retriever_prompt
    )

    document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
    
    retrieval_chain = create_retrieval_chain(
        history_aware_retriever,
        document_chain,
    )

    result = retrieval_chain.invoke({"input": query})
    print(result["answer"])
    chat_history.append(HumanMessage(content=query))
    chat_history.append(AIMessage(content=result["answer"]))

    sources = [
        {"source": doc.metadata["source"], "page_content": doc.page_content}
        for doc in result["context"]
    ]

    response_answer = {"answer": result["answer"], "sources": sources}
    return JSONResponse(content=response_answer)


@app.post("/pdf")
async def pdf_post(file: UploadFile = File(...)):
    file_name = file.filename
    save_file = f"pdf/{file_name}"
    os.makedirs(os.path.dirname(save_file), exist_ok=True)

    with open(save_file, "wb") as buffer:
        buffer.write(await file.read())
    print(f"filename: {file_name}")

    loader = PDFPlumberLoader(save_file)
    docs = loader.load_and_split()
    print(f"docs len={len(docs)}")

    chunks = text_splitter.split_documents(docs)
    print(f"chunks len={len(chunks)}")

    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=folder_path
    )

    vector_store.persist()

    response = {
        "status": "Successfully Uploaded",
        "filename": file_name,
        "doc_len": len(docs),
        "chunks": len(chunks),
    }
    return JSONResponse(content=response)

@app.get("/clear")
async def clear():
    global chat_history
    chat_history = []
    #delete db folder
    import shutil
    shutil.rmtree(folder_path)     
    return JSONResponse(content={"status": "Chat history cleared."})


def start_app():
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    start_app()
