import re
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from pinecone_text.sparse import BM25Encoder

import time
import logging

from model import Article, EmbeddingResult, IssueEmbedding

        
class Vectorizer:
    """
    Generates embeddings using Pydantic models for data encapsulation.
    """
    
    def __init__(self):
        logging.info("모델 로딩중")
        self.dense_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)        
        logging.info("모델 로드 성공")

    def embed(self, article: Article) -> EmbeddingResult:
        """
        단일 Article을 입력받아 EmbeddingResult(Pydantic) 반환
        """
        full_text = article.title + ' ' + article.content
        
        dense_vec = self.dense_model.encode(full_text, convert_to_numpy=True).tolist()
                
        return IssueEmbedding(
            dense=dense_vec,
        )