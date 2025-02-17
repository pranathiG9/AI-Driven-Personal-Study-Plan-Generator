<h3>Abstract</h3>
<p>Abstract— The rapid growth of online learning platforms has created a powerful amount of educational content making it challenging for learners to identify the most relevant courses<br>
and resources tailored to their individual learning goals. Conventional recommendation systems frequently lack customization and are unable to dynamically adjust to the feedback,
preferences and progress of a learner. Furthermore, even though courses offer structured learning they frequently lack an integrated system for monitoring skill improvement and improving suggestions based on personal contact.
Additionally, even while videos are essential for learning their efficiency and quality are frequently unknown making students uncertain of which material will help them the most.
In order to overcome these obstacles our AI-powered personalized study plan creator uses Coursera's dataset and processes course descriptions using natural language processing (NLP) 
techniques including Count Vectorizer, TF-IDF, lemmatization and stop word removal.<br> It determines which courses are most appropriate for a given input by using cosine similarity.
A Q-learning algorithm has been added to improve tailoring. Feedback-based learning is carried out using a Q-table with relevance scores, enabling the system to dynamically improve recommendations.
In order to retrieve suggested shows that relate to the advised courses the model also incorporates the YouTube API. <br>Sentiment analysis is performed on the retrieved remarks using a lexicon-based model
to rate each video with positive and negative sentiments in order to evaluate the quality and applicability of these videos. This guarantees that students receive excellent components 
in addition to course recommendations.<br> Streamlit is used to install the system, which enables users to create a structured study schedule by entering their study preferences
including subjects that interest them and the number of weeks available.</p>
