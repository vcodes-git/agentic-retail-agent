import os
import pandas as pd

from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

class RAGService:
    def __init__(self):
        self.rag_chain = None

    def initialize_engine(self):
        print("Booting up AI Engine and reading 10,000 items...")

        # This points to: loblaw-rag-analytics/data/inventory_10k.csv
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        csv_path = os.path.join(project_root, "data", "inventory_10k.csv")

        df = pd.read_csv(csv_path)
        documents = []
        for index, row in df.iterrows():
            content = (
                f"Product: {row['name']}\nBrand: {row['brand']}\nCategory: {row['category']}\n"
                f"Price: ${row['price']} (Margin: {row['margin_pct']}%)\nStock: {row['stock_level']} units\n"
                f"Promo Status: {row['promotional_status']}\nDescription: {row['description']}"
            )
            doc = Document(page_content=content, metadata={"item_id": row['item_id'], "name": row['name']})
            documents.append(doc)

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_db = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")
        retriever = vector_db.as_retriever(search_kwargs={"k": 5}) # Increased to 5 for better context
        
        llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0.2)

        system_prompt = (
            "You are an intelligent retail data assistant for Loblaw Merchandise Analytics. "
            "Use ONLY the provided retrieved context to answer the user's question. "
            "If you don't know the answer, say 'I cannot find that in our current inventory data.' "
            "Context: {context}"        # add more context in a scaled up version?
        )
        prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{input}")])

        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        self.rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        print("[success]: AI Engine is online.")

    def ask_question(self, question: str) -> str:
        if not self.rag_chain:
            raise Exception("AI Engine is not initialized")
        response = self.rag_chain.invoke({"input": question})
        return response['answer']

# to use single instance across the app
rag_engine = RAGService()