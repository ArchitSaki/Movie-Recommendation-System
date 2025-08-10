import pickle
import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
import time

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.getenv('TMDB_API_KEY', '83d09bdf8b934823853ec996d6df72e9')}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "poster_path" in data and data["poster_path"]:
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    return "https://via.placeholder.com/500"
    
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        time.sleep(0.5)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    cols = st.columns(len(names))  # create columns based on number of recommendations
    
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)
            

