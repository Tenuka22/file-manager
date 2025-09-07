from typing import Any, List, Optional, Union
from .app_types import ChunkDict, IndexDict
import os
import json


JSONType = Union[dict[str, Any], list[Any], str, int, float, bool, None]


def getJSONContent(file_path: str) -> JSONType:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise Exception(f"Error: The file '{file_path}' was not found.")
    except json.JSONDecodeError as e:
        raise Exception(f"Error decoding JSON file '{file_path}': {str(e)}")
    except Exception as e:
        raise Exception(f"Error reading JSON file '{file_path}': {str(e)}")


class JSONHandler:
    def __init__(self, save_path: Optional[str] = None) -> None:
        self.save_path = save_path or "./output"
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    def create_index(self, file_path: str) -> IndexDict:
        content: JSONType = getJSONContent(file_path)
        content_str: str = json.dumps(content, indent=2, ensure_ascii=False)

        chunks: List[ChunkDict] = [
            {
                "id": 0,
                "text": content_str,
                "word_count": len(content_str.split()),
            }
        ]

        entries: List[str] = []
        if isinstance(content, dict):
            for k, v in content.items():
                key: str = str(k)
                value: str = str(v)
                entries.append(f"{key}: {value}")
        elif isinstance(content, list):
            for item in content:
                entry: str = str(item)
                entries.append(entry)
        else:
            entries = [str(content)]

        total_words: int = len(content_str.split())
        total_chunks: int = len(chunks)

        index: IndexDict = {
            "file": file_path,
            "type": "json",
            "summary": f"{total_chunks} chunk(s), {total_words} words",
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
    handler = JSONHandler(save_path="./tmp/indexes/json")

    try:
        file_path = "./test-files/config.json"
        index = handler.create_index(file_path)
        index_file = handler.save_index(index)
        print(f"Created index with {len(index['chunks'])} chunks")
        print(f"Save path: {handler.save_path}")
    except Exception as e:
        print(f"Error: {e}")
