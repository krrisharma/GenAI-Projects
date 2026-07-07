from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)
from langchain_core.output_parsers import StrOutputParser

from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


def build_chain(video_id):

    # -------------------- Step 1 : Transcript --------------------

    try:
        transcripts = YouTubeTranscriptApi().fetch(
            video_id,
            languages=["en"]
        )

    except TranscriptsDisabled:
        raise Exception("Transcript is disabled for this video.")

    except NoTranscriptFound:
        raise Exception("No English transcript found.")

    text = " ".join(
        snippet.text for snippet in transcripts
    )

    # -------------------- Step 2 : Text Splitting --------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=250
    )

    chunks = splitter.create_documents([text])

    # -------------------- Step 3 : Embeddings --------------------

    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-en-v1.5"
    )

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    # -------------------- Step 4 : Retriever --------------------

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    # -------------------- Step 5 : Prompt --------------------

    prompt = PromptTemplate(
        template="""
        You are a helpful assistant.

        Answer ONLY from the provided transcript context.

        If the context is insufficient, just say you don't know.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """,
        input_variables=["context", "question"]
    )

    parallel_chain = RunnableParallel(
        context=retriever
        | RunnableLambda(
            lambda docs: "\n\n".join(
                doc.page_content for doc in docs
            )
        ),
        question=RunnablePassthrough()
    )

    # -------------------- Step 6 : LLM --------------------

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    parser = StrOutputParser()

    chain = parallel_chain | prompt | llm | parser

    return chain