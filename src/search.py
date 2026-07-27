import logging

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

try:
    from spellchecker import SpellChecker
    _SPELLCHECK_AVAILABLE = True
except ImportError:
    _SPELLCHECK_AVAILABLE = False
    logger.warning(
        "pyspellchecker not installed; queries will be searched without spelling correction. "
    )


class SearchEngine:

    def __init__(self, indexer, preprocessor, use_spellcheck: bool = True):
        self.indexer = indexer
        self.preprocessor = preprocessor
        self.spell_checker = SpellChecker(language="en") if (use_spellcheck and _SPELLCHECK_AVAILABLE) else None
        logger.debug("SearchEngine initialized (spellcheck=%s).", self.spell_checker is not None)

    def _correct_spelling(self, query: str) :
        if self.spell_checker is None:
            return query

        corrected_words = []
        for word in query.split():
            corrected = self.spell_checker.correction(word)
            corrected_words.append(corrected if corrected else word)
        return " ".join(corrected_words)

    def search(self, query: str, top_k: int = 5):

        corrected_query = self._correct_spelling(query)
        if corrected_query != query:
            logger.info("Spelling corrected: '%s' -> '%s'", query, corrected_query)

        processed_query = self.preprocessor.preprocess(corrected_query)
        if processed_query == "":
            return []

        query_vector = self.indexer.vectorizer.transform([processed_query])

        similarities = cosine_similarity(query_vector, self.indexer.tfidf_matrix).flatten()
        
        if similarities.max() == 0:
            return []

        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            movie = self.indexer.documents.iloc[idx]
            results.append({
                "title": movie["title"],
                "overview": movie["overview"],
                "vote_average": movie["vote_average"],
                "score": round(float(similarities[idx]), 4),
            })

        return results