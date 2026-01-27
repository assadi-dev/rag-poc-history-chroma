from langchain_text_splitters import RecursiveCharacterTextSplitter

class TextSplitterService:

    
    def split_text(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        all_splits = text_splitter.split_documents(docs)
        print("Texte divisé")
        print(f"Texte divisé en {len(all_splits)} sous-documents.")
        return all_splits