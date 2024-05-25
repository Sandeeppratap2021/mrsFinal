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
#         # # logout
#         # authenticator.logout("Logout", "sidebar")
#         # st.sidebar.title(f"Welcome {name}")
#         authenticator.logout("Logout", "main")
#         st.title(f"Welcome {name}")
#         st.subheader(f"username {username}")
        # try:
        #     if authenticator.reset_password(["username"]):
        #         st.success('Password modified successfully')
        # except Exception as e:
        #     st.error(e)

import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests


cred = credentials.Certificate("movierec-1b79c-3438b911b648.json")
# firebase_admin.initialize_app(cred) #run only one time
def app():
# Usernm = []
    st.title('Welcome to :violet[Movie Recommendation system] :sunglasses:')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''


    def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token
            }
            if username:
                payload["displayName"] = username 
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyC3smmRPv6SFdMMDkTsKdJlgnu-1SoLN7w"}, data=payload)
            try:
                return r.json()['email']
            except:
                st.warning(r.json())
        except Exception as e:
            st.warning(f'Signup failed: {e}')

    def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

        try:
            payload = {
                "returnSecureToken": return_secure_token
            }
            if email:
                payload["email"] = email
            if password:
                payload["password"] = password
            payload = json.dumps(payload)
            print('payload sigin',payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyC3smmRPv6SFdMMDkTsKdJlgnu-1SoLN7w"}, data=payload)
            try:
                data = r.json()
                user_info = {
                    'email': data['email'],
                    'username': data.get('displayName')  # Retrieve username if available
                }
                return user_info
            except:
                st.warning(data)
        except Exception as e:
            st.warning(f'Signin failed: {e}')

    def reset_password(email):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
            payload = {
                "email": email,
                "requestType": "PASSWORD_RESET"
            }
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyC3smmRPv6SFdMMDkTsKdJlgnu-1SoLN7w"}, data=payload)
            if r.status_code == 200:
                return True, "Reset email Sent"
            else:
                # Handle error response
                error_message = r.json().get('error', {}).get('message')
                return False, error_message
        except Exception as e:
            return False, str(e)

    # Example usage
    # email = "example@example.com"
           

    def f(): 
        try:
            # user = auth.get_user_by_email(email)
            # print(user.uid)
            # st.session_state.username = user.uid
            # st.session_state.useremail = user.email

            userinfo = sign_in_with_email_and_password(st.session_state.email_input,st.session_state.password_input)
            st.session_state.username = userinfo['username']
            st.session_state.useremail = userinfo['email']

            
            global Usernm
            Usernm=(userinfo['username'])
            
            st.session_state.signedout = True
            st.session_state.signout = True    
  
            
        except: 
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''


    def forget():
        email = st.text_input('Email')
        if st.button('Send Reset Link'):
            print(email)
            success, message = reset_password(email)
            if success:
                st.success("Password reset email sent successfully.")
            else:
                st.warning(f"Password reset failed: {message}") 
        
    
        
    if "signedout"  not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    
        

        
    
    if  not st.session_state["signedout"]: # only show if the state is False, hence the button has never been clicked
        choice = st.selectbox('Login/Signup',['Login','Sign up'])
        email = st.text_input('Email Address')
        password = st.text_input('Password',type='password')
        st.session_state.email_input = email
        st.session_state.password_input = password

        

        
        if choice == 'Sign up':
            username = st.text_input("Enter  your unique username")
            
            if st.button('Create my account'):
                # user = auth.create_user(email = email, password = password,uid=username)
                user = sign_up_with_email_and_password(email=email,password=password,username=username)
                
                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')
                st.balloons()
        else:
            # st.button('Login', on_click=f)          
            st.button('Login', on_click=f)
            # if st.button('Forget'):
            forget()
            # st.button('Forget',on_click=forget)

            
            
    if st.session_state.signout:
                st.text('Name '+st.session_state.username)
                st.text('Email id: '+st.session_state.useremail)
                st.button('Sign out', on_click=t) 
            
                
    


# import streamlit as st
# import auth_functions

# def app():
#     ## -------------------------------------------------------------------------------------------------
#     ## Not logged in -----------------------------------------------------------------------------------
#     ## -------------------------------------------------------------------------------------------------
#     if 'user_info' not in st.session_state:
#         col1,col2,col3 = st.columns([1,2,1])

#         # Authentication form layout
#         do_you_have_an_account = col2.selectbox(label='Do you have an account?',options=('Yes','No','I forgot my password'))
#         auth_form = col2.form(key='Authentication form',clear_on_submit=False)
#         email = auth_form.text_input(label='Email')
#         password = auth_form.text_input(label='Password',type='password') if do_you_have_an_account in {'Yes','No'} else auth_form.empty()
#         auth_notification = col2.empty()

#         # Sign In
#         if do_you_have_an_account == 'Yes' and auth_form.form_submit_button(label='Sign In',use_container_width=True,type='primary'):
#             with auth_notification, st.spinner('Signing in'):
#                 auth_functions.sign_in(email,password)

#         # Create Account
#         elif do_you_have_an_account == 'No' and auth_form.form_submit_button(label='Create Account',use_container_width=True,type='primary'):
#             with auth_notification, st.spinner('Creating account'):
#                 auth_functions.create_account(email,password)

#         # Password Reset
#         elif do_you_have_an_account == 'I forgot my password' and auth_form.form_submit_button(label='Send Password Reset Email',use_container_width=True,type='primary'):
#             with auth_notification, st.spinner('Sending password reset link'):
#                 auth_functions.reset_password(email)

#         # Authentication success and warning messages
#         if 'auth_success' in st.session_state:
#             auth_notification.success(st.session_state.auth_success)
#             del st.session_state.auth_success
#         elif 'auth_warning' in st.session_state:
#             auth_notification.warning(st.session_state.auth_warning)
#             del st.session_state.auth_warning

#     ## -------------------------------------------------------------------------------------------------
#     ## Logged in --------------------------------------------------------------------------------------
#     ## -------------------------------------------------------------------------------------------------
#     else:
#         # Show user information
#         st.header('User information:')
#         st.write(st.session_state.user_info)

#         # Sign out
#         st.header('Sign out:')
#         st.button(label='Sign Out',on_click=auth_functions.sign_out,type='primary')

#         # Delete Account
#         st.header('Delete account:')
#         password = st.text_input(label='Confirm your password',type='password')
#         st.button(label='Delete Account',on_click=auth_functions.delete_account,args=[password],type='primary')




# import streamlit as st
# import pickle
# from pathlib import Path
# import streamlit_authenticator as stauth

# def register(users):
#     new_name = st.text_input("Enter your full name:")
#     new_username = st.text_input("Enter your desired username:")
#     new_password = st.text_input("Enter your password:", type="password")

#     if st.button("Register"):
#         # Check if the username is unique
#         if new_username in users:
#             st.error("Username already exists. Please choose a different username.")
#         else:
#             # Update user information
#             users[new_username] = {'name': new_name, 'password': new_password}

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
#         if username in users and users[username]['password'] == password:
#             st.success(f"Welcome {users[username]['name']}! Login successful.")
#             authenticator.logout("Logout", "main")
#             st.title(f"Welcome {name}")
#             st.subheader(f"username {username}")
#         else:
#             st.error("Username/password is incorrect")

# def app():
#     # Load or initialize user data
#     file_path = Path(__file__).parent / "user_data.pkl"
#     if file_path.exists():
#         with file_path.open("rb") as file:
#             users = pickle.load(file)
#     else:
#         users = {}

#     action = st.selectbox("Select Action", ["Login", "Register"])

#     if action == "Login":
#         login(users)
#     elif action == "Register":
#         register(users)

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



