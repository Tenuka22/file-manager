from typing import Dict, List, Optional
from ._types import ChunkDict, IndexDict
import os
import json
import csv


def getCSVContent(file_path: str) -> List[Dict[str, str]]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        raise Exception(f"Error: The file '{file_path}' was not found.")
    except UnicodeDecodeError:
        try:
            with open(file_path, "r", encoding="latin-1") as file:
                reader = csv.DictReader(file)
                return list(reader)
        except Exception as e:
            raise Exception(f"Error reading file '{file_path}': {str(e)}")


class CSVHandler:
    def __init__(self, save_path: Optional[str] = None) -> None:
        self.save_path = save_path or "./output"
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def create_index(self, file_path: str) -> IndexDict:
        rows = getCSVContent(file_path)
        chunks: List[ChunkDict] = []
        chunk_id = 0
        current_chunk: List[str] = []

        for i, row in enumerate(rows):
            text_line = " ".join([str(v) for v in row.values() if v])
            current_chunk.append(text_line)

            if (i + 1) % 10 == 0:
                chunk_text = " ".join(current_chunk)
                chunks.append(
                    {
                        "id": chunk_id,
                        "text": chunk_text.strip(),
                        "word_count": len(chunk_text.split()),
                    }
                )
                chunk_id += 1
                current_chunk = []

        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append(
                {
                    "id": chunk_id,
                    "text": chunk_text.strip(),
                    "word_count": len(chunk_text.split()),
                }
            )

        entries: List[str] = [
            f"Row {i+1}: " + ", ".join(f"{k}={v}" for k, v in row.items())
            for i, row in enumerate(rows)
        ]

        total_rows = len(rows)
        total_chunks = len(chunks)
        word_count = sum(chunk["word_count"] for chunk in chunks)

        index: IndexDict = {
            "file": file_path,
            "type": "csv",
            "summary": f"{total_rows} rows, {total_chunks} chunks, {word_count} words",
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
    handler = CSVHandler(save_path="./tmp/indexes/csv")

    file_path = "./test-files/data.csv"
    try:
        index = handler.create_index(file_path)
        index_file = handler.save_index(index)
        print(f"Created index with {len(index['chunks'])} chunks")
        print(f"Save path: {handler.save_path}")
    except Exception as e:
        print(f"Error: {e}")
