from typing import List, TypedDict


class ChunkDict(TypedDict):
    id: int
    text: str
    word_count: int


class IndexDict(TypedDict):
    file: str
    type: str
    summary: str
    chunks: List[ChunkDict]
    entries: List[str]
