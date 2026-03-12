class ContextBuilder:
    def build(self, chunks: list[dict]) -> str:
        return "\n".join([c.get("text", "") for c in chunks])
