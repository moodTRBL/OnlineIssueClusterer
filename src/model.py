from pydantic import BaseModel

class Article(BaseModel):
    title: str
    content: str
    
class IssueEmbedding:
    issue_id: int
    dense: list[float]

class MatchCandidate(BaseModel):
    issue_id: int
    title: str
    score: float
    similarity: float
