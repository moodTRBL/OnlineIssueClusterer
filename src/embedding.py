import re
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
from pinecone_text.sparse import BM25Encoder

import time
import logging

from model import Article, EmbeddingResult

        
class Vectorizer:
    """
    Generates embeddings using Pydantic models for data encapsulation.
    """
    
    def __init__(self):
        logging.info("모델 로딩중")
        self.dense_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True)
        self.bm_model = BM25Encoder()
        
        logging.info("모델 로드 성공")

    def fit(self, corpus: list[str]):
        self.bm_model.fit(corpus)

    def embed(self, article: Article) -> EmbeddingResult:
        """
        단일 Article을 입력받아 EmbeddingResult(Pydantic) 반환
        """
        full_text = article.title + ' ' + article.content
        
        dense_vec = self.dense_model.encode(full_text, convert_to_numpy=True).tolist()
        
        bm25_results = self.bm_model.encode_documents(full_text)
        sparse_indices = bm25_results['indices']
        sparse_values = bm25_results['values']
        
        return EmbeddingResult(
            dense=dense_vec,
            sparse_indice=sparse_indices, 
            sparse_value=sparse_values,   
        )