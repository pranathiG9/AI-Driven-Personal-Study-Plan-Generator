import streamlit as st
from database import add_user
import re
def navigate_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.experimental_rerun()
def validate_mail(mail):
    valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', mail)
    return True
def signup_page():
    st.markdown(
    """
    <style>
    /* Apply background image to the main content area */
    .main {
        background-image: url("https://miro.medium.com/v2/resize:fit:736/0*zPdYe2yXP-vCHc7D.jpeg");  
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-color: rgba(255, 255, 255, 0.7);
        background-blend-mode: overlay;

    }
    </style>
    """,
    unsafe_allow_html=True
    )
    with st.form(key="signup_form"):
        col1,col2=st.columns([10,1])
        if col2.form_submit_button("🏠"):
            navigate_to_page("home")
        st.markdown(
            """
            <div style="text-align: center; color: red;">
                <h1 style="font-size: 50px; color:blue;">Sign Up Here !!</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
        col1,col2=st.columns([1,1])
        name=col1.text_input("Name")
        email = col2.text_input("Email", key="signup_email")
        age = col1.slider("Age", 1, 100, 18)
        role = col2.selectbox("Role", ["Student", "Teacher", "Parent"])
        col1,col2=st.columns([1,1])
        password = col1.text_input("Create a Password", type="password", key="signup_password")
        retyped_password = col2.text_input("Retype Password", type="password", key="signup_retyped_password")
        col1,col2,col3 = st.columns([1,1,1])
        with col1:
            if st.form_submit_button("Sign Up🔒",type='primary') and validate_mail(email)!=None and len(password)>=6 and password==retyped_password and age and role:
                try:
                    add_user(name,email,age,role,password)
                    st.success("Account created successfully!!")
                    navigate_to_page("login")
                except Exception as e:
                    st.error('Already have an account with this email address. Please login.')
            elif validate_mail(email)==None:
                st.error("Invalid email address. Please enter a valid email address.")
            elif password!=retyped_password:
                st.error("Passwords do not match.")
            elif len(password)<6 and len(password)!=0:
                st.error("Password must be at least 8 characters long.")
        with col3:
            if st.form_submit_button("Already have an account🙋🏻‍♂️",type='primary'):
                navigate_to_page("login")