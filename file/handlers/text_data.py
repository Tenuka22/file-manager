from typing import List, Optional
import json
import os
from .app_types import ChunkDict, IndexDict


def getTextContent(file_path: str) -> List[str]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        raise Exception(f"Error: The file '{file_path}' was not found.")
    except UnicodeDecodeError:
        try:
            with open(file_path, "r", encoding="latin-1") as file:
                return [line.strip() for line in file.readlines() if line.strip()]
        except Exception as e:
            raise Exception(f"Error reading text file '{file_path}': {str(e)}")


class TextHandler:
    def __init__(self, save_path: Optional[str] = None) -> None:
        self.save_path = save_path or "./output"
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def create_index(self, file_path: str) -> IndexDict:
        paragraphs = getTextContent(file_path)
        chunks: List[ChunkDict] = []
        current_chunk_text: List[str] = []
        chunk_id = 0

        for i, paragraph_text in enumerate(paragraphs):
            current_chunk_text.append(paragraph_text)

            if (i + 1) % 10 == 0 or (i + 1) == len(paragraphs):
                chunk_content = " ".join(current_chunk_text).strip()
                if chunk_content:
                    chunks.append(
                        {
                            "id": chunk_id,
                            "text": chunk_content,
                            "word_count": len(chunk_content.split()),
                        }
                    )
                    chunk_id += 1
                current_chunk_text = []

        if current_chunk_text:
            chunk_content = " ".join(current_chunk_text).strip()
            if chunk_content:
                chunks.append(
                    {
                        "id": chunk_id,
                        "text": chunk_content,
                        "word_count": len(chunk_content.split()),
                    }
                )

        entries: List[str] = [
            f"Paragraph {i+1}: {para_text}" for i, para_text in enumerate(paragraphs)
        ]

        total_words = sum(len(p.split()) for p in paragraphs)
        total_paragraphs = len(paragraphs)
        total_chunks = len(chunks)

        index: IndexDict = {
            "file": file_path,
            "type": "text",
            "summary": f"{total_paragraphs} paragraphs, {total_chunks} chunks, {total_words} words",
            "chunks": chunks,
            "entries": entries,
        }
        return index

    def save_index(self, index: IndexDict, output_file: Optional[str] = None) -> str:
        if not output_file:
            file_path = str(index.get("file", ""))
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_file = f"{base_name}_index.json"

        if not os.path.dirname(output_file):
            output_file = os.path.join(self.save_path, output_file)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        print(f"Index saved to: {output_file}")
        return output_file

    def load_index(self, index_file: str) -> IndexDict:
        if not os.path.exists(index_file):
            alt_path = os.path.join(self.save_path, index_file)
            if os.path.exists(alt_path):
                index_file = alt_path

        with open(index_file, "r", encoding="utf-8") as f:
            return json.load(f)


if __name__ == "__main__":
    handler = TextHandler(save_path="./tmp/indexes/text")

    try:
        index = handler.create_index("./test-files/notes.txt")
        index_file = handler.save_index(index)
        print(f"Created index with {len(index['chunks'])} chunks")
        print(f"Save path: {handler.save_path}")
    except Exception as e:
        print(f"Error: {e}")
