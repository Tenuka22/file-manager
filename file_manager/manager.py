import os
from typing import List
from .handlers.docx_data import DOCXHandler
from .gemini import AiModel
from .handlers.json_data import JSONHandler, getJSONContent
from .handlers.csv_data import CSVHandler
from .handlers.text_data import TextHandler
from .handlers._types import IndexDict

handlers = [".csv", ".docx", ".txt", ".json", ".pdf"]


def handleFileIndexes(file_name: str, file_path: str, temp_location: str) -> None:
    fullPath: str = os.path.join(file_path, file_name)

    _, ext = os.path.splitext(fullPath)
    ext = ext.lower()

    if os.path.isabs(temp_location):
        location: str = temp_location
    else:
        location = os.path.join(os.getcwd(), temp_location)

    os.makedirs(location, exist_ok=True)

    if ext == ".csv":
        fileHandler = CSVHandler(os.path.join(location, "csv"))
    elif ext == ".docx":
        fileHandler = DOCXHandler(os.path.join(location, "docx"))
    elif ext == ".txt":
        fileHandler = TextHandler(os.path.join(location, "txt"))
    elif ext == ".json":
        fileHandler = JSONHandler(os.path.join(location, "json"))
    else:
        print(f"⚠️ Unhandled file type, skipping {fullPath}")
        return

    indexes = fileHandler.create_index(file_path=fullPath)
    fileHandler.save_index(index=indexes)


class FileManager:
    def __init__(self, dir: str = "./test-files", temp_location: str = "tmp/") -> None:
        if not os.path.exists(dir):
            raise FileNotFoundError(f"Directory not found: {dir}")

        files = os.listdir(dir)
        for file in files:
            handleFileIndexes(
                file_name=file, file_path=dir, temp_location=temp_location
            )

    def askQuestion(self, question: str, ai: AiModel, temp_location: str) -> str:
        location = (
            temp_location
            if os.path.isabs(temp_location)
            else os.path.join(os.getcwd(), temp_location)
        )
        folders = os.listdir(location)

        fileData: List[IndexDict] = []

        for folder in folders:
            folder_path = os.path.join(location, folder)
            if not os.path.isdir(folder_path):
                continue

            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                fileData.append(getJSONContent(file_path))  # type: ignore

        return ai.ask_doc_question(files=fileData, user_question=question)


if __name__ == "__main__":
    print("🔍 Running FileManager test...")

    fm = FileManager()

    ai = AiModel(api_key=os.getenv("GEMINI_API_KEY"))

    try:
        response = fm.askQuestion("List all files indexed", ai, temp_location="tmp/")
        print("✅ AI Response:\n", response)
    except Exception as e:
        print("❌ Error during test:", e)
