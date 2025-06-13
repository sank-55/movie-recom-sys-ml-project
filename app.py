import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()
    pos = "https://image.tmdb.org/t/p/w500" + data['poster_path']
    return pos

def recommend(movie):
    movie_index = df[df['title'] == movie].index[0]  # 0 th position gives the index no. of the movie
    dists = siml[movie_index]
    movies_list = sorted(list(enumerate(dists)), reverse = True, key = lambda x: x[1])[1:6] ## main logic behind the whole code

    recommended_movies = []
    recommended_movies_posters =[]
    for i in movies_list:
        movie_id = df.iloc[i[0]].movie_id
        #fetching poster from api
        recommended_movies.append(df.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('MovieRecomSYS_dict.pkl','rb'))
df = pd.DataFrame(movies_dict) ## name of the data frame in this case
siml = pickle.load(open('siml.pkl','rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Write the name of the movie for getting suggestions...',
df['title'].values
)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])