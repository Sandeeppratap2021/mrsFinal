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
        menu_icon="cast",
        orientation="horizontal",
        default_index=0,
        styles={
            # "nav-link": { "--hover-color": "pink"},
            # "container": {"background-color": "#ffffff", "color": "#ff0000"},
            # "use_padding": False
            "container": {"padding": "0!important", "margin":"0px","background-color": "#fafafa"},
            # "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "pink"},
            # "nav-link-selected": {"background-color": "green"},
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


        footer_container = st.container()

        with footer_container:
            col1, col2, col3 = st.columns((1,1,1))

            with col1:
                st.header("Contact info")

                # css_example ='''
                # <i class="fa-solid fa-envelope"></i> suryamrs2024@gmail.com 
                # <i class="fa-solid fa-phone"></i> +91 73200 XXXXX
                # <i class="fa-solid fa-location-dot"></i> Kolkata, West Bengal
                # '''
                st.markdown("""
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="24" height="24" fill="#ffffff"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M48 64C21.5 64 0 85.5 0 112c0 15.1 7.1 29.3 19.2 38.4L236.8 313.6c11.4 8.5 27 8.5 38.4 0L492.8 150.4c12.1-9.1 19.2-23.3 19.2-38.4c0-26.5-21.5-48-48-48H48zM0 176V384c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V176L294.4 339.2c-22.8 17.1-54 17.1-76.8 0L0 176z"/></svg>
                    suryamrs2024@gmail.com
                </div>
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="24" height="24" fill="#ffffff"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M164.9 24.6c-7.7-18.6-28-28.5-47.4-23.2l-88 24C12.1 30.2 0 46 0 64C0 311.4 200.6 512 448 512c18 0 33.8-12.1 38.6-29.5l24-88c5.3-19.4-4.6-39.7-23.2-47.4l-96-40c-16.3-6.8-35.2-2.1-46.3 11.6L304.7 368C234.3 334.7 177.3 277.7 144 207.3L193.3 167c13.7-11.2 18.4-30 11.6-46.3l-40-96z"/></svg>
                    +91 73200 XXXXX
                </div>
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512" width="24" height="24" fill="#ffffff"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M215.7 499.2C267 435 384 279.4 384 192C384 86 298 0 192 0S0 86 0 192c0 87.4 117 243 168.3 307.2c12.3 15.3 35.1 15.3 47.4 0zM192 128a64 64 0 1 1 0 128 64 64 0 1 1 0-128z"/></svg>
                    Kolkata, West Bengal
                </div>
                """, unsafe_allow_html=True)

            with col2:

                st.header("Policies")
                st.markdown(' <a style="color: #00ff00; text-decoration:none; " href="https://www.google.com" target="_blank"> Privacy Policy </a>', unsafe_allow_html=True)
                st.markdown(' <a style="color: #00ff00; text-decoration:none; " href="https://www.google.com" target="_blank"> Terms and Conditions </a>', unsafe_allow_html=True)

            with col3:

                st.header("Social Media")

                st.markdown("""
                    <style>
                        .icon-link {
                            color: #5c68c0; 
                            text-decoration: none;
                            display: inline-block;
                            margin-right: 10px;
                        }
                        .icon-link svg {
                            width: 24px; /* Set the desired width */
                            height: 24px; /* Set the desired height */
                        }
                    </style>
                    <a class="icon-link" href="https://www.google.com" target="_blank">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512" fill="#ffffff">
                            <path d="M224.1 141c-63.6 0-114.9 51.3-114.9 114.9s51.3 114.9 114.9 114.9S339 319.5 339 255.9 287.7 141 224.1 141zm0 189.6c-41.1 0-74.7-33.5-74.7-74.7s33.5-74.7 74.7-74.7 74.7 33.5 74.7 74.7-33.6 74.7-74.7 74.7zm146.4-194.3c0 14.9-12 26.8-26.8 26.8-14.9 0-26.8-12-26.8-26.8s12-26.8 26.8-26.8 26.8 12 26.8 26.8zm76.1 27.2c-1.7-35.9-9.9-67.7-36.2-93.9-26.2-26.2-58-34.4-93.9-36.2-37-2.1-147.9-2.1-184.9 0-35.8 1.7-67.6 9.9-93.9 36.1s-34.4 58-36.2 93.9c-2.1 37-2.1 147.9 0 184.9 1.7 35.9 9.9 67.7 36.2 93.9s58 34.4 93.9 36.2c37 2.1 147.9 2.1 184.9 0 35.9-1.7 67.7-9.9 93.9-36.2 26.2-26.2 34.4-58 36.2-93.9 2.1-37 2.1-147.8 0-184.8zM398.8 388c-7.8 19.6-22.9 34.7-42.6 42.6-29.5 11.7-99.5 9-132.1 9s-102.7 2.6-132.1-9c-19.6-7.8-34.7-22.9-42.6-42.6-11.7-29.5-9-99.5-9-132.1s-2.6-102.7 9-132.1c7.8-19.6 22.9-34.7 42.6-42.6 29.5-11.7 99.5-9 132.1-9s102.7-2.6 132.1 9c19.6 7.8 34.7 22.9 42.6 42.6 11.7 29.5 9 99.5 9 132.1s2.7 102.7-9 132.1z"/>
                        </svg>
                    </a>
                    <a class="icon-link" href="https://www.google.com" target="_blank">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512" fill="#ffffff"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M549.7 124.1c-6.3-23.7-24.8-42.3-48.3-48.6C458.8 64 288 64 288 64S117.2 64 74.6 75.5c-23.5 6.3-42 24.9-48.3 48.6-11.4 42.9-11.4 132.3-11.4 132.3s0 89.4 11.4 132.3c6.3 23.7 24.8 41.5 48.3 47.8C117.2 448 288 448 288 448s170.8 0 213.4-11.5c23.5-6.3 42-24.2 48.3-47.8 11.4-42.9 11.4-132.3 11.4-132.3s0-89.4-11.4-132.3zm-317.5 213.5V175.2l142.7 81.2-142.7 81.2z"/>
                        </svg>
                    </a>
                    <a class="icon-link" href="https://www.google.com" target="_blank">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 496 512" fill="#ffffff"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M248 8C111 8 0 119 0 256S111 504 248 504 496 393 496 256 385 8 248 8zM363 176.7c-3.7 39.2-19.9 134.4-28.1 178.3-3.5 18.6-10.3 24.8-16.9 25.4-14.4 1.3-25.3-9.5-39.3-18.7-21.8-14.3-34.2-23.2-55.3-37.2-24.5-16.1-8.6-25 5.3-39.5 3.7-3.8 67.1-61.5 68.3-66.7 .2-.7 .3-3.1-1.2-4.4s-3.6-.8-5.1-.5q-3.3 .7-104.6 69.1-14.8 10.2-26.9 9.9c-8.9-.2-25.9-5-38.6-9.1-15.5-5-27.9-7.7-26.8-16.3q.8-6.7 18.5-13.7 108.4-47.2 144.6-62.3c68.9-28.6 83.2-33.6 92.5-33.8 2.1 0 6.6 .5 9.6 2.9a10.5 10.5 0 0 1 3.5 6.7A43.8 43.8 0 0 1 363 176.7z"/>
                        </svg>
                    </a>
                    <a class="icon-link" href="https://www.google.com" target="_blank">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="#ffffff"><!--!Font Awesome Free 6.5.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path d="M512 256C512 114.6 397.4 0 256 0S0 114.6 0 256C0 376 82.7 476.8 194.2 504.5V334.2H141.4V256h52.8V222.3c0-87.1 39.4-127.5 125-127.5c16.2 0 44.2 3.2 55.7 6.4V172c-6-.6-16.5-1-29.6-1c-42 0-58.2 15.9-58.2 57.2V256h83.6l-14.4 78.2H287V510.1C413.8 494.8 512 386.9 512 256h0z"/>
                        </svg>
                    </a>
                    """, unsafe_allow_html=True)




    run()    
