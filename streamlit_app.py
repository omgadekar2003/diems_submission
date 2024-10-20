
#Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas as pd







# Image URLs
image_url_left = "https://media.licdn.com/dms/image/D4E12AQF-BvR3QRs9gw/article-cover_image-shrink_720_1280/0/1656343174665?e=2147483647&v=beta&t=T3dP2OU7Tbws3Ap79YdaIIYX1st1UqSW1TeKVdH6L48"
image_url_center = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSkM0Emsq4_Gz6ZqhBstMmUDwDeogsSd0zcQQ&s"
image_url_right = "https://www.uptoplay.net/imagescropped/diemsnoticesicon128.jpg.webp"

# Layout using Streamlit columns
col1, col2, col3 = st.columns([1, 2, 1])  # Adjust the proportions of the columns

# Display the left image in the first column with circular styling
with col1:
    st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="{image_url_left}" alt="Left Image" style="width:150px; height:150px; border-radius: 50%;">
    </div>
    """, unsafe_allow_html=True)

# Display the center collab image in the second column
with col2:
    st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="{image_url_center}" alt="Collab Logo" style="width:150px; height:150px; border-radius: 50%;">
    </div>
    """, unsafe_allow_html=True)

    # Attractive heading for B.Tech CA-II Submission
    st.title("🎓 **DIEMS B.Tech CA-II Submission** 🎓")
    st.write("Enhancing Knowledge Through Collaboration")

# Display the right image in the third column with circular styling
with col3:
    st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center;">
        <img src="{image_url_right}" alt="DIEMS Logo" style="width:150px; height:150px; border-radius: 50%;">
    </div>
    """, unsafe_allow_html=True)



# student's subject selection check box:

subject_option = st.selectbox(
    "Select Student's Submission Subject",
    ("AI (Artifical Intelligence)", "CC (Cloud Computing)", "BDA (Big Data Analytics)"
     ,"BCT (Block Chain Technology)", "DL (Deep Learning)"),
    index=None,
    placeholder="Select Subject...",
)

st.write("You selected Subject is:", subject_option)






session = get_active_session()

# Select ROLL_NO, NAME_OF_STUDENT, and CLASS columns from the table
my_dataframe = session.table("DIEMS_CA.PUBLIC.STUDENT_DETAILS").select(col('ROLL_NO'), col('NAME_OF_STUDENT'), col('CLASS'))

# Extract roll numbers, corresponding student names, and classes into a dictionary for easy lookup
roll_number_dict = {row['ROLL_NO']: (row['NAME_OF_STUDENT'], row['CLASS']) for row in my_dataframe.collect()}

# Create a list of roll numbers for the selectbox options
roll_numbers = list(roll_number_dict.keys())

# Insert a placeholder at the beginning of the list
roll_numbers.insert(0, "Select Roll Number...")

# Student roll number selection drop-down with placeholder
roll_option = st.selectbox(
    "Select Student's Rollno",
    options=roll_numbers,  # Pass the list of roll numbers with placeholder
    index=0  # Set the index to 0 to show the placeholder as the default
)

# Initialize student_name and class_name as None
student_name = None
class_name = None

# Only fetch the student name and class if a valid roll number is selected
if roll_option != "Select Roll Number...":
    # Fetch the student's name and class based on the selected roll number
    student_name, class_name = roll_number_dict.get(roll_option)
    
    # Display the selected roll number, student's name, and class
    st.write(f"Selected Roll Number: {roll_option}")
    st.write(f"Student Name: {student_name}")
    st.write(f"Class: {class_name}")

# Assuming roll_option, subject_option, student_name, and class_name are selected
if student_name and class_name:
    # Use an f-string for formatting the SQL query, adding Student_Name and Class to the query
    my_insert_stmt = f"""
    INSERT INTO DIEMS_CA.PUBLIC.submission
    (rollno, subject, Student_Name, Class)
    VALUES ('{roll_option}', '{subject_option}', '{student_name}', '{class_name}')
    """

    # Button to submit the form
    time_to_insert = st.button("Submit Assignment")

    if time_to_insert:
        # Execute the SQL query
        session.sql(my_insert_stmt).collect()
        
        # Display success message
        st.success(f'Your Assignment is submitted, {student_name}!', icon="✅")



