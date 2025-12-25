import chromadb
from chromadb.config import Settings
from embeddings.embedder import get_embedding
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


client= chromadb.Client(Settings(
    persist_directory="db/chroma_db"
))

collection = client.get_or_create_collection(name="embeddings")

def _extract_embedding_vector(embedding_result):
    try:
        return embedding_result.embeddings[0].values
    except AttributeError:
        return embedding_result.embeddings[0]['values']
    except Exception as e:
        raise ValueError(f"Unable to extract embedding vector: {e}")
    
def save_version(chapter_id: str, version_text:str):
    embedding= get_embedding(version_text)
    vector = _extract_embedding_vector(embedding)
    collection.add(
        documents=[version_text],
        embeddings=[vector],
        ids=[chapter_id]
    )

def rl_reward_score(doc_embedding, query_embedding) -> float:
    doc_array = np.array(doc_embedding).reshape(1, -1)
    query_array = np.array(query_embedding).reshape(1, -1)
    return float(cosine_similarity(doc_array, query_array)[0][0])

def search_versions(query: str, top_k: int = 3, return_all: bool = False):
    if return_all:
        results = collection.get(include=["documents", "embeddings"])
        docs = results["documents"]
        ids = results["ids"]
        return [{"id": doc_id, "score": None, "text": doc} for doc_id, doc in zip(ids, docs)]

    embedding_result = get_embedding(query)
    query_vector = _extract_embedding_vector(embedding_result)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        include=["documents", "embeddings", "ids"]
    )

    docs = results["documents"][0]
    embeddings = results["embeddings"][0]
    ids = results["ids"][0]

    scored = [
        (doc, doc_id, rl_reward_score([doc_embedding], [query_vector]))
        for doc, doc_id, doc_embedding in zip(docs, ids, embeddings)
    ]
    scored.sort(key=lambda x: x[2], reverse=True)

    return [
        {"id": doc_id, "score": round(score, 4), "text": doc}
        for doc, doc_id, score in scored
    ]
