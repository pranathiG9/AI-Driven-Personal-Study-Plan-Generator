import streamlit as st
from streamlit_option_menu import option_menu
from database import fetch_user, add_study_plan, get_study_plans, update_study_plan, delete_study_plan
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from textblob import TextBlob
from googleapiclient.discovery import build
import googleapiclient.discovery
import os
import numpy as np
from datetime import datetime, date
from datetime import datetime, timedelta
import requests
YOUTUBE_API_KEY = "AIzaSyDYEeSTrT7pPpVzpmaJ491gxogVxfWwpvM"

def fetch_youtube_videos(query, max_results=12):
    url = f"https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'key': YOUTUBE_API_KEY,
        'maxResults': max_results
    }
    response = requests.get(url, params=params)
    videos = []
    if response.status_code == 200:
        data = response.json()
        for item in data['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            videos.append({'video_id': video_id, 'title': video_title})
    return videos

# Load the pre-trained models and data
tfidf_vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))
data = pd.read_csv("coursera.csv")  # Replace with the path to your data file
data['tags'] = data['Course Name'] + " " + data['Difficulty Level'] + " " + data['Course Description'] + " " + data['Skills']

# Precompute vectors for all tags
vectors = tfidf_vectorizer.transform(data['tags'])

def recommend(course_name, df, tfidf_vectorizer, top_n=1):
    course_vector = tfidf_vectorizer.transform([course_name])
    similarity_scores = cosine_similarity(course_vector, vectors)[0]

    similar_courses = [(index, score) for index, score in enumerate(similarity_scores)]
    similar_courses_sorted = sorted(similar_courses, key=lambda x: x[1], reverse=True)

    recommendations = []
    for i in similar_courses_sorted[:top_n]:
        recommendations.append((df.iloc[i[0]]['Course Name'], df.iloc[i[0]]['Skills']))

    return recommendations


def navigate_to_page(page_name):
    st.session_state["current_page"] = page_name
    st.experimental_rerun()
def user_home_page():
    
    user = fetch_user(st.session_state["current_user"])
    with st.sidebar:
        st.markdown(f"<h1 style='text-align: center;'>Welcome, {user[1]}!</h1>", unsafe_allow_html=True)

        # Centered image
        st.markdown(
            f"<div style='text-align: center;'><img src='https://cdni.iconscout.com/illustration/premium/thumb/boy-saying-hi-illustration-download-in-svg-png-gif-file-formats--hello-logo-man-waiving-hand-waving-people-say-pack-illustrations-4438343.png?f=webp' width=200></div>",
            unsafe_allow_html=True
        )

        select = option_menu(
            None,
            ["View Study Plan", "Update Study Plan", "Recommend Plan", "Courses", "Delete Plan","Logout"],
            icons=["eye-fill", "pencil-fill", "lightbulb-fill", "book-fill", "trash-fill", "house-lock-fill"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5px"},
                "icon": {"font-size": "18px"},
                "nav-link": {"font-size": "16px"},
                "nav-link-selected": {"background-color": "#11809e"},
            },
        )

    if select == "View Study Plan":
        st.title("Your Study Plans")
        
        plans = get_study_plans(user[0])
        if plans:
            st.markdown(
                """
                <style>
                /* Apply background image to the main content area */
                .main {
                    background-image: url("https://img.freepik.com/free-photo/fitness-concept-with-dumbbells-frame_23-2148531434.jpg");  
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    background-color: rgba(255, 255, 255, 0.5);
                    background-blend-mode: overlay;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            for plan in plans:
                try:
                    # Extract and parse the start date
                    start_date_str = plan['start_date'].split(" ")[0]  # Extract only the date part
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

                    # Calculate end date
                    weeks_duration = plan['days']  # Assuming 'days' represents the number of weeks
                    end_date = start_date + timedelta(weeks=weeks_duration)

                    # Extract course details
                    course_name = plan['course_name']
                    skills = plan['skills']

                    # Add an outline box for the entire plan
                    st.markdown(
                        f"""
                        <div style="
                            border: 2px solid #4CAF50; 
                            border-radius: 10px; 
                            padding: 15px; 
                            margin-bottom: 20px; 
                            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                            background-color: #f9f9f9;">
                            <h4 style='color:#007BFF; font-weight:bold;'>📌 Course: {course_name}</h4>
                            <p><strong>Start Date:</strong> {start_date.strftime('%Y-%m-%d')}</p>
                            <p><strong>End Date:</strong> {end_date.strftime('%Y-%m-%d')}</p>
                        """, 
                        unsafe_allow_html=True
                    )

                    # Process skills and map them week-wise
                    if "," in skills:
                        skill_list = skills.split(",")
                        num_skills = len(skill_list)

                        if num_skills == weeks_duration:
                            for i in range(num_skills):
                                week_start = start_date + timedelta(weeks=i)
                                week_end = week_start + timedelta(days=6)
                            cols = st.columns(2)
                            for k in range(num_skills):
                                week_start = start_date + timedelta(weeks=k)
                                week_end = week_start + timedelta(days=6)
                                if k == weeks_duration:
                                    break
                                cols[k % 2].markdown(
                                    f'<p><span style="color:green; font-weight:bold;">Week {k+1} ({week_start.strftime("%Y-%m-%d")} - {week_end.strftime("%Y-%m-%d")}):</span> '
                                    f'<span style="color:black;">{skill_list[k].strip().upper()}</span></p>',
                                    unsafe_allow_html=True
                                )
                        elif num_skills > weeks_duration:
                            for i in range(weeks_duration):
                                week_start = start_date + timedelta(weeks=i)
                                week_end = week_start + timedelta(days=6)

                            cols = st.columns(2)
                            for k in range(weeks_duration):
                                week_start = start_date + timedelta(weeks=k)
                                week_end = week_start + timedelta(days=6)
                                cols[k % 2].markdown(
                                    f'<p><span style="color:green; font-weight:bold;">Week {k+1} ({week_start.strftime("%Y-%m-%d")} - {week_end.strftime("%Y-%m-%d")}):</span> '
                                    f'<span style="color:black;">{skill_list[k].strip().upper()}</span></p>',
                                    unsafe_allow_html=True
                                )
                            remaining_skills = ', '.join(skill_list[weeks_duration:])
                            st.markdown(
                                f'<p><span style="color:blue; font-weight:bold;">Additional Skills:</span> '
                                f'<span style="color:black;">{remaining_skills.upper()}</span></p>',
                                unsafe_allow_html=True
                            )
                        else:
                            for i in range(num_skills):
                                week_start = start_date + timedelta(weeks=i)
                                week_end = week_start + timedelta(days=6)

                            cols = st.columns(2)
                            for k in range(num_skills):
                                week_start = start_date + timedelta(weeks=k)
                                week_end = week_start + timedelta(days=6)
                                cols[k % 2].markdown(
                                    f'<p><span style="color:green; font-weight:bold;">Week {k+1} ({week_start.strftime("%Y-%m-%d")} - {week_end.strftime("%Y-%m-%d")}):</span> '
                                    f'<span style="color:black;">{skill_list[k].strip().upper()}</span></p>',
                                    unsafe_allow_html=True
                                )

                            st.markdown(
                                f'<p><span style="color:blue; font-weight:bold;">Additional Weeks:</span> '
                                f'<span style="color:black;">Practice more technical skills and enhance your learning with projects.</span></p>',
                                unsafe_allow_html=True
                            )
                    else:
                        st.markdown(f"<p><strong>Skills:</strong> {skills}</p>", unsafe_allow_html=True)

                    # Close the box after everything
                    st.markdown("</div>", unsafe_allow_html=True)

                    # Store study plan (function to save the plan can be implemented)
                    # add_study_plan(user[0], course_name, datetime.now(), weeks_duration, skills)

                except Exception as e:
                    st.markdown(f"<p style='color:red;'>Error processing plan: {e}</p>", unsafe_allow_html=True)


        else:
            st.image("https://assets.medfin.in/static/assets-v3/common/images/no-data-found.svg")

    elif select == "Update Study Plan":
        st.title("Update Study Plan")
        plans = get_study_plans(user[0])
        if plans:
            st.markdown(
                """
                <style>
                /* Apply background image to the main content area */
                .main {
                    background-image: url("https://www.discoverengineering.org/wp-content/uploads/2023/12/mj_11416_3.jpg");  
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    background-color: rgba(255, 255, 255, 0.6);
                    background-blend-mode: overlay;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            plan_options = [f"{plan['course_name']} ({plan['id']})" for plan in plans]
            selected_plan = st.selectbox("Select a plan to update", plan_options)

            if selected_plan:
                plan_id = int(selected_plan.split(" (")[1][:-1])
                selected_plan_data = next(p for p in plans if p['id'] == plan_id)

                new_course_name = st.text_input("Course Name", value=selected_plan_data['course_name'])
                start_date = datetime.strptime(selected_plan_data['start_date'].split(" ")[0], "%Y-%m-%d").date()

                # Ensure default value is not in the past
                default_date = max(start_date, date.today())
                
                new_start_date = st.date_input(
                    "Start Date",
                    value=default_date,  # Ensures default is not in the past
                    min_value=date.today()  # Blocks past dates
                )

                new_days = st.number_input("Duration (days)", value=selected_plan_data['days'], min_value=1)

                if st.button("Update Plan"):
                    update_study_plan(plan_id, new_course_name, new_start_date, new_days)
                    st.success("Plan updated successfully!")
        else:
            st.image('https://img.freepik.com/free-vector/hand-drawn-no-data-concept_52683-127823.jpg')

    elif select == "Recommend Plan":
        st.title("Recommend Study Plan")
        df=pd.read_csv("Coursera.csv")
        st.markdown(
            """
            <style>
            /* Apply background image to the main content area */
            .main {
                background-image: url("https://t4.ftcdn.net/jpg/02/98/89/07/360_F_298890723_gxZy7ljKF1pvZcGTpxxUEKPmVXoF2eCZ.jpg");  
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
        with st.form(key="recommend_form"):
            course_name = st.text_input("Enter the course name:",placeholder="Example: Python for Data Science")
            days= st.slider("Duration (weeks)", 1, 100, 7)
            if st.form_submit_button("Generate Plan",type='primary') and course_name:
                recommendations = recommend(course_name, data, tfidf_vectorizer, top_n=2)
                if recommendations:
                    recommended_course, skills = recommendations[0]  # Unpack the tuple properly
                    df1=pd.read_csv("Skills.csv")
                    #df1 contains area and skills columns and all ares is in lower case check if the recommendation_course is in lower case are in df1 then skills will be the skills of that area otherwise skills will be the skills of the course
                    lis=df1['area'].str.lower().values
                    #make lis as list of lower case areas
                    lis1=list(lis)
                    course=recommended_course.lower()
                    words=course.replace(":", "").split()
                    if any(item in course for item in lis1): 
                        for i in lis1:
                            if i in course:
                                skills=df1[df1['area']==i]['skills'].values[0]
                    st.markdown(f"### Recommended Course: {recommended_course}")
                    try:
                        #if skills contains comma then split the skills and print each skill
                        if "," in skills:
                            lis=skills.split(",")
                            n=int(len(lis))
                            weeks=int(days)
                            if n==weeks:
                                for i in range(n):
                                    st.markdown(
                                        f'<p><span style="color:green; font-weight:bold;">Week {i+1}:</span> '
                                        f'<span style="color:black;">{lis[i].upper()}</span></p>',
                                        unsafe_allow_html=True
                                    )
                            elif n>weeks:
                                for i in range(weeks):
                                    st.markdown(
                                        f'<p><span style="color:green; font-weight:bold;">Week {i+1}:</span> '
                                        f'<span style="color:black;">{lis[i].upper()}</span></p>',
                                        unsafe_allow_html=True
                                    )
                                    #display like additonal skills
                                rest_skills=', '.join(lis[weeks:])
                                st.markdown(
                                    f'<p><span style="color:blue; font-weight:bold;">Additional Skills:</span> ' 
                                    f'<span style="color:black;">{rest_skills.upper()}</span></p>',
                                    unsafe_allow_html=True
                                )       
                            else:
                                for i in range(n):
                                    st.markdown(
                                        f'<p><span style="color:green; font-weight:bold;">Week {i+1}:</span> '
                                        f'<span style="color:black;">{lis[i].upper()}</span></p>',
                                        unsafe_allow_html=True
                                    )
                                #display like additinal weeks with text like practice more some content in 2 sentences
                                st.markdown(
                                    f'<p><span style="color:blue; font-weight:bold;">Additional Weeks:</span> ' 
                                    f'<span style="color:black;">Practice more technical skills and some content</span></p>',
                                    unsafe_allow_html=True
                                )
                        else:
                            st.markdown(f"**Skills:** {skills}")
                        add_study_plan(user[0], recommended_course, datetime.now(), days, skills)
                    except:
                        pass
    elif select == "Courses":
        st.title("Courses Recommended for You")
        plans= get_study_plans(user[0])
        if plans:
            st.markdown(
                """
                <style>
                /* Apply background image to the main content area */
                .main {
                    background-image: url("https://img.freepik.com/premium-photo/success-idea-concept_670147-47682.jpg");  
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
            try:
                plan_options = [f"{plan['course_name']} ({plan['id']})" for plan in plans]
                selected_plan = st.selectbox("Select a plan to view courses", plan_options)
                
                if selected_plan:
                    id = selected_plan.split(" (")[0]
                    st.markdown(f"<h2 style='text-align: center; color:blue;'>{id}</h2>", unsafe_allow_html=True)
                    start_time = datetime(year=2020, month=1, day=1).strftime('%Y-%m-%dT%H:%M:%SZ')
                    end_time = datetime(year=2025, month=1, day=28).strftime('%Y-%m-%dT%H:%M:%SZ')
                    def rankFinder(comment):
                        list_1 = []
                        for ele in comment:
                            t=TextBlob(ele)
                            list_1.append(t.sentiment.polarity)
                            if len(list_1)>0:
                                return abs(sum(list_1)/len(list_1))
                            else:
                                pass
                    s=[]
                    ids=[]
                    ind=[]
                    api_key="AIzaSyApIE8uHcg1wcDZZNCPEY4qWSwxRifBQ8w"
                    youtube=build('youtube','v3',developerKey=api_key)
                    results = youtube.search().list(q=id, part="snippet", type="video", order="viewCount",publishedAfter=start_time,
                                                publishedBefore=end_time, maxResults=20).execute()
                    for item in sorted(results['items'], key=lambda x:x['snippet']['publishedAt']):
                        coll = item['snippet']['title'], item['id']['videoId']
                        df_1 = pd.DataFrame(coll)
                        for i in range(len(df_1)):
                            s.append(df_1.iloc[i,0])
                    for j in range(0,len(s),2):
                        ind.append(s[j])
                    for i in range(1,len(s),2):
                        ids.append(s[i])
                    for it in range(0,len(ids)):
                        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
                        api_service_name = "youtube"
                        api_version = "v3"
                        youtube = googleapiclient.discovery.build(
                        api_service_name, api_version, developerKey = api_key)
                        request = youtube.commentThreads().list(
                            part="id,snippet",
                            maxResults=100,
                            order="relevance",
                            videoId= ids[it]
                        )
                        response = request.execute()
                        authorname = []
                        comments = []
                        positive = []
                        negative = []
                        for i in range(len(response["items"])):
                            authorname.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"])
                            comments.append(response["items"][i]["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
                            df_1 = pd.DataFrame(comments, index = authorname,columns=["Comments"])
                        for i in range(len(df_1)):
                            text =  TextBlob(df_1.iloc[i,0])
                            polarity = text.sentiment.polarity
                            if polarity>0:
                                positive.append(df_1.iloc[i,0])
                            elif polarity<0:
                                negative.append(df_1.iloc[i,0])
                            else:
                                pass
                        inh="https://www.youtube.com/watch?v="
                        inh+=ids[it]
                        if len(negative)==0:
                            rank_1 = rankFinder(positive)
                            inten_1=rank_1*len(positive)
                            neg_int=0
                            pos_int= 1/(1 + np.exp(-inten_1))
                            if pos_int>=0.95:
                                st.markdown(f"<h3 style='color: green;'>{ind[it]}</h3>", unsafe_allow_html=True)
                                st.write(inh)
                                st.write("⭐⭐⭐⭐⭐")
                                st.video(str(inh))
                            if pos_int>0.75 and pos_int<0.95:
                                st.markdown(f"<h3 style='color: green;'>{ind[it]}</h3>", unsafe_allow_html=True)
                                st.write(inh)
                                st.write("⭐⭐⭐⭐✰")
                                st.video(str(inh))
                            if pos_int>0.50 and pos_int<0.75:
                                st.markdown(f"<h3 style='color: orange;'>{ind[it]}</h3>", unsafe_allow_html=True)
                                st.write(inh)
                                st.write("⭐⭐⭐✰✰")
                                st.video(str(inh))
                            if pos_int>0.30 and pos_int<0.50:
                                st.markdown(f"<h3 style='color: red;'>{ind[it]}</h3>", unsafe_allow_html=True)
                                st.write(inh)
                                st.write("⭐⭐✰✰✰")
                                st.video(str(inh))
                            if pos_int<0.30:
                                st.markdown(f"<h3 style='color: red;'>{ind[it]}</h3>", unsafe_allow_html=True)
                                st.write(inh)
                                st.write("⭐✰✰✰✰")
                                st.video(str(inh))
                        if len(negative)>0:
                            rank_1 = rankFinder(positive)
                            inten_1=rank_1*len(positive)
                            rank_2=rankFinder(negative)
                            inten_2=rank_2*len(negative)
                            pos_int=inten_1/(inten_1+inten_2)
                            neg_int=inten_2/(inten_1+inten_2)
                            if pos_int>=0.95:
                                st.markdown(f"<h3 style='color: green;'>{ind[it]}</h3>", unsafe_allow_html=True)
                                st.write(inh)
                                st.write("⭐⭐⭐⭐⭐")
                                st.video(str(inh))
                            if pos_int>0.75 and pos_int<0.95:
                                st.markdown(f"<h3 style='color: green;'>{ind[it]}</h3>", unsafe_allow_html=True)
                                st.write(inh)
                                st.write("⭐⭐⭐⭐✰")
                                st.video(str(inh))
                            if pos_int>0.50 and pos_int<0.75:
                                st.markdown(f"<h3 style='color: orange;'>{ind[it]}</h3>", unsafe_allow_html=True)
                                st.write(inh)
                                st.write("⭐⭐⭐✰✰")
                                st.video(str(inh))
                            if pos_int>0.30 and pos_int<0.50:
                                st.markdown(f"<h3 style='color: red;'>{ind[it]}</h3>", unsafe_allow_html=True)
                                st.write(inh)
                                st.write("⭐⭐✰✰✰")
                                st.video(str(inh))
                            if pos_int<0.30:
                                st.markdown(f"<h3 style='color: red;'>{ind[it]}</h3>", unsafe_allow_html=True)
                                st.write(inh)
                                st.write("⭐✰✰✰✰")
                                st.video(str(inh))
                        st.markdown(f"<hr/>",unsafe_allow_html=True)
            except:
                pass
        else:
            st.write("")
            st.write("")
            st.image('https://www.qlivelearn.in/_nuxt/img/courses-background.c16c3ca.svg',use_column_width=True)
    elif select == "Delete Plan":
        st.title("Delete Study Plans")
        
        plans= get_study_plans(user[0])
        if plans:
            st.markdown(
                """
                <style>
                /* Apply background image to the main content area */
                .main {
                    background-image: url("https://t4.ftcdn.net/jpg/04/26/37/35/360_F_426373558_cZSZYCVZ4C4m1r8EpYFd7EJHoY1UsRhL.jpg");  
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    background-color: rgba(255, 255, 255, 0);
                    background-blend-mode: overlay;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            plan_options = [f"{plan['course_name']} ({plan['id']})" for plan in plans]
            selected_plan = st.selectbox("Select a plan to delete", plan_options)

            if selected_plan:
                plan_id = int(selected_plan.split(" (")[1][:-1])
                selected_plan_data = next(p for p in plans if p['id'] == plan_id)

                if st.button("Delete Plan"):
                    delete_study_plan(plan_id)
                    st.success("Plan deleted successfully!")
        else:
            st.image("https://img.freepik.com/free-vector/hand-drawn-no-data-concept_52683-127818.jpg",use_column_width=True)
    elif select == "Logout":
        st.session_state["logged_in"] = False
        st.session_state["current_user"] = None
        navigate_to_page("home")
