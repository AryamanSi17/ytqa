from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()

embeddings = OpenAIEmbeddings()

def vector_db_from_youtube(video_url:str)->FAISS:
    loader=YoutubeLoader.from_youtube_url(video_url)
    transcipt=loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(transcipt)
    vector_db = FAISS.from_documents(docs, embeddings)
    return vector_db

def query_result(db,query,k=4):
    docs=db.similarity_search(query,k=k)
    docs_text=" ".join([d.page_content for d in docs])
    llm=ChatOpenAI(model_name="gpt-4o")
    prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a helpful assistant that answers questions based on the transcript."
    ),
    HumanMessagePromptTemplate.from_template(
        """Answer the following question: {question}
           Using only this transcript: {docs}
           If you don’t know, say "I don't know"."""
    ),
    ])
    
    chain=LLMChain(llm=llm,prompt=prompt)
    response = chain.run(question=query, docs=docs_text)
    response = response.replace("\n", "")
    return response, docs