# import pandas as pd

# from preprocess import TextPreprocessor
# from indexer import SearchIndexer
# from search import SearchEngine

# movies = pd.read_csv("Data/tmdb_5000_movies.csv")
# print(movies.head(2))
# print(movies.shape)

# preprocessor = TextPreprocessor()
# text = "The astronauts are travelling through space!"
# print(preprocessor.preprocess(text))

####################################
## INDEXER TEST
# import pandas as pd
# from src.preprocess import TextPreprocessor
# from src.indexer import SearchIndexer
# movies = pd.read_csv("Data/tmdb_5000_movies.csv")
# movies["overview"] = movies["overview"].fillna("")
# preprocessor = TextPreprocessor()
# processed = movies["overview"].apply(preprocessor.preprocess)
# indexer = SearchIndexer()
# indexer.build_index(movies, processed)
# print(indexer.documents is not None)
# print(indexer.tfidf_matrix is not None)
# print(indexer.documents)

####################################
#SEARCH TEST
# import pandas as pd

# from src.preprocess import TextPreprocessor
# from src.indexer import SearchIndexer
# from src.search import SearchEngine

# movies = pd.read_csv("Data/tmdb_5000_movies.csv")
# movies["overview"] = movies["overview"].fillna("")
# preprocessor = TextPreprocessor()
# processed = preprocessor.preprocess_list(movies["overview"])
# indexer = SearchIndexer()
# indexer.build_index(movies, processed)

# engine = SearchEngine(indexer, preprocessor)

# results = engine.search("explore space adventure", top_k=5)

# for movie in results:
#     print("-" * 50)
#     print("Title :", movie["title"])
#     print("Score :", round(movie["score"], 3))
#     print("Overview :", movie["overview"][:150])

import pandas as pd

from src.preprocess import TextPreprocessor
from src.indexer import SearchIndexer
from src.search import SearchEngine  

def main():
    movies = pd.read_csv("Data/tmdb_5000_movies.csv")
    
    movies["overview"] = movies["overview"].fillna("")
    movies["title"] = movies["title"].fillna("")
    movies["text"] = movies["title"] + " " + movies["overview"]
    
    preprocessor = TextPreprocessor()
    processed = preprocessor.preprocess_list(movies["text"])
    
    # Show sample
    idx = movies[movies["title"] == "Interstellar"].index[0]
    print(f"✅ Sample preprocessing: {processed[idx][:100]}...")
    
    indexer = SearchIndexer()
    indexer.build_index(movies, processed)
    vocab = indexer.vectorizer.get_feature_names_out()
    print(f"✅ 'interstellar' in vocab: {'interstellar' in vocab}")

if __name__ == "__main__":
    main()