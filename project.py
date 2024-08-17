import streamlit as st
import pandas as pd
import numpy as np

st.title("Movie Recommendation System")

import pickle
movie = pickle.load(open('movie.pkl','rb'))
movies_list = movie['title'].values

cosine_similarity = pickle.load(open('cosinesimilarity.pkl','rb'))
count = pickle.load(open('count.pkl','rb'))

vote_counts = movie['vote_count'].astype('int')
vote_averages = movie['vote_average'].astype('int')
c = vote_averages.mean()
m = vote_counts.quantile(0.60)

def weighted_rating(x):
    v = x['vote_count']
    R = x['vote_average']
    return (v/(v+m) * R) + (m/(m+v) * c)

def improved_recommendations(title,movies_preprocessed):
    count_matrix = count.fit_transform(movies_preprocessed['soup'])
    cosine_sim = cosine_similarity(count_matrix,count_matrix)
    movies_preprocessed = movies_preprocessed.reset_index()
    titles = movies_preprocessed['title']
    indices = pd.Series(movies_preprocessed.index, index=movies_preprocessed['title'])
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]

    pred = movies_preprocessed.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'year']]
    vote_counts = pred['vote_count'].astype('int')
    vote_averages = pred['vote_average'].astype('int')
    c = vote_averages.mean()
    m = vote_counts.quantile(0.40)
    qualified = pred[(pred['vote_count'] >= m)]
    qualified['wr'] = qualified.apply(weighted_rating,axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(10).title
    return qualified



movie_name = st.selectbox(
    "Which movie would you like getting recommendations for?",
    movies_list,
)

option = st.selectbox(
    "Interested in getting recommendations from any specific year or decade?",
    ("None (suggest all year)", "decade", "year"),
)
if option=='year':
    number = st.number_input("Select the year (max - 2016)")
    st.write("The current number is ", number)
    
if option=='decade':
    number = st.number_input("Select the decade(ex: 1970 for 1970s, max - 2010)")
    st.write("The current number is ", number)
    

if st.button("Recommend"):
    if option=='None (suggest all year)':
        recom = improved_recommendations(movie_name,movie)
        for i in recom:
            st.write(i)
    elif option=='decade':
        movie_2=movie[movie['decade']==number]
        a=movie[movie['title']==movie_name].index[0]
        b = movie_2.index
        if (a not in b):
            movie_2.loc[a]=movie.loc[a]
        movie_2= movie_2.reset_index()
        movie_2.drop(columns='index',inplace=True)
        recom = improved_recommendations(movie_name,movie_2)
        for i in recom:
            st.write(i)
    elif option=='year':
        movie_2=movie[movie['year']==number]
        a=movie[movie['title']==movie_name].index[0]
        b = movie_2.index
        if (a not in b):
            movie_2.loc[a]=movie.loc[a]
        movie_2= movie_2.reset_index()
        movie_2.drop(columns='index',inplace=True)
        recom = improved_recommendations(movie_name,movie_2)
        for i in recom:
            st.write(i)

