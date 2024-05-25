import streamlit as st
import pandas as pd
import pickle
import requests
from fuzzywuzzy import process
import speech_recognition as sr


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

def fetch_trailer(title):
        # Construct the URL to fetch movie details
        url = f"https://api.apilayer.com/youtube/{title}?api_key=2lmyWj6yj49vBGJ8R4wjczyOl1v6vZGI&append_to_response=videos"
        
        # Make the API request
        response = requests.get(url)
        data = response.json()

        # Check if the 'videos' key is present in the response
        if 'videos' in data and 'results' in data['videos']:
            videos = data['videos']['results']
            
            # Search for a trailer among the videos
            for video in videos:
                # Assuming trailers are of type 'Trailer' and hosted on YouTube
                if video['type'] == 'Trailer' and 'YouTube' in video['site']:
                    # Construct the YouTube trailer URL
                    trailer_key = video['key']
                    trailer_url = f"https://www.youtube.com/watch?v={trailer_key}"
                    return trailer_url

        # Return None if no trailer is found
        return None


def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio_data = recognizer.listen(source)
        st.write("Processing...")
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I did not understand the audio.")
        except sr.RequestError:
            st.error("Sorry, the service is unavailable.")
        return ""


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
        # recommend_trailer.append(fetch_trailer(movies.iloc[i[0]].title))
        recommend_genres.append(movies.iloc[i[0]].genres)
        recommend_tagline.append(movies.iloc[i[0]].tagline)
        recommend_overview.append(movies.iloc[i[0]].overview)
        recommend_cast.append(movies.iloc[i[0]].cast)
        recommend_director.append(movies.iloc[i[0]].director)

    return recommend_movie, similarity_score,  recommend_poster, recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director
    # return recommend_movie, similarity_score,  recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director
    # return recommend_movie, similarity_score,  recommend_poster, recommend_trailer, recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director

# movies = pickle.load(open("movies_list.pkl", 'rb'))
movies = pd.read_pickle("movies_list.pkl")
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list=movies['title'].values

def app():

    st.title("Movie Recommendation System")

    # Search movie option
    st.markdown(
        """
        <style>
            [data-testid="baseButton-secondary"] {
                # color: white;
                background-color: transparent;
                border: solid;
                border-radius: 25px;
                # border-bottom: 1px solid white;
                # outline: none;
                # width: 100%;
            }
            [data-testid="baseButton-secondary"]:hover {
                color: white;
                background-color: #ff0000;
                # border: solid;
                # border-bottom: 1px solid white;
                # outline: none;
                # width: 100%;
            }
            [data-baseweb="select"]{
                # color: red;
                # background-color: transparent;
                # font-size: 55px;
                width: 50%;
            }
            [data-baseweb="input"]{
                # color: red;
                background-color: transparent;
                # font-size: 55px;
                width: 50%;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Display the text input
    user_input = st.text_input("Search for a movie:",placeholder="Enter the movie name")
    
    if user_input or st.button("Search"):
        corrected_text_movie = movie_finder(user_input, movies_list.tolist())
        st.info(f"Corrected Movie Input: {corrected_text_movie}")

        # Recommendation for the corrected movie
        if st.button("Show Similar Movies"):
            recommend_movie, similarity_score, recommend_poster, recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director = recommend(corrected_text_movie)
            # recommend_movie, similarity_score, recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director = recommend(corrected_movie)
            # recommend_movie, similarity_score, recommend_poster, recommend_trailer, recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director = recommend(corrected_text_movie)


            cols = st.columns(5)
            for i, col in enumerate(cols):
                with col:
                    st.markdown(f"**{recommend_movie[i]}**")
                    st.image(recommend_poster[i], use_column_width=True)
                    # st.markdown(f"[Watch Trailer]({recommend_trailer[i]})")
                    st.markdown(f"**Similarity-score:** {similarity_score[i]:.5f}")

                    with st.popover(f"Movie Description"):
                        col1, col2 = st.columns([1, 1.2])  

                        with col1:
                            st.image(recommend_poster[i], use_column_width=False)

                        with col2:
                            st.markdown("**Title:** "+f"{recommend_movie[i]}")
                            st.markdown("**Tagline:** " + f"{recommend_tagline[i]}")
                            st.markdown("**Genres:** " + f"{recommend_genres[i]}")
                            st.markdown("**Overview:** " + f"{recommend_overview[i]}")
                            st.markdown("**Cast:** " + f"{recommend_cast[i]}")
                            st.markdown("**Director:** " + f"{recommend_director[i]}")

    if st.button("Use Voice Input"):
        voice_text = voice_to_text()
        if voice_text:
            st.write(f"You said: {voice_text}")
            corrected_text_movie = movie_finder(voice_text, movies_list.tolist())
            st.info(f"Corrected Movie Input: {corrected_text_movie}")

            recommend_movie, similarity_score, recommend_poster, recommend_genres, recommend_tagline, recommend_overview, recommend_cast, recommend_director = recommend(corrected_text_movie)

            cols = st.columns(5)
            for i, col in enumerate(cols):
                with col:
                    st.markdown(f"**{recommend_movie[i]}**")
                    st.image(recommend_poster[i], use_column_width=True)
                    # st.markdown(f"[Watch Trailer]({recommend_trailer[i]})")
                    st.markdown(f"**Similarity-score:** {similarity_score[i]:.5f}")

                    with st.popover(f"Movie Description"):
                        col1, col2 = st.columns([1, 1.2])
                        with col1:
                            st.image(recommend_poster[i], use_column_width=False)
                        with col2:
                            st.markdown("**Title:** " + f"{recommend_movie[i]}")
                            st.markdown("**Tagline:** " + f"{recommend_tagline[i]}")
                            st.markdown("**Genres:** " + f"{recommend_genres[i]}")
                            st.markdown("**Overview:** " + f"{recommend_overview[i]}")
                            st.markdown("**Cast:** " + f"{recommend_cast[i]}")
                            st.markdown("**Director:** " + f"{recommend_director[i]}")



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

                with st.popover(f"Movie Description"):
                    col1, col2 = st.columns([1, 1.2])  

                    with col1:
                        st.image(movie_poster[i], use_column_width=False)

                    with col2:
                        st.markdown("**Title:** "+f"{movie_name[i]}")
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

                    # with st.popover(f"Movie Description"):
                    #     st.image(movie_poster, use_column_width=False)
                    #     st.markdown("**Title:** "+f"{movie_name}")
                    #     st.markdown("**Tagline:** "+f"{movie['tagline']}")
                    #     st.markdown("**Genres:** "+f"{movie['genres']}")
                    #     st.markdown("**Overview:** "+f"{movie['overview']}")
                    #     st.markdown("**Cast:** "+f"{movie['cast']}")
                    #     st.markdown("**Director:** "+f"{movie['director']}")

                    with st.popover("Movie Description"):
                        col1, col2 = st.columns([1, 1.2])  

                        with col1:
                            st.image(movie_poster, use_column_width=False)

                        with col2:
                            st.markdown("**Title:** " + f"{movie_name}")
                            st.markdown("**Tagline:** " + f"{movie['tagline']}")
                            st.markdown("**Genres:** " + f"{movie['genres']}")
                            st.markdown("**Overview:** " + f"{movie['overview']}")
                            st.markdown("**Cast:** " + f"{movie['cast']}")
                            st.markdown("**Director:** " + f"{movie['director']}")


    # Create a dictionary where keys are actors and values are lists of movie titles with that actor
    cast_movies = {}

    for index, row in movies.iterrows():
        cast = row['cast']
        
        if isinstance(cast, str):  # Check if 'cast' is a valid string
            cast = [actor.strip() for actor in cast.split(',')]
            for actor in cast:
                cast_movies.setdefault(actor, []).append(row['title'])

    # Select an actor from the list
    # Define the HTML string with custom CSS for increasing text size
    selectbox_html = f"""
        <style>
            /* Increase font size of selectbox label */
            .st-bn > div > div > div > div > label > span {{
                font-size: larger !important;
            }}
            /* Increase font size of selectbox options */
            .st-eb > div > div > div > div > div > div > div {{
                font-size: larger !important;
            }}
        </style>
    """

    # Write the HTML to the Streamlit app
    st.write(selectbox_html, unsafe_allow_html=True)
    selected_actor = st.selectbox("Select cast name", ['All'] + list(cast_movies.keys()))

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

                    with st.popover(f"Movie Description"):
                        col1, col2 = st.columns([1, 1.2])  

                        with col1:
                            st.image(movie_poster, use_column_width=False)

                        with col2:
                            st.markdown("**Title:** "+f"{movie_name}")
                            st.markdown("**Tagline:** " + f"{movie['tagline']}")
                            st.markdown("**Genres:** " + f"{movie['genres']}")
                            st.markdown("**Overview:** " + f"{movie['overview']}")
                            st.markdown("**Cast:** " + f"{movie['cast']}")
                            st.markdown("**Director:** " + f"{movie['director']}")


