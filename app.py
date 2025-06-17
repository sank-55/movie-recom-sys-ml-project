import streamlit as st
import pickle
import pandas as pd
import requests
import random

# Page Configuration
st.set_page_config(page_title="🎬 CineLegend Pro Max", layout="wide")

# Load Data
movies_dict = pickle.load(open('MovieRecomSYS_dict.pkl', 'rb'))
df = pd.DataFrame(movies_dict)
siml = pickle.load(open('siml.pkl', 'rb'))

# API Key
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

# Style & Background
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background: linear-gradient(135deg, #141e30, #243b55);
        background-attachment: fixed;
        font-family: 'Segoe UI', sans-serif;
        color: white;
    }
    .movie-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }
    .movie-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .movie-card:hover {
        transform: scale(1.03);
        background: rgba(255, 255, 255, 0.1);
    }
    .movie-title {
        font-size: 24px;
        font-weight: bold;
        color: #f1c40f;
        margin-top: 15px;
    }
    .genre-bubble {
        display: inline-block;
        background: linear-gradient(to right, #00f2fe, #4facfe);
        color: #fff;
        font-weight: bold;
        padding: 6px 12px;
        margin: 6px 6px 0 0;
        border-radius: 25px;
        font-size: 13px;
    }
    iframe {
        border-radius: 12px;
        margin-top: 15px;
    }
    .hover-separator {
        height: 2px;
        background: linear-gradient(to right, #fff, transparent);
        margin: 25px 0;
        opacity: 0.4;
    }
    </style>
""", unsafe_allow_html=True)

# TMDB API Functions
def fetch_movie_details(movie_id):
    details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
    videos_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}&language=en-US"

    data = requests.get(details_url).json()
    credits = requests.get(credits_url).json()
    videos = requests.get(videos_url).json()

    poster = "https://image.tmdb.org/t/p/w500" + data.get('poster_path', '')
    overview = data.get("overview", "No overview available.") + "\n\nThis cinematic gem delivers drama, thrill, and emotion with stunning visuals and storytelling."
    genres = [g['name'] for g in data.get("genres", [])]
    director = next((c['name'] for c in credits.get('crew', []) if c['job'] == 'Director'), "Unknown")
    actors = [c['name'] for c in credits.get('cast', [])][:4]

    trailer_key = next((v['key'] for v in videos.get("results", []) if v['site'] == 'YouTube' and v['type'] == 'Trailer'), None)
    trailer_url = f"https://www.youtube.com/embed/{trailer_key}" if trailer_key else None

    return poster, overview, genres, director, actors, trailer_url

# Recommendation Function
def recommend(movie):
    idx = df[df['title'] == movie].index[0]
    distances = siml[idx]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]

    recommendations = []
    for i in movie_indices:
        movie_id = df.iloc[i[0]].movie_id
        title = df.iloc[i[0]].title
        poster, overview, genres, director, actors, trailer = fetch_movie_details(movie_id)

        if ((selected_genre == "All" or selected_genre in genres) and
            (not selected_director or selected_director.lower() in director.lower()) and
            (not selected_actor or any(selected_actor.lower() in a.lower() for a in actors))):
            recommendations.append({
                'title': title,
                'poster': poster,
                'overview': overview,
                'genres': genres,
                'director': director,
                'actors': actors,
                'trailer': trailer
            })
    return recommendations

# Sidebar Filters
st.sidebar.title("🎥 CineLegend Filters")
st.sidebar.markdown("Select a movie or click a Surprise Mode!")

GENRE_OPTIONS = [
    "All", "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary",
    "Drama", "Family", "Fantasy", "History", "Horror", "Music", "Mystery",
    "Romance", "Science Fiction", "TV Movie", "Thriller", "War", "Western"
]
selected_genre = st.sidebar.selectbox("Filter by Genre", GENRE_OPTIONS)
selected_actor = st.sidebar.text_input("Filter by Actor (optional)")
selected_director = st.sidebar.text_input("Filter by Director (optional)")

# Surprise Buttons
## basically gives a movie a new taste from your genre which you will gonna love the most
## hidden gem is also recommend a movie which is underrated
if st.sidebar.button("🎲 Surprise Me (Random)"):
    selected_movie = random.choice(df['title'].values)
    st.sidebar.success(f"🎉 You got: {selected_movie}")
    movie_id = df[df['title'] == selected_movie].iloc[0].movie_id
    poster, overview, genres, director, actors, trailer = fetch_movie_details(movie_id)
    st.sidebar.image(poster, use_column_width=True)
    st.sidebar.markdown(f"**🎬 {selected_movie}**")
    st.sidebar.markdown(f"**🎭 Genres:** {', '.join(genres)}")
    st.sidebar.markdown(f"**🎬 Director:** {director}")
    st.sidebar.markdown(f"**🎟️ Stars:** {', '.join(actors)}")
    st.sidebar.markdown(f"**📖 Overview:** {overview[:200]}...")

elif st.sidebar.button("💎 Hidden Gem Mode"):
    low_popularity_movies = df.sample(frac=1).reset_index(drop=True)
    for movie in low_popularity_movies['title']:
        movie_id = df[df['title'] == movie].iloc[0].movie_id
        poster, overview, genres, director, actors, trailer = fetch_movie_details(movie_id)
        if len(overview) > 100 and len(actors) >= 2:
            selected_movie = movie
            st.sidebar.success(f"💎 Hidden Gem: {selected_movie}")
            st.sidebar.image(poster, use_column_width=True)
            st.sidebar.markdown(f"**🎬 {selected_movie}**")
            st.sidebar.markdown(f"**🎭 Genres:** {', '.join(genres)}")
            st.sidebar.markdown(f"**🎬 Director:** {director}")
            st.sidebar.markdown(f"**🎟️ Stars:** {', '.join(actors)}")
            st.sidebar.markdown(f"**📖 Overview:** {overview[:200]}...")
            break
else:
    selected_movie = st.sidebar.selectbox("Search for a Movie", df['title'].values)

# Header
st.markdown("<h1 style='text-align: center;'>🌟 CineLegend Pro Max 🌟</h1>", unsafe_allow_html=True)

# Button
if st.button("🎬 Recommend Movies"):
    results = recommend(selected_movie)

    st.markdown('<div class="movie-grid">', unsafe_allow_html=True)
    for movie in results:
        genre_html = ''.join([f'<span class="genre-bubble">{g}</span>' for g in movie['genres']])
        trailer_embed = f'<iframe width="100%" height="250" src="{movie["trailer"]}" frameborder="0" allowfullscreen></iframe>' if movie['trailer'] else '<p>🎞️ Trailer not available.</p>'
        actors_html = ', '.join(movie['actors'])
        st.markdown(f"""
            <div class="movie-card">
                <img src="{movie['poster']}" width="100%" style="border-radius: 10px;">
                <div class="movie-title">{movie['title']}</div>
                <p><strong>Director:</strong> {movie['director']}</p>
                <p><strong>Actors:</strong> {actors_html}</p>
                <p><strong>Overview:</strong> {movie['overview']}</p>
                {genre_html}
                {trailer_embed}
            </div>
            <div class="hover-separator"></div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
---
<center>© 2025 CineLegend Pro Max(s@nk) • All rights reserved</center>
""", unsafe_allow_html=True)
