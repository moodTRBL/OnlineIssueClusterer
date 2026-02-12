from pydantic import BaseModel

class Article(BaseModel):
    title: str
    content: str
    
class ArticleVector(BaseModel):
    vector: list[float]

class EmbeddingFeature(BaseModel):
    token_title: list[float]
    token_content: list[float]
    token_combine: list[float]
    
    lemma_title: list[float]
    lemma_content: list[float]
    lemma_combine: list[float]
    
    entity_title: list[float]
    entity_content: list[float]
    entity_combine: list[float]

class ArticleFeature(BaseModel):
    tokens: str
    lemmas: str
    entity: str
    

class EmbeddingResult(BaseModel):
    dense: list[float]
    sparse_indice: list[int]
    sparse_value: list[float]
    # entity: list[str]
