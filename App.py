import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image
import base64
import time

# Page configuration
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 42px;
        font-weight: bold;
        color: #FF4B4B;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 28px;
        color: #4B4B4B;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .recommendation {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #FF4B4B;
        font-size: 18px;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #D32F2F;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 5px;
        border: 1px solid #E0E0E0;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        color: #9E9E9E;
        font-size: 14px;
    }
    .movie-card {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        margin-bottom: 15px;
    }
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .movie-title {
        padding: 10px;
        text-align: center;
        font-weight: bold;
        background-color: rgba(255,75,75,0.1);
    }
    </style>
    """, unsafe_allow_html=True)


# Function to add background
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Uncomment and use this if you have a background image
# add_bg_from_local('path/to/your/image.jpg')

# Function to fetch movie poster
def fetch_movie_poster(movie_title):
    """
    Fetch movie poster from TMDB API

    Parameters:
        movie_title (str): The title of the movie

    Returns:
        str: URL of the movie poster or None if not found
    """
    api_key = "8ba578bb6928d140e247e499d464ff23"

    # Search for the movie
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"

    try:
        response = requests.get(search_url)
        if response.status_code == 200:
            data = response.json()
            if data['results'] and len(data['results']) > 0:
                # Get the first movie result
                movie_id = data['results'][0]['id']

                # Get poster path
                poster_path = data['results'][0]['poster_path']
                if poster_path:
                    return f"https://image.tmdb.org/t/p/w500{poster_path}"

        return None  # Return None if no poster found
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return None


# Recommendation function
def recommend_movies(movie):
    """
    Generate movie recommendations based on similarity to the selected movie.

    Parameters:
        movie (str): The title of the selected movie

    Returns:
        list: A list of recommended movie titles
    """
    # Find the index of the selected movie
    movie_index = movies_data[movies_data['title'] == movie].index[0]

    # Get similarity scores
    distances = similarities[movie_index]

    # Get top 5 similar movies (excluding the selected movie)
    similar_movies = sorted(list(enumerate(distances)),
                            reverse=True,
                            key=lambda x: x[1])[1:6]

    # Extract recommended movie titles
    recommendations = []
    for i in similar_movies:
        movie_id = i[0]
        # fetch from API
        recommendations.append(movies_data.iloc[i[0]]["title"])

    return recommendations


# Load data with error handling
@st.cache_data
def load_data():
    try:
        movies_data = pickle.load(open('movies.pkl', 'rb'))
        similarities = pickle.load(open('similarities', 'rb'))
        return movies_data, similarities
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None


# Load data
movies_data, similarities = load_data()

if movies_data is not None and similarities is not None:
    # Extract movie titles
    movies_list = movies_data['title'].values

    # Application header
    st.markdown("<h1 class='main-header'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

    # App description
    st.markdown("""
    <div style="background-color: rgba(255,255,255,0.8); padding: 20px; border-radius: 10px; margin-bottom: 30px;">
    <p style="font-size: 18px; line-height: 1.6;">
    Discover new movies based on your favorites! This recommender system uses advanced algorithms to find films with similar 
    themes, styles, and content to ones you already love. Just select a movie from the dropdown and click "Recommend" to see your personalized suggestions.
    </p>
    </div>
    """, unsafe_allow_html=True)

    # Create two columns
    col1, col2 = st.columns([2, 1])

    with col1:
        # Movie selection dropdown
        selected_movie = st.selectbox(
            "🎯 Select a movie you enjoy",
            movies_list,
            help="Choose a movie from the dropdown list"
        )

    with col2:
        # Recommend button
        recommend_button = st.button("🔍 Find Similar Movies")

    # Selected movie poster (if available)
    if selected_movie:
        selected_movie_poster = fetch_movie_poster(selected_movie)
        if selected_movie_poster:
            st.image(selected_movie_poster, width=200, caption=f"Selected: {selected_movie}")

    # Show spinner during recommendation
    if recommend_button:
        with st.spinner('Finding the perfect movies for you...'):
            time.sleep(1)  # Simulating processing time

            # Get recommendations
            recommended_movies = recommend_movies(selected_movie)

            # Display recommendations
            st.markdown("<h2 class='sub-header'>💫 Recommended Movies</h2>", unsafe_allow_html=True)

            # Create columns for posters - up to 5 movies per row
            cols = st.columns(5)

            for i, movie in enumerate(recommended_movies):
                with cols[i % 5]:
                    # Fetch poster
                    poster_url = fetch_movie_poster(movie)

                    st.markdown(f"""
                    <div class="movie-card">
                    """, unsafe_allow_html=True)

                    if poster_url:
                        st.image(poster_url, width=150, use_container_width=True)
                    else:
                        # Display placeholder if no poster found
                        st.markdown(f"""
                        <div style='height:225px; background-color:#f0f0f0; 
                        display:flex; justify-content:center; align-items:center;'>
                        <p style='text-align:center;'>No poster available</p>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="movie-title">
                    <p>#{i + 1} {movie}</p>
                    </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Success message
            st.success("Recommendations generated successfully!")

    # Footer
    st.markdown("<div class='footer'>© 2025 Movie Recommender System | Powered by AI</div>", unsafe_allow_html=True)
else:
    st.error("Unable to load movie data. Please check your data files and try again.")