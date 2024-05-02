import streamlit as st
import pandas as pd
import pickle
import requests
from fuzzywuzzy import process
from streamlit_modal import Modal

import json
from streamlit_lottie import st_lottie

# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()
# lottie_hello = load_lottieurl("https://lottie.host/embed/93d1c9c9-931f-45c6-94d0-6d5f3f63f5f4/3V0TBuV3H6.json")

# def load_lottiefile(filepath: str):
#     with open(filepath, "r") as f:
#         return json.load(f)

# lottie_coding = load_lottiefile("lottiefiles/coding.json")

def movie_finder(title, all_titles):
        closest_match = process.extractOne(title, all_titles)
        return closest_match[0]

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

# def voice_to_text():
#     recognizer = sr.Recognizer()

#     st.info("Please speak the name of a movie into the microphone...")

#     with sr.Microphone() as source:
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source, timeout=15)

#     st.success("Recording complete. Transcribing...")

#     try:
#         # Use the Google Web Speech API for transcription
#         text = recognizer.recognize_google(audio)
#         st.success("Transcription successful:")
#         st.write(text)
#         return text
#     except sr.UnknownValueError:
#         st.warning("Could not understand audio.")
#         return None
#     except sr.RequestError as e:
#         st.error(f"Error connecting to Google Web Speech API: {e}")
#         return None


def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    similarity_score=[]
    recommend_poster=[]
    # recommend_trailer=[]
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
        # recommend_trailer.append(fetch_trailer(movies_id))
        recommend_genres.append(movies.iloc[i[0]].genres)
        recommend_tagline.append(movies.iloc[i[0]].tagline)
        recommend_overview.append(movies.iloc[i[0]].overview)
        recommend_cast.append(movies.iloc[i[0]].cast)
        recommend_director.append(movies.iloc[i[0]].director)

    return recommend_movie, similarity_score,  recommend_poster, recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director
    # return recommend_movie, similarity_score,  recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director

# movies = pickle.load(open("movies_list.pkl", 'rb'))
movies = pd.read_pickle("movies_list.pkl")
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list=movies['title'].values

def app():

    st.title("Movie Recommender System")
    # st_lottie(
    #     lottie_coding,
    #     speed=1,
    #     reverse=False,
    #     loop=True,
    #     quality="low",
    #     height=200,
    #     width= 200,
        
    #     key=None,
    # )
    # Search movie option
    user_input = st.text_input("Search for a movie:")
    if user_input:
        corrected_text_movie = movie_finder(user_input, movies_list.tolist())
        st.info(f"Corrected Movie Input: {corrected_text_movie}")

        # Recommendation for the corrected movie
        if st.button("Show Similar Movies"):
            recommend_movie, similarity_score, recommend_poster, recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director = recommend(corrected_text_movie)
            # recommend_movie, similarity_score, recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director = recommend(corrected_movie)

            cols = st.columns(5)
            modal = Modal(key="Demo Key",title="test")
            for i, col in enumerate(cols):
                with col:
                    st.markdown(f"**{recommend_movie[i]}**")
                    st.image(recommend_poster[i], use_column_width=True)
                    st.markdown(f"**Similarity-score:** {similarity_score[i]:.5f}")

                    # Append unique identifier (index i) to the key
                    button_key = f"Button_{i}"
                    open_modal = st.button(label='Movie Description', key=button_key)
                    if open_modal:
                        modal.open()
                        with modal:
                            st.markdown('testtesttesttesttesttesttesttest')
                    # Define a button to trigger the modal
                    # Generate a unique key for the button based on the index
                    # show_modal_button_key = f"Show_Modal_Button_{i}"
                    # show_modal_button = st.button("Movie Description111", key=show_modal_button_key)
                    # # show_modal_button = st.button("Movie Description111")

                    # # Check if the button is clicked
                    # if show_modal_button:
                    #     # Open a modal
                    #     with st.modal():
                    #         # st.write("This is a modal dialog.")
                    #         # Add any content you want to display in the modal
                    # # with st.expander(f"Movie Description"):
                    #         st.markdown("**Tagline:** " + f"{recommend_tagline[i]}")
                    #         st.markdown("**Genres:** " + f"{recommend_genres[i]}")
                    #         st.markdown("**Overview:** " + f"{recommend_overview[i]}")
                    #         st.markdown("**Cast:** " + f"{recommend_cast[i]}")
                    #         st.markdown("**Director:** " + f"{recommend_director[i]}")


    selectvalue=st.selectbox("Select movie from dropdown", movies_list)

    if st.button("Show Recommendation"):
        movie_name, movie_similarity, movie_poster, movie_genres, movie_tagline, movie_overview, movie_cast, movie_director = recommend(selectvalue)
        # movie_name, movie_similarity, movie_genres, movie_tagline, movie_overview, movie_cast, movie_director = recommend(selectvalue)

        cols=st.columns(5)

        for i, col in enumerate(cols):

            with col:    
                st.markdown(f"**{movie_name[i]}**")
                st.image(movie_poster[i], use_column_width=True)
                st.markdown(f"**Similarity-score:** {movie_similarity[i]:.5f}")
                # st.video(movie_trailer[i])

                with st.expander(f"Movie Description"):
                    st.markdown("**Tagline:** "+f"{movie_tagline[i]}")
                    st.markdown("**Genres:** "+f"{movie_genres[i]}")
                    st.markdown("**Overview:** "+f"{movie_overview[i]}")
                    st.markdown("**Cast:** "+f"{movie_cast[i]}")
                    st.markdown("**Director:** "+f"{movie_director[i]}")

        # if st.session_state.search_history and selectvalue not in st.session_state.search_history:
        #     st.session_state.search_history.append(selectvalue)
        # elif not st.session_state.search_history:
        #     st.session_state.search_history.append(selectvalue)

    # # Display search history
    # st.sidebar.title("Search History")
    # for search in st.session_state.search_history[-5:][::-1]:  # Display the last 5 searches in reverse order
    #     st.sidebar.write(search)


    # Create a dictionary where keys are genres and values are lists of movie titles in that genre
    genre_movies = {}

    for index, row in movies.iterrows():
        genres = row['genres']
        if isinstance(genres, str):  # Check if 'genres' is a valid string
            genres = [genre.strip() for genre in genres.split(',')]
            for genre in genres:
                if genre in genre_movies:
                    genre_movies[genre].append(row['title'])
                else:
                    genre_movies[genre] = [row['title']]

    # Select a genre from the list
    selected_genre = st.selectbox("Select a genre", ['All'] + list(genre_movies.keys()))

    # Add a button to show the results
    show_results = st.button("Show Movies")

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
        
    # Create a dictionary where keys are actors and values are lists of movie titles with that actor
    cast_movies = {}

    for index, row in movies.iterrows():
        cast = row['cast']
        
        if isinstance(cast, str):  # Check if 'cast' is a valid string
            cast = [actor.strip() for actor in cast.split(',')]
            for actor in cast:
                cast_movies.setdefault(actor, []).append(row['title'])

    # Select an actor from the list
    selected_actor = st.selectbox("Select an actor", ['All'] + list(cast_movies.keys()))

    # Add a button to show the results
    show_results = st.button("Show Cast Movies")

    if show_results:
        if selected_actor == 'All':
            # Display the most popular movies overall
            st.header(f"Popular Movies with All Actors")
            popular_movies_all = movies.dropna(subset=['cast']).sort_values(by='popularity', ascending=False).head(5)
        else:
            # Display the most popular movies with the selected actor
            st.header(f"Popular Movies with {selected_actor}")
            actor_filter = movies['cast'].fillna('').str.contains(selected_actor)
            popular_movies_all = movies[actor_filter].sort_values(by='popularity', ascending=False).head(5)

        cols = st.columns(5)

        for i, col in enumerate(cols):
            if i < len(popular_movies_all):
                movie = popular_movies_all.iloc[i]  # Access the row of the DataFrame

                movie_name = movie['title']
                movie_poster = fetch_poster(movie['title'])
                popularity = movie['popularity']

                with col:
                    st.markdown(f"**{movie_name}**")
                    st.image(movie_poster, use_column_width=True)
                    st.markdown(f"**Popularity:** {popularity:.2f}")

                    with st.expander(f"Movie Description"):
                        st.markdown("**Tagline:** " + f"{movie['tagline']}")
                        st.markdown("**Genres:** " + f"{movie['genres']}")
                        st.markdown("**Overview:** " + f"{movie['overview']}")
                        st.markdown("**Cast:** " + f"{movie['cast']}")
                        st.markdown("**Director:** " + f"{movie['director']}")


