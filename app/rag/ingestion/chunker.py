class Chunker:
    def chunk(self, text: str, size: int = 600, overlap: int = 80) -> list[str]:
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + size, len(text))
            chunks.append(text[start:end])
            start = end - overlap
            if start < 0:
                start = 0
        return chunks
