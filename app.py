import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c750f388cfbd8451f00777b68e17ec2a&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path'] if data.get('poster_path') else None

def recommend(movie):
    if isinstance(movies, pd.DataFrame):
        movie_index = movies[movies['title'] == movie].index[0]
    else:
        raise ValueError("Movies data is not in the expected DataFrame format.")
    
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        recommended_movies.append((title, movie_id))
    
    return recommended_movies

# Load movie data and similarity matrix
movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set page configuration
st.set_page_config(page_title="Movie Recommendation System", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #e6e6fa;  /* Lavender background color */
    }
    .header {
        text-align: center;
        color: #ff6347;
        padding: 20px;
        font-size: 2.5em;
        font-weight: bold;
        border-bottom: 2px solid #ff6347;
        background-color: #ffffff;
    }
    .card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        margin: 10px;
        text-align: center;
    }
    .poster {
        max-height: 300px;  /* Fixed height for posters */
        object-fit: cover;  /* Cover the element without distortion */
    }
    .footer {
        text-align: center;
        padding: 10px;
        color: #ffffff;
        background-color: #333333;
        position: fixed;
        width: 100%;
        bottom: 0;
        font-size: 0.9em;
        font-weight: bold;
    }
    .footer a {
        color: #ff6347;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">Movie Recommendation System</div>', unsafe_allow_html=True)

selected_movie_name = st.selectbox(
    'Which movie do you like?',
    movies['title']  
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    
    # Create columns dynamically
    num_cols = len(recommendations)  # Number of columns based on recommendations
    cols = st.columns(num_cols)
    
    for idx, (name, movie_id) in enumerate(recommendations):
        poster_url = fetch_poster(movie_id)
        with cols[idx]:  # Place each movie in a separate column
            st.markdown(f'<div class="card"><h4>{name}</h4>', unsafe_allow_html=True)
            if poster_url:
                st.image(poster_url, use_column_width='auto', width=150)  # Fixed width for uniformity
            else:
                st.text("Poster not available")
            st.markdown('</div>', unsafe_allow_html=True)

# Footer with custom message
st.markdown("""
    <div class="footer">
        This project is created by <a href="https://github.com/jaydugad" target="_blank">Jay Dugad</a>
    </div>
""", unsafe_allow_html=True)
