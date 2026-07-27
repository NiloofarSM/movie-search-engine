import logging
import streamlit as st
from data_utils import load_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Movie Search",
    page_icon="🎬",
    initial_sidebar_state="expanded",
)

@st.cache_resource
def load_search_engine():

    return load_engine()

engine, movies, preprocessor = load_search_engine()

search_movie = st.sidebar.text_input(
    "🔍 Search movies in list",
    placeholder="e.g., Interstellar",
    key="search_movie_sidebar",
)

show_all = st.sidebar.button("📽️ Show All Movies", use_container_width=True)
if show_all:
    filtered_movies = movies
    st.sidebar.info(f"Showing all {len(movies)} movies")

elif search_movie:
    filtered_movies = movies[movies["title"].str.contains(search_movie, case=False, na=False)]
else:
    filtered_movies = None

if filtered_movies is not None:  
    if filtered_movies.empty:
        st.sidebar.warning("No movies found!")
    else:
        for _, row in filtered_movies.iterrows():
            st.sidebar.markdown(f"**{row['title']}**")
            st.sidebar.caption(f"⭐ {row['vote_average']:.1f} | {row['overview'][:80]}...")
            st.sidebar.divider()

st.sidebar.metric("Total Movies", len(movies))
st.sidebar.metric("Top Rating", f"{movies['vote_average'].max():.1f}")

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Settings")
top_k = st.sidebar.slider("Number of results", 1, 20, 10)
show_overview = st.sidebar.checkbox("Show overview", value=True)

st.markdown(
    """
# 🎬 Movie Search Engine
#### Find your favorite movies in a snap! 🙂‍↔️
"""
)
st.markdown("---")

col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input("🔍 Enter your search:", placeholder="e.g., a space adventure", key="search_input")
with col2:
    st.write("")
    st.write("")
    search_clicked = st.button("🔍 Search", type="primary", use_container_width=True)

if query or search_clicked:
    if query.strip() == "":
        st.warning("⚠️ Please enter a search term.")
    else:
        with st.spinner(f"🔍 Searching for '{query}'..."):
            results = engine.search(query, top_k=top_k)

        if not results:
            st.error(f"❌ No results found for '{query}'. Try another search!")
        else:
            st.success(f"✅ Found {len(results)} results for '{query}'")

            for i, movie in enumerate(results, start=1):
                with st.container():
                    r_col1, r_col2, r_col3 = st.columns([4, 1.2, 1.2])

                    with r_col1:
                        st.markdown(f"### {i}. {movie['title']}")
                        if i == 1:
                            st.caption("🥇 Best Match")

                    with r_col2:
                        score_percent = movie["score"] * 100
                        if score_percent > 30:
                            color, label = "🟢", "High"
                        elif score_percent > 10:
                            color, label = "🟡", "Medium"
                        else:
                            color, label = "🔴", "Low"

                        st.metric("Score", f"{score_percent:.0f}%")
                        st.caption(f"{color} {label} ")

                    with r_col3:
                        st.metric("⭐ Rating", f"{movie['vote_average']:.1f}")

                    if show_overview and movie["overview"]:
                        st.markdown(movie["overview"][:500])

                    st.markdown("---")

st.markdown("---")
st.markdown(
    """
<div style='text-align: center; color: gray;'>
    Made with ❤️ using Streamlit, TF-IDF, and Cosine Similarity
</div>
""",
    unsafe_allow_html=True,
)