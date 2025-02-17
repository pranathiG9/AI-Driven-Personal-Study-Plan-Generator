import streamlit as st

# Navigation function
def navigate_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.experimental_rerun()
def home_page():
    st.markdown(
    """
    <style>
    /* Apply background image to the main content area */
    .main {
        background-image: url("https://t3.ftcdn.net/jpg/07/82/01/84/360_F_782018423_8Y5BkW9uG1zj9vrZRsuai7J1BPcigWOo.jpg");  
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-color: rgba(255, 255, 255, 0.1);
        background-blend-mode: overlay;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    with st.form(key="home_page_form"):
        st.markdown(
            """
            <div style="text-align: center; padding: 1px; background-color: #a632a8; border-radius: 10px; border: 3px solid black;">
                <p style="color: white; font-size: 30px;"><b>AI Driven Personalized Study Plan Generator 👩🏻‍💻</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )
        #add image
        st.markdown(
            """
            <div style="text-align: center;">
                <img src="https://cdni.iconscout.com/illustration/premium/thumb/young-man-working-on-ai-production-illustration-download-in-svg-png-gif-file-formats--mind-artificial-intelligence-brain-automation-pack-machine-learning-illustrations-6423310.png" width="500" height="400">
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3, col4, col5,col6 = st.columns([1, 1, 1, 1, 1.3,1])
        with col2:
            if st.form_submit_button("Login 🔓",type='primary'):
                navigate_to_page("login")
        with col5:
            if st.form_submit_button("Sign Up 🔐",type='primary'):
                navigate_to_page("signup")
