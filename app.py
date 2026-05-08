import pandas as pd
import streamlit as st
import pickle
import requests

movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# fetch poster
def fetch(movie):
    response = requests.get(f'https://www.omdbapi.com/?t={movie}&apikey=dc9120d9')
    data = response.json()
    return data['Poster']

#recommendation system
def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=(lambda x:x[1]))[1:6]
    recommended_movies = []
    recommended_movie_posters = []
    for i in movie_list:
        # append name
        recommended_movies.append(movies_list.iloc[i[0]].title)
        # # append poster
        recommended_movie_posters.append(fetch(movies_list.iloc[i[0]].title))
        
    return recommended_movies, recommended_movie_posters


st.title("Movie Recommender System")
option = st.selectbox(
    'Type or select a movie from the dropdown',
    movies_list['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)
    movies = zip(recommended_movie_names, recommended_movie_posters)
    cols = [col1, col2, col3, col4, col5]

    for col, movie in zip(cols, movies):
        name, poster = movie

        with col:
            st.markdown(
                f"""
                <div style='height:60px; overflow:hidden; font-weight:bold;'>
                    {name}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.image(poster, use_container_width=True)