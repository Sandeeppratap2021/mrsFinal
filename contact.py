import streamlit as st

def app():
    # st.write('contact')
    # st.markdown("<h1 style= 'text-align: center;'>User Registration</h1>", unsafe_allow_html=True)
    # with st.form("Form 1",clear_on_submit=True):
    #     col1, col2 = st.columns(2)
    #     f_name= col1.text_input("First Name")
    #     l_name= col2.text_input("Last Name")
    #     s_email= st.text_input("Email Address")
    #     s_password= st.text_input("Password")
    #     s_cpassword= st.text_input("Confirm Password")
    #     s_state= st.form_submit_button("Submit")

    #     if s_state:
    #         if f_name == "" and l_name == "" and s_email == "" and s_password == "" and s_cpassword =="" :
    #             st.warning("Please fill the above fields")
    #         else:
    #             st.success("Submitted Successfully")
    st.header(":mailbox: Get in touch with us!!")

    contact_form = """
    <form action="https://formsubmit.co/suryamrs2024@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your Name" required>
        <input type="email" name="email" placeholder="Your Email" required>
        <textarea name="message" placeholder="Your message here..."></textarea>
        <button type="submit">Send</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)

    # use local CSS file
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("style/style.css")
