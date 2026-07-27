import json
import logging
import os

import pandas as pd

try:
    from indexer import SearchIndexer
    from preprocess import TextPreprocessor
    from search import SearchEngine
except ImportError:
    from src.indexer import SearchIndexer
    from src.preprocess import TextPreprocessor
    from src.search import SearchEngine

logger = logging.getLogger(__name__)

DATA_PATH = os.path.join("Data", "tmdb_5000_movies.csv")
INDEX_PATH = "index"


def extract_genre(genres_str) -> str:

    if not isinstance(genres_str, str) or not genres_str.strip():
        return ""
    try:
        genres_list = json.loads(genres_str)
        return " ".join(g["name"] for g in genres_list if "name" in g)
    except (json.JSONDecodeError, TypeError):
        logger.debug("Could not parse genres field: %r", genres_str)
        return ""


def load_movies(data_path: str = DATA_PATH) : 
    logger.info("Loading movie data from %s", data_path)
    movies = pd.read_csv(data_path)

    movies["title"] = movies["title"].fillna("")
    movies["overview"] = movies["overview"].fillna("")

    if "genres_text" not in movies.columns:
        if "genres" in movies.columns:
            movies["genres_text"] = movies["genres"].apply(extract_genre)
        else:
            movies["genres_text"] = ""

    movies["text"] = (
        movies["title"] + " " + movies["overview"] + " " + movies["genres_text"]).str.strip()

    return movies


def load_engine(data_path: str = DATA_PATH, index_path: str = INDEX_PATH):
 
    movies = load_movies(data_path)

    preprocessor = TextPreprocessor()
    indexer = SearchIndexer()

    if indexer.index_exists(index_path):
        logger.info("Loading existing index from '%s'...", index_path)
        indexer.load_index(index_path)
    else:
        logger.info("Preprocessing %d movie texts...", len(movies))
        processed_texts = preprocessor.preprocess_list(movies["text"].tolist())
        logger.info("Building new index...")
        indexer.build_index(movies, processed_texts)
        indexer.save_index(index_path)
        logger.info("Index built and saved at '%s'.", index_path)

    engine = SearchEngine(indexer, preprocessor)
    return engine, movies, preprocessor