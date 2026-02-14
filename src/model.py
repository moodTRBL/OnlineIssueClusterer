import datetime

from pydantic import BaseModel


class Article(BaseModel):
    title: str
    content: str


class GeneratedEmbedding(BaseModel):
    dense: list[float]


class ClusterIssueEmbedding(BaseModel):
    issue_id: int
    dense: list[float]


class MatchCandidate(BaseModel):
    issue_id: int
    title: str
    score: float
    similarity: float


class Source(BaseModel):
    url: str
    reference: str
    category: str


class CrawlItem(BaseModel):
    title: str
    content: str
    source: Source
    url: str
    published_at: datetime.datetime


class ArticleRow(BaseModel):
    id: int
    title: str
    content: str


class IssueRow(BaseModel):
    id: int
    title: str
    updated_at: datetime.datetime
    article_count: int


class IssueEmbeddingRow(BaseModel):
    issue_id: int
    dense: list[float]


class PipelineResult(BaseModel):
    scraped: int
    saved: int
    clustered: int
    issues: list[IssueRow]
