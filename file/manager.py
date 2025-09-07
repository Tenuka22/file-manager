import os
from handlers import CSVHandler, DOCXHandler, JSONHandler, TextHandler


handlers = [".csv", ".docx", ".txt", ".json", ".pdf"]


def handleFileIndexes(file_name: str, file_path: str) -> None:
    fullPath = f"{file_path}/{file_name}"
    _, ext = os.path.splitext(fullPath)
    ext = ext.lower()

    if ext == ".csv":
        fileHandler = CSVHandler("./tmp/csv")
    elif ext == ".docx":
        fileHandler = DOCXHandler("./tmp/docx")
    elif ext == ".txt":
        fileHandler = TextHandler("./tmp/txt")
    elif ext == ".json":
        fileHandler = JSONHandler("./tmp/json")
    else:
        return

    indexes = fileHandler.create_index(file_path=fullPath)
    fileHandler.save_index(index=indexes)


class FileManager:
    def __init__(self, dir: str = "./test-files") -> None:
        if not os.path.exists(dir):
            raise FileNotFoundError(f"Directory not found: {dir}")
        files = os.listdir(dir)
        for file in files:
            handleFileIndexes(file_name=file, file_path=dir)


if __name__ == "__main__":
    fm = FileManager("./test-files")
