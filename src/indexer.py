import logging
import os
import pickle
from typing import Iterable, Optional

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

logger = logging.getLogger(__name__)


class SearchIndexer:
 
    def __init__(self) :
        self.vectorizer: TfidfVectorizer = TfidfVectorizer(
            max_features=5000,
            min_df=2,
            max_df=0.8,
            ngram_range=(1, 2),
        )

        self.tfidf_matrix = None
        self.documents: Optional[pd.DataFrame] = None
        logger.debug("SearchIndexer initialized with TF-IDF vectorizer.")

    def build_index(self, documents: pd.DataFrame, texts: Iterable[str]) :
        logger.info("Building TF-IDF index...")
        self.documents = documents.reset_index(drop=True)
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)

    def save_index(self, path: str = "index"):
        os.makedirs(path, exist_ok=True)

        with open(os.path.join(path, "vectorizer.pkl"), "wb") as f:
            pickle.dump(self.vectorizer, f)
        with open(os.path.join(path, "tfidf_matrix.pkl"), "wb") as f:
            pickle.dump(self.tfidf_matrix, f)
        with open(os.path.join(path, "documents.pkl"), "wb") as f:
            pickle.dump(self.documents, f)

        logger.info("Index saved at '%s'.", path)

    def load_index(self, path: str = "index") :
        with open(os.path.join(path, "vectorizer.pkl"), "rb") as f:
            self.vectorizer = pickle.load(f)
        with open(os.path.join(path, "tfidf_matrix.pkl"), "rb") as f:
            self.tfidf_matrix = pickle.load(f)
        with open(os.path.join(path, "documents.pkl"), "rb") as f:
            self.documents = pickle.load(f)

        logger.info("Index loaded from '%s'.", path)

    def index_exists(self, path: str = "index") -> bool:
        required = [
            os.path.join(path, "vectorizer.pkl"),
            os.path.join(path, "tfidf_matrix.pkl"),
            os.path.join(path, "documents.pkl"),
        ]
        exists = all(os.path.exists(p) for p in required)
        logger.debug("Index exists at '%s': %s", path, exists)
        return exists