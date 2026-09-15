import os
from openai import OpenAI
import chromadb

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
chroma_client = chromadb.Client()

collection = chroma_client.create_collection(
    name="rag_docs",
    metadata={"hnsw:space": "cosine"}
)

def load_documents():
    path = "data/docs.txt"
    with open(path, "r", encoding="utf-8") as f:
        docs = [line.strip() for line in f.readlines() if line.strip()]
    return docs

documents = load_documents()

def embed_text(texts):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [item.embedding for item in response.data]

def build_vector_db():
    embeddings = embed_text(documents)
    collection.add(
        documents=documents,
        embeddings=embeddings,
        ids=[f"doc_{i}" for i in range(len(documents))]
    )
    print("문서가 ChromaDB에 저장되었습니다.")

build_vector_db()

def rag_query(question):
    q_embedding = embed_text([question])[0]
    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=3
    )
    retrieved_docs = results["documents"][0]
    context = "\n".join(retrieved_docs)

    prompt = f"""
    참고 문서:

    {context}

    위 문서를 기반으로 아래 질문에 답변하세요.
    질문: {question}
    """

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print(rag_query("RAG에 대해 알려줘"))
