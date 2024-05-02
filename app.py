import streamlit as st
import pandas as pd
import pickle
import requests
from pathlib import Path
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from fuzzywuzzy import process

import urllib3
from bs4 import BeautifulSoup
import re
from mechanize import Browser
import json
# import requests
from bs4 import BeautifulSoup
from requests import get
# import pandas as pd
from urllib.parse import urlparse
import httplib2
import urllib.request
import sqlite3
import re
import sys

from dash import html, dcc, Dash, callback, Input, Output, State
import dash_bootstrap_components as dbc 

external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]
app = Dash(__name__, external_stylesheets=external_css)



# def if_webpage_exists(url):

# 	requested_web_page = requests.get(url)

# 	if (requested_web_page.status_code == 200):
# 		return 1
# 	return 0


# def extract_data(url):

# 	with urllib.request.urlopen(url) as response:
# 		contents = response.read()

# 	return contents 
 

# ### To extract the movie trailer page on youtube
# def get_movie_trailer_page(movie):

# 	movie_dup = movie.replace(' ', '+')

# 	youtube_link = "https://www.youtube.com/"
# 	movie_url = youtube_link + "results?search_query=" + movie_dup

# 	return movie_url


# ### To extract the movie trailer
# def fetch_trailer(movie):

# 	movie_link_to_be_parsed = get_movie_trailer_page(movie)

# 	data = extract_data(movie_link_to_be_parsed)
# 	soup = BeautifulSoup(data, features="html5lib")

# 	for link in soup.find_all('a'):
# 		if ('/watch?v=' in link.get('href')):
# 			return "https://www.youtube.com" + link.get('href')




# --- USER AUTHENTICATION ---
names = ["Sandeep Pratap", "Pratyaya Prakash", "Govind Pandey", "Abhinav Kumar"]
usernames = ["sandeep007", "pratyaya057", "govind047", "abhinav008"]

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "movies_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main") # main body or side-bar

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:

#     def fetch_poster(movie_id):
#         url = "https://api.themoviedb.org/3/movie/{}?api_key=4dcaab1bf38b4ba42fd052fa044d92b8".format(movie_id)
#         data=requests.get(url)
#         data=data.json()
#         poster_path = data['poster_path']
#         full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
#         return full_path

        


    def fetch_poster(title):
        api_key = "993d52f7"  # Replace with your OMDb API key
        base_url = "http://www.omdbapi.com/"

        params = {
            't': title,
            'apikey': api_key,
        }

        response = requests.get(base_url, params=params)
        data = response.json()

        if 'Poster' in data and data['Poster'] != 'N/A':
            poster_url = data['Poster']
            return poster_url
        else:
            return None

    # def fetch_trailer(movie_id):
    #     # Construct the URL to fetch movie details
    #     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4dcaab1bf38b4ba42fd052fa044d92b8&append_to_response=videos"
        
    #     # Make the API request
    #     response = requests.get(url)
    #     data = response.json()

    #     # Check if the 'videos' key is present in the response
    #     if 'videos' in data and 'results' in data['videos']:
    #         videos = data['videos']['results']
            
    #         # Search for a trailer among the videos
    #         for video in videos:
    #             # Assuming trailers are of type 'Trailer' and hosted on YouTube
    #             if video['type'] == 'Trailer' and 'YouTube' in video['site']:
    #                 # Construct the YouTube trailer URL
    #                 trailer_key = video['key']
    #                 trailer_url = f"https://www.youtube.com/watch?v={trailer_key}"
    #                 return trailer_url

    #     # Return None if no trailer is found
    #     return None

    
    def if_webpage_exists(url):

        requested_web_page = requests.get(url)

        if (requested_web_page.status_code == 200):
            return 1
        return 0


    def extract_data(url):

        with urllib.request.urlopen(url) as response:
            contents = response.read()

        return contents 
    

    ### To extract the movie trailer page on youtube
    def get_movie_trailer_page(movie):

        movie_dup = movie.replace(' ', '+')

        youtube_link = "https://www.youtube.com/"
        movie_url = youtube_link + "results?search_query=" + movie_dup

        return movie_url


    ### To extract the movie trailer
    def fetch_trailer(movie):

        movie_link_to_be_parsed = get_movie_trailer_page(movie)

        data = extract_data(movie_link_to_be_parsed)
        soup = BeautifulSoup(data, features="html5lib")

        for link in soup.find_all('a'):
            if ('/watch?v=' in link.get('href')):
                return "https://www.youtube.com" + link.get('href')




    def movie_finder(title, all_titles):
        closest_match = process.extractOne(title, all_titles)
        return closest_match[0]

    def recommend(movie):
        index=movies[movies['title']==movie].index[0]
        distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
        recommend_movie=[]
        similarity_score=[]
        recommend_poster=[]
        recommend_trailer=[]
        recommend_genres=[]
        recommend_tagline=[]
        recommend_overview=[]
        recommend_cast=[]
        recommend_director=[]
    
        for i in distance[1:6]:
            movies_id=movies.iloc[i[0]].id
            recommend_movie.append(movies.iloc[i[0]].title)
            similarity_score.append(i[1])
            recommend_poster.append(fetch_poster(movies.iloc[i[0]].title))
            recommend_trailer.append(fetch_trailer(movies.iloc[i[0]].title))
            recommend_genres.append(movies.iloc[i[0]].genres)
            recommend_tagline.append(movies.iloc[i[0]].tagline)
            recommend_overview.append(movies.iloc[i[0]].overview)
            recommend_cast.append(movies.iloc[i[0]].cast)
            recommend_director.append(movies.iloc[i[0]].director)

        # return recommend_movie, similarity_score,  recommend_poster, recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director
        return recommend_movie, similarity_score,  recommend_poster, recommend_trailer, recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director

    # movies = pickle.load(open("movies_list.pkl", 'rb'))
    movies = pd.read_pickle("movies_list.pkl")
    similarity = pickle.load(open("similarity.pkl", 'rb'))
    movies_list=movies['title'].values

    # logout
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")

    st.title("Movie Recommender System")

     # Search movie option
    user_input = st.text_input("Search for a movie:")
    if user_input:
        corrected_movie = movie_finder(user_input, movies_list.tolist())
        st.info(f"Corrected Movie Input: {corrected_movie}")

        # Recommendation for the corrected movie
        if st.button("Show Similar Movies"):
            # recommend_movie, similarity_score, recommend_poster, recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director = recommend(corrected_movie)
            recommend_movie, similarity_score, recommend_poster, recommend_trailer, recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director = recommend(corrected_movie)

            cols = st.columns(5)

            for i, col in enumerate(cols):
                with col:
                    st.markdown(f"**{recommend_movie[i]}**")
                    st.image(recommend_poster[i], use_column_width=True)
                    st.video(recommend_trailer[i])
                    # st.markdown(f"[Watch Trailer]({recommend_trailer[i]})")
                    st.markdown(f"**Similarity-score:** {similarity_score[i]:.5f}")

                    with st.expander(f"Movie Description"):
                        st.markdown("**Tagline:** " + f"{recommend_tagline[i]}")
                        st.markdown("**Genres:** " + f"{recommend_genres[i]}")
                        st.markdown("**Overview:** " + f"{recommend_overview[i]}")
                        st.markdown("**Cast:** " + f"{recommend_cast[i]}")
                        st.markdown("**Director:** " + f"{recommend_director[i]}")


    selectvalue=st.selectbox("Select movie from dropdown", movies_list)

    if st.button("Show Recommendation"):
        # movie_name, movie_similarity, movie_poster, movie_genres, movie_tagline, movie_overview, movie_cast, movie_director = recommend(selectvalue)
        movie_name, movie_similarity, movie_poster, movie_trailer, movie_genres, movie_tagline, movie_overview, movie_cast, movie_director = recommend(selectvalue)
        # if isinstance(selectvalue, str):
        #     # Call the recommend function with the correct movie title
        #     movie_name, movie_similarity, movie_poster, movie_trailer, movie_genres, movie_tagline, movie_overview, movie_cast, movie_director = recommend(selectvalue)
        # else:
        #     # Handle the case where selectvalue is not a string (e.g., it's an integer ID)
        #     st.error("Invalid selection. Please select a movie from the dropdown.")

        cols=st.columns(5)

        for i, col in enumerate(cols):

            with col:    
                st.markdown(f"**{movie_name[i]}**")
                st.image(movie_poster[i], use_column_width=True)
                st.markdown(f"**Similarity-score:** {movie_similarity[i]:.5f}")
                st.video(movie_trailer[i])
                # st.markdown(f"[Watch Trailer]({movie_trailer[i]})")


                with st.expander(f"Movie Description"):
                    st.markdown("**Tagline:** "+f"{movie_tagline[i]}")
                    st.markdown("**Genres:** "+f"{movie_genres[i]}")
                    st.markdown("**Overview:** "+f"{movie_overview[i]}")
                    st.markdown("**Cast:** "+f"{movie_cast[i]}")
                    st.markdown("**Director:** "+f"{movie_director[i]}")
                # html.Div([
                # dbc.button("Movie Description", id= "close",  n_clicks=0),
                # dbc.Modal([
                #     dbc.ModalHeader(dbc.ModalTitle("Movie Details")),
                #     dbc.ModalBody(
                #         [
                #         st.markdown("**Tagline:** "+f"{movie_tagline[i]}")
                #         st.markdown("**Genres:** "+f"{movie_genres[i]}")
                #         st.markdown("**Overview:** "+f"{movie_overview[i]}")
                #         st.markdown("**Cast:** "+f"{movie_cast[i]}")
                #         st.markdown("**Director:** "+f"{movie_director[i]}")
                #         ]
                #     ),
                #     dbc.ModalFooter(dbc.Button("Close", id= "close", className="ms-auto", n_clicks=0)),
                # ],
                # id="modal",
                # is_open=False,
                # ),
                # ], className="col", style={"height": "100vh", "background-color": "#e5ecf6"}
                # )
                # @app.callback(Output("modal", "is_open"), [Input("open", "n_clicks"), Input("close", "n_clicks")], [State("modal", "is_open")])
                # def toggle_modal(n1,n2, is_open):
                #     if n1 or n2:
                #         return not is_open
                #     return is_open

        # if st.session_state.search_history and selectvalue not in st.session_state.search_history:
        #     st.session_state.search_history.append(selectvalue)
        # elif not st.session_state.search_history:
        #     st.session_state.search_history.append(selectvalue)

    # # Display search history
    # st.sidebar.title("Search History")
    # for search in st.session_state.search_history[-5:][::-1]:  # Display the last 5 searches in reverse order
    #     st.sidebar.write(search)

    # # Display 5 popular movies on the home screen in one row with 5 columns
    # st.header("Popular Movies")
    # popular_movies = movies.dropna(subset=['genres']).sort_values(by='popularity', ascending=False).head(5)
    # cols= st.columns(5)

    # for i, col in enumerate(cols):

    #     if i < len(popular_movies):

    #         movie = popular_movies.iloc[i]  # Access the row of the DataFrame

    #         movie_name = movie['title']
    #         movie_poster = fetch_poster(movie['id'])
    #         popularity = movie['popularity']
    #         movie_trailer = fetch_trailer(movie['id'])


    #         with col:    
    #             st.markdown(f"**{movie_name}**")
    #             st.image(movie_poster, use_column_width=True)
    #             st.markdown(f"**Popularity:** {popularity:.2f}")
    #             # st.markdown(f"**Similarity-score:** {movie_similarity:.5f}")
    #             st.video(movie_trailer)

    #             with st.expander(f"Movie Description"):
    #                 st.markdown("**Tagline:** "+f"{movie['tagline']}")
    #                 st.markdown("**Genres:** "+f"{movie['genres']}")
    #                 st.markdown("**Overview:** "+f"{movie['overview']}")
    #                 st.markdown("**Cast:** "+f"{movie['cast']}")
    #                 st.markdown("**Director:** "+f"{movie['director']}")

    # Create a dictionary where keys are genres and values are lists of movie titles in that genre
    genre_movies = {}

    for index, row in movies.iterrows():
        genres = row['genres']
        if isinstance(genres, str):  # Check if 'genres' is a valid string
            genres = genres.split(' ')
            for genre in genres:
                if genre in genre_movies:
                    genre_movies[genre].append(row['title'])
                else:
                    genre_movies[genre] = [row['title']]

    # Select a genre from the list
    selected_genre = st.selectbox("Select a genre", ['All'] + list(genre_movies.keys()))

    # Add a button to show the results
    show_results = st.button("Show Movies")

    # ... [Previous code remains the same]

    if show_results:
        if selected_genre == 'All':
            # Display the most popular movies overall
            st.header(f"Popular Movies in All Genres")
            popular_movies_all = movies.dropna(subset=['genres']).sort_values(by='popularity', ascending=False).head(5)
        else:
            # Display the most popular movies in the selected genre
            st.header(f"Popular Movies in {selected_genre}")
            genre_filter = movies['genres'].fillna('').str.contains(selected_genre)
            popular_movies_all = movies[genre_filter].sort_values(by='popularity', ascending=False).head(5)

        cols=st.columns(5)

        for i, col in enumerate(cols):

            if i < len(popular_movies_all):

                movie = popular_movies_all.iloc[i]  # Access the row of the DataFrame

                movie_name = movie['title']
                movie_poster = fetch_poster(movie['title'])
                popularity = movie['popularity']
                # movie_trailer = fetch_trailer(movie['id'])


                with col:    
                    st.markdown(f"**{movie_name}**")
                    st.image(movie_poster, use_column_width=True)
                    st.markdown(f"**Popularity:** {popularity:.2f}")
                    # st.markdown(f"**Similarity-score:** {movie_similarity:.5f}")
                    # st.video(movie_trailer)

                    with st.expander(f"Movie Description"):
                        st.markdown("**Tagline:** "+f"{movie['tagline']}")
                        st.markdown("**Genres:** "+f"{movie['genres']}")
                        st.markdown("**Overview:** "+f"{movie['overview']}")
                        st.markdown("**Cast:** "+f"{movie['cast']}")
                        st.markdown("**Director:** "+f"{movie['director']}")
        
