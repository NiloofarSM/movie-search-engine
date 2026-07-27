import logging

from src.data_utils import load_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    engine, movies, preprocessor = load_engine()

    print("\n" + "=" * 60)
    print("🎬 MOVIE SEARCH")
    print("=" * 60)
    logger.info("Movie Retrieval Engine ready. Type 'quit' to exit.")

    while True:
        query = input("\nEnter movie search : ").strip()

        if query.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break

        if not query:
            print("Please enter a search term or Type 'quit' to exit.")
            continue

        results = engine.search(query, top_k=5)

        if not results:
            print("No results found for your search.")
            continue

        print(f"\nTop {len(results)} results for '{query}':\n")
        for i, movie in enumerate(results, start=1):
            print("-" * 50)
            print(f"{i}. Title: {movie['title']}")
            print(f"   Score: {movie['score']}")
            print(f"   Overview: {movie['overview'][:300]}")


if __name__ == "__main__":
    main()