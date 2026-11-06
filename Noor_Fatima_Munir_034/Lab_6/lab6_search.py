import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class Retriever:
    def __init__(self, records, backend="tfidf", model=None):
        if not records or any(not r["text"].strip() for r in records):
            raise ValueError("Provide nonempty records")
        self.records = records
        self.backend = backend
        self.model_load_seconds = 0.0
        beginning = time.perf_counter()
        texts = [r["text"] for r in records]
        if backend == "tfidf":
            self.vectorizer = TfidfVectorizer()
            self.matrix = self.vectorizer.fit_transform(texts)
        elif backend == "embedding":
            if model is None:
                load_start = time.perf_counter()
                from sentence_transformers import SentenceTransformer
                model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
                self.model_load_seconds = time.perf_counter() - load_start
            self.model = model
            self.check_length(texts)
            self.matrix = self.model.encode(texts, normalize_embeddings=True)
        else:
            raise ValueError("Use tfidf or embedding")
        self.index_seconds = time.perf_counter() - beginning - self.model_load_seconds

    def check_length(self, texts):
        if self.backend != "embedding":
            return []
        counts = [len(self.model.tokenizer(t, truncation=False)["input_ids"]) for t in texts]
        if any(count > self.model.max_seq_length for count in counts):
            raise ValueError("Input exceeds the model limit")
        return counts

    def search(self, query, k=3, filters=None):
        if not query.strip() or k <= 0:
            return []
        if self.backend == "tfidf":
            q = self.vectorizer.transform([query])
            if q.nnz == 0:
                return []
            scores = (q @ self.matrix.T).toarray()[0]
        else:
            self.check_length([query])
            q = self.model.encode([query], normalize_embeddings=True)[0]
            scores = self.matrix @ q
        allowed = [i for i, rec in enumerate(self.records) if all(rec.get(a)==b for a,b in (filters or {}).items())]
        indexes = sorted(allowed, key=lambda i:(-float(scores[i]),i))[:k]
        return [(self.records[i],float(scores[i])) for i in indexes]

def show_hits(hits):
    if not hits:
        print("No matching records.")
    for record,score in hits:
        print(record["id"],f"score={score:.4f}",record.get("source_id",record.get("source","")))
        print(record["text"])
