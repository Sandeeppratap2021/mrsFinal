import streamlit as st
from streamlit_option_menu import option_menu
import home, account, movies, contact, about


def set_bg_hack_url():
    
    st.markdown(
         f"""
         <style>
         [data-testid="stAppViewContainer"]{{
            background: url("https://wallpapergod.com/images/hd/movie-1920X1080-wallpaper-eeotwqkmypkvalg9.jpeg");
            # background: url("https://wallpapergod.com/images/hd/movie-1920X1080-wallpaper-z0puq43u0qbtr6j2.jpeg");

            background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run():
        # with st.sidebar:
        #     app = option_menu(
        #     menu_title="Main Menu",
        #     options=["Home", "Account", "Movies", "Contact", "About Us"],
        #     icons=["house","person", "film","envelope", "globe"],
        #     menu_icon="cast",
        #     default_index=0,
        #     styles={       
        #         "nav-link": {"--hover-color": "pink"},
        #         }
        # )

        set_bg_hack_url() #background-image function

        app = option_menu(
        menu_title=None,
        options=["Home", "Account", "Movies", "Contact", "About Us"],
        icons=["house","person", "film","envelope", "globe"],
        # menu_icon="cast",
        orientation="horizontal",
        default_index=0,
        styles={
            "nav-link": { "--hover-color": "pink"},
            }
        )
        if app =="Home":
            home.app()
        if app =="Account":
            account.app()
        if app =="Movies":
            movies.app()
        if app =="Contact":
            contact.app()
        if app =="About Us":
            about.app()

    run()    
