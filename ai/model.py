from google import genai


class AiModel:
    def __init__(self, api_key: None | str) -> None:
        self.client = genai.Client(api_key=api_key, project="file-manager")
