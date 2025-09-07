from google import genai
from typing import List, Optional
from .handlers._types import IndexDict
import os


class AiModel:
    def __init__(self, api_key: Optional[str]) -> None:
        if not api_key:
            raise ValueError(
                "❌ GEMINI_API_KEY is missing. Set it in your environment."
            )

        try:
            self.client = genai.Client(api_key=api_key)
        except Exception as e:
            raise RuntimeError(f"❌ Failed to initialize Gemini client: {e}") from e

    def ask_doc_question(
        self, files: List[IndexDict], user_question: str = "List all the files"
    ) -> str:
        file_summaries: List[str] = []
        for f in files:
            file_summaries.append(str(f))

        message = (
            "🔎 You are an AI-powered document analyzer.\n\n"
            "Here are the indexed files:\n"
            f"{chr(10).join(file_summaries)}\n\n"
            f"Question: {user_question}\n\n"
            "👉 Please provide a clear, concise answer based only on these files."
        )

        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=message,
            )

            if not hasattr(response, "text") or not response.text:
                return "⚠️ Gemini returned an empty response."

            return response.text

        except Exception as e:
            return f"❌ Error while querying Gemini: {e}"


if __name__ == "__main__":
    print("🔍 Testing AiModel...")

    api_key = os.getenv("GEMINI_API_KEY")

    try:
        ai = AiModel(api_key=api_key)

        dummy_files: List[IndexDict] = [
            {
                "file": "example1.txt",
                "type": "txt",
                "summary": "A simple text file about testing.",
                "chunks": [
                    {"id": 1, "text": "This is the first test file.", "word_count": 6},
                ],
                "entries": ["This is the first test file."],
            },
            {
                "file": "example2.csv",
                "type": "csv",
                "summary": "CSV file with sample user data.",
                "chunks": [
                    {"id": 1, "text": "id,name", "word_count": 2},
                    {"id": 2, "text": "1,Alice", "word_count": 2},
                    {"id": 3, "text": "2,Bob", "word_count": 2},
                ],
                "entries": ["Alice", "Bob"],
            },
        ]

        response = ai.ask_doc_question(
            files=dummy_files, user_question="Summarize what these files contain."
        )

        print("\n📝 Final Output:\n", response)

    except Exception as e:
        print("❌ Test failed:", e)
