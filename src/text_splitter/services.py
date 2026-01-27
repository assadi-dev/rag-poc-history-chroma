from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextSplitterService:

    
    def split_text(self, text: str) -> list:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        all_splits = text_splitter.split_documents(text)
        print("Texte divisé")
        print(f"Texte divisé en {len(all_splits)} sous-documents.")
        return all_splits