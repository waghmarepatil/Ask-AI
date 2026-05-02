from sentence_transformers import SentenceTransformer


class RAGService:

    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def chunk_text(self, text, chunk_size=500, overlap=100):
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap

        return chunks

    def create_faiss_index(self, embeddings):
        import faiss
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings)
        return index

    def search(self, query, index, chunks, top_k=3):
        import numpy as np

        query_embedding = self.embedding_model.encode([query])
        query_embedding = np.array(query_embedding).astype("float32")

        distances, indices = index.search(query_embedding, top_k)

        return [chunks[i] for i in indices[0]]

    def build_context_from_pdf(self, pdf_bytes: bytes, question: str, top_k: int = 3):
        try:
            import io
            from pypdf import PdfReader
            import numpy as np

            # 1. Extract text
            reader = PdfReader(io.BytesIO(pdf_bytes))
            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            if not text.strip():
                raise Exception("No readable text found in PDF")

            # 2. Chunk
            chunks = self.chunk_text(text)

            # 3. Embeddings
            embeddings = self.embedding_model.encode(chunks)
            embeddings = np.array(embeddings).astype("float32")

            # 4. Index
            index = self.create_faiss_index(embeddings)

            # 5. Search
            results = self.search(question, index, chunks, top_k=top_k)

            # 6. Context
            context = "\n".join(results)

            return context

        except Exception as e:
            raise Exception(f"RAG processing failed: {e}")