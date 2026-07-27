import logging
import re
import string
from typing import Iterable, List

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

logger = logging.getLogger(__name__)

_NLTK_RESOURCES = {"stopwords": "corpora/stopwords"}

for resource, path in _NLTK_RESOURCES.items():
    try:
        nltk.data.find(path)
    except LookupError:
        logger.info("Downloading NLTK resource: %s", resource)
        nltk.download(resource)

class TextPreprocessor:

    def __init__(self) :
        self.stopwords = set(stopwords.words("english"))
        self.stemmer = PorterStemmer()
        logger.debug("TextPreprocessor initialized with %d stopwords.", len(self.stopwords))

    @staticmethod
    def decontracted(text: str) :
        text = re.sub(r"won't", "will not", text)
        text = re.sub(r"can't", "can not", text)
        text = re.sub(r"n't", " not", text)
        text = re.sub(r"'re", " are", text)
        text = re.sub(r"'s", " is", text)
        text = re.sub(r"'d", " would", text)
        text = re.sub(r"'ll", " will", text)
        text = re.sub(r"'ve", " have", text)
        text = re.sub(r"'m", " am", text)
        return text

    def preprocess(self, text: str) :
       
        if not isinstance(text, str):
            return ""

        text = self.decontracted(text)
        text = text.lower()
        text = re.sub(r"[^\x00-\x7F]+", " ", text)
        text = text.translate(str.maketrans("", "", string.punctuation))
        text = re.sub(r"[0-9]+", "", text)

        tokens = text.split()
        filtered_tokens: List[str] = []

        for word in tokens:
            if word in self.stopwords or len(word) <= 1:
                continue
            filtered_tokens.append(self.stemmer.stem(word))

        processed = " ".join(filtered_tokens)
        return processed

    def preprocess_list(self, texts: Iterable[str]) :
        return [self.preprocess(t) for t in texts]