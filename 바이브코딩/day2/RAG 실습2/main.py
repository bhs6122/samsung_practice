import os
from typing import List
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import OpenAI
import chromadb
from chromadb.config import Settings

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


VECTOR_STORE_DIR = "./vector_store"
chroma_client = chromadb.PersistentClient(path=VECTOR_STORE_DIR)

COLLECTION_NAME = "rag_docs"

app = FastAPI(title="RAG FastAPI Example")
templates = Jinja2Templates(directory="templates")

DOC_PATH = "data/docs.txt"

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-5-nano"
TOP_K = 5

class AskRequest(BaseModel):
    question: str


def load_documents(path: str) -> List[str]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return [l for l in lines if l]


def embed_texts(texts: List[str]) -> List[List[float]]:
    resp = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in resp.data]


LAST_MTIME_PATH = "./vector_store/docs_mtime.txt"

def get_saved_mtime():
    if not os.path.exists(LAST_MTIME_PATH):
        return None
    try:
        with open(LAST_MTIME_PATH, "r") as f:
            return float(f.read().strip())
    except:
        return None

def save_mtime(mtime: float):
    os.makedirs(os.path.dirname(LAST_MTIME_PATH), exist_ok=True)
    with open(LAST_MTIME_PATH, "w") as f:
        f.write(str(mtime))



def prepare_vector_store():
    current_mtime = os.path.getmtime(DOC_PATH) if os.path.exists(DOC_PATH) else None
    saved_mtime = get_saved_mtime()

    docs_changed = (saved_mtime is None) or (current_mtime != saved_mtime)

    if docs_changed:
        print("🔄 docs.txt 변경 감지됨 → 벡터 DB 재구축합니다.")
        try:
            chroma_client.delete_collection(COLLECTION_NAME)
            print("📌 기존 컬렉션 삭제 완료")
        except:
            print("⚠ 기존 컬렉션 삭제 실패 또는 존재하지 않음")

    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    if docs_changed:
        docs = load_documents(DOC_PATH)
        if not docs:
            print("⚠ docs.txt가 비어있습니다.")
            return collection

        print(f"📄 {len(docs)}개의 문서를 재임베딩하여 저장합니다...")

        embeddings = embed_texts(docs)
        ids = [f"doc_{i}" for i in range(len(docs))]

        collection.add(documents=docs, embeddings=embeddings, ids=ids)

        save_mtime(current_mtime)
        print("✅ 벡터DB 갱신 완료")

    else:
        print("✔ 변경 없음 → 기존 벡터DB 그대로 사용합니다.")

    return collection


collection = prepare_vector_store()


def rag_answer(question: str) -> str:
    q_emb = embed_texts([question])[0]

    results = collection.query(query_embeddings=[q_emb], n_results=TOP_K)

    retrieved_docs = results.get("documents", [[]])[0]
    context = "\n\n".join(retrieved_docs)

    prompt = f"""
아래 참고 문서를 바탕으로 질문에 한국어로 답변하세요.

참고 문서:
{context}

질문: {question}
"""

    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=512,
    )

    return resp.choices[0].message.content.strip()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/ask")
def api_ask(req: AskRequest):
    try:
        return {"answer": rag_answer(req.question)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
