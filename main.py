from file_manager.manager import FileManager
import os
from file_manager.gemini import AiModel


def main() -> None:
    cwd = os.getcwd()
    userPath = (
        input("Give your folder (relative to cwd or absolute): ") or "./test-files"
    )

    if os.path.isabs(userPath):
        dir = userPath
    else:
        dir = os.path.join(cwd, userPath)

    if not os.path.exists(dir):
        print(f"❌ Directory does not exist: {dir}")
    else:
        fm = FileManager(dir=dir, temp_location="tmp")
        ai = AiModel(os.getenv("GEMINI_API_KEY"))

        while True:
            print("")
            user_question = input("How can I help you today: ")
            res = fm.askQuestion(user_question, ai=ai, temp_location="tmp")
            print(res)


if __name__ == "__main__":
    main()
