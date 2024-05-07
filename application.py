import streamlit as st
import numpy as np
import pandas as pd
import requests
import json
from itertools import cycle

new_df = pd.read_csv('movie_data.csv')
api_key = ''  # insert tmdb api key here
with open('similiarity_scores.npy', 'rb') as f:
    similarity = np.load(f)


def return_movie_posters_link(movie):
    movie_id = new_df[new_df['title'] == movie]['movie_id'].values[0]
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    response = requests.get(url)
    return response.json()['poster_path']


def recommend(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),
                        reverse=True, key=lambda x: x[1])[1:6]
    l = []
    for i in movie_list:
        l.append(new_df.iloc[i[0]].title)
    return l


st.title("Movie Recommender System")
curr_movie = st.selectbox(label='Select a movie',
                          options=new_df['title'].values)
if st.button('Recommend'):
    rec_movies = recommend(curr_movie)
    cols = cycle(st.columns(5))

    for i in rec_movies:
        poster_link = return_movie_posters_link(i)
        next(cols).image(
            f"https://image.tmdb.org/t/p/w500/{poster_link}", f"{i}", width=130)
