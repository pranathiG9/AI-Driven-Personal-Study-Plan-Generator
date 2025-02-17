import streamlit as st
from database import authenticate_user
def navigate_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.experimental_rerun()

def login_page():
    # Center the login form using Streamlit form layout
    st.markdown(
    """
    <style>
    /* Apply background image to the main content area */
    .main {
        background-image: url("https://images.pexels.com/photos/207700/pexels-photo-207700.jpeg?cs=srgb&dl=pexels-pixabay-207700.jpg&fm=jpg");  
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-color: rgba(255, 255, 255, 0.4);
        background-blend-mode: overlay;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    with st.form(key="login_form"):
        # Title
        col1,col2=st.columns([10,1])
        if col2.form_submit_button("🏡"):
            navigate_to_page("home")
        st.markdown(
            """
            <div style="text-align: center; color: red;">
                <h1 style="font-size: 50px; color:white;">Login Here !!</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Email and Password inputs
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        # Submit button inside the form
        col1,col2,col3=st.columns([1,2,1])
        with col1:
            if st.form_submit_button("Login",type='primary'):
                if authenticate_user(email, password):
                    st.success(f"Login successful. Welcome {email}!")
                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = email

                    navigate_to_page("user_home")
                else:
                    col2.error("Invalid email or password.")
        with col3:
            if st.form_submit_button("Create Account🤔",type='primary'):
                navigate_to_page("signup")