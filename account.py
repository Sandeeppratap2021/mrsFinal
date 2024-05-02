# import streamlit as st
# import pandas as pd
# import pickle
# import requests
# from pathlib import Path
# import streamlit_authenticator as stauth  # pip install streamlit-authenticator
# from fuzzywuzzy import process

# def app():
#     # st.write('account')
#     # --- USER AUTHENTICATION ---
#     names = ["Sandeep Pratap", "Pratyaya Prakash", "Govind Pandey", "Abhinav Kumar"]
#     usernames = ["sandeep007", "pratyaya057", "govind047", "abhinav008"]

#     # load hashed passwords
#     file_path = Path(__file__).parent / "hashed_pw.pkl"
#     with file_path.open("rb") as file:
#         hashed_passwords = pickle.load(file)

#     authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
#         "movies_dashboard", "abcdef", cookie_expiry_days=30)

#     name, authentication_status, username = authenticator.login("Login", "main") # main body or side-bar

#     if authentication_status == False:
#         st.error("Username/password is incorrect")

#     if authentication_status == None:
#         st.warning("Please enter your username and password")

#     if authentication_status:
#         # logout
#         # authenticator.logout("Logout", "sidebar")
#         # st.sidebar.title(f"Welcome {name}")
#         authenticator.logout("Logout", "main")
#         st.title(f"Welcome {name}")
#         st.subheader(f"username {username}")

import streamlit as st
import pickle
from pathlib import Path
import streamlit_authenticator as stauth

def register(users):
    new_name = st.text_input("Enter your full name:")
    new_username = st.text_input("Enter your desired username:")
    new_password = st.text_input("Enter your password:", type="password")

    if st.button("Register"):
        # Check if the username is unique
        if new_username in users:
            st.error("Username already exists. Please choose a different username.")
        else:
            # Update user information
            users[new_username] = {'name': new_name, 'password': new_password}

            # Save the updated information to the file
            file_path = Path(__file__).parent / "user_data.pkl"
            with file_path.open("wb") as file:
                pickle.dump(users, file)

            st.success("Registration successful! You can now log in.")

def login(users):
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        # Check if the username exists and the password is correct
        if username in users and users[username]['password'] == password:
            st.success(f"Welcome {users[username]['name']}! Login successful.")
            # authenticator.logout("Logout", "main")
            # st.title(f"Welcome {name}")
            # st.subheader(f"username {username}")
        else:
            st.error("Username/password is incorrect")

def app():
    # Load or initialize user data
    file_path = Path(__file__).parent / "user_data.pkl"
    if file_path.exists():
        with file_path.open("rb") as file:
            users = pickle.load(file)
    else:
        users = {}

    action = st.selectbox("Select Action", ["Login", "Register"])

    if action == "Login":
        login(users)
    elif action == "Register":
        register(users)

# import streamlit as st
# import pickle
# from pathlib import Path
# import streamlit_authenticator as stauth
# from fuzzywuzzy import process

# # Initialize session state
# if 'logout_clicked' not in st.session_state:
#     st.session_state.logout_clicked = False


# def register(users):
#     new_name = st.text_input("Enter your full name:")
#     new_username = st.text_input("Enter your desired username:")
#     new_password = st.text_input("Enter your password:", type="password")

#     if st.button("Register"):
#         # Check if the username is unique
#         existing_usernames = [user['username'] for user in users]
#         if new_username in existing_usernames:
#             st.error("Username already exists. Please choose a different username.")
#         else:
#             # Update user information
#             user_data = {'name': new_name, 'username': new_username, 'password': new_password}
#             users.append(user_data)

#             # Save the updated information to the file
#             file_path = Path(__file__).parent / "user_data.pkl"
#             with file_path.open("wb") as file:
#                 pickle.dump(users, file)

#             st.success("Registration successful! You can now log in.")

# def login(users):
#     username = st.text_input("Username:")
#     password = st.text_input("Password:", type="password")

#     if st.button("Login"):
#         # Check if the username exists and the password is correct
#         matching_users = [user for user in users if user['username'] == username]
#         if matching_users:
#             user = matching_users[0]
#             if user['password'] == password:
#                 st.success(f"Welcome {user['name']}! Login successful.")
#                 return user
#                 # display_after_login(user)
#         st.error("Username/password is incorrect")
#         return None
#         # --- USER AUTHENTICATION ---
#         # names = [user['name'] for user in users]
#         # usernames = [user['username'] for user in users]
#         # passwords = [user['password'] for user in users]

#         # print(f"Names: {names}")
#         # print(f"Usernames: {usernames}")
#         # print(f"Passwords: {passwords}")

#         # authenticator = stauth.Authenticate(names, usernames, passwords, "movies_dashboard", "abcdef", cookie_expiry_days=30)
#         # name, authentication_status, username = authenticator.login("Login", "main")  # main body or side-bar
#         # print(f"Name: {name}, Authentication Status: {authentication_status}, Username: {username}")
#         # if authentication_status == False:
#         #     st.error("Username/password is incorrect")

#         # if authentication_status == None:
#         #     st.warning("Please enter your username and password")

#         # if authentication_status:
#         #     st.button("Logout", on_click=logout)
#         #     st.title(f"Welcome {name}")
#         #     st.subheader(f"username {username}")

# def display_after_login(user):
#     # Clear the login UI
#     st.empty()

#     # Display the welcome message and additional information
#     st.button("Logout", on_click=logout)
#     st.title(f"Welcome {user['name']}")
#     st.subheader(f"Username: {user['username']}")
#     # Stop script execution
#     # st.stop()
#     # return True
#     # Infinite loop to keep the information displayed until logout
#     while True:
#         # Sleep for a short duration to avoid high CPU usage
#         # time.sleep(0.1)
#         # Check if the logout button is clicked
#         if st.session_state.logout_clicked:
#             # If clicked, break out of the loop and execute logout
#             logout()
#             break
        
# def logout():

#     st.empty()
#     st.title("Logged out")
#     st.subheader("You have been successfully logged out.")
#     # return False
#     st.session_state.logout_clicked = False
#     # st.empty()
#     # login(users)

# def display_user_list(users):
#     st.header("List of Users (Admin View)")
#     for user in users:
#         st.write(f"Name: {user['name']}, Username: {user['username']}, Password: {user['password']}")

# def app():
#     # Load or initialize user data
#     file_path = Path(__file__).parent / "user_data.pkl"
#     if file_path.exists():
#         with file_path.open("rb") as file:
#             users = pickle.load(file)
#     else:
#         users = []

#     # --- USER AUTHENTICATION ---
#     # # --- USER AUTHENTICATION ---
#     # names = [user['name'] for user in users]
#     # usernames = [user['username'] for user in users]
#     # passwords = [user['password'] for user in users]

#     action = st.selectbox("Select Action", ["Login", "Register"])

#     # if action == "Login":
#     #     login(users)
#     # elif action == "Register":
#     #     register(users)

#     if action == "Login":
#         user = login(users)
#         if user:
#             display_after_login(user)
#             # user_logged_in = display_after_login(user)
#             # if user_logged_in:
#             #     st.stop()
#     elif action == "Register":
#         register(users)
#     elif action == "Logout":
#         logout()

#     # # If the user is logged in, stop the script execution
#     # if user_logged_in:
#     #     st.stop()

#     # authenticator = stauth.Authenticate(names, usernames, passwords, "movies_dashboard", "abcdef", cookie_expiry_days=30)
#     # name, authentication_status, username = authenticator.login("Login/Register", "main")  # main body or side-bar

#     # if authentication_status == False:
#     #     st.error("Username/password is incorrect")

#     # if authentication_status == None:
#     #     st.warning("Please enter your username and password")

#     # if authentication_status:
#     #     st.button("Logout", on_click=logout)
#     #     st.title(f"Welcome {name}")
#     #     st.subheader(f"username {username}")
    

#         # # Both Login and Register options are available to all users
#         # action = st.selectbox("Select Action", ["Login", "Register"])

#         # if action == "Login":
#         #     login(users)
#         # elif action == "Register":
#         #     register(users)

#     # if username == 'admin':  # Check if the user is the admin
#     #     # Additional feature: Registration for admin
#     #     # st.sidebar.header("Admin Registration")
#     #     # register(users)
#     #     action = st.selectbox("Select Action", ["Login", "Register"])

#     #     if action == "Login":
#     #         login(users)
#     #     elif action == "Register":
#     #         register(users)

#     #     # Display user list only for the admin
#     #     display_user_list(users)



