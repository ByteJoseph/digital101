import streamlit as st
import pandas as pd
import os
from streamlit_js_eval import streamlit_js_eval
import google.generativeai as genai
import requests
genai.configure(api_key=st.secrets["api"]["gemini_key"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("Digital 101")
st.markdown("""
Welcome to my learning hub! Here you'll find curated content to strengthen your mooc foundations.
""")

load_bar = st.progress(0)
st.caption("% of LLM performance")
st.subheader("📚 Topics")
topics = [
    "An Overview of Artificial Intelligence",
    "Introduction to Machine Learning",
    "Introduction to Deep Learning",
    "ChatGPT",
    "GPT-4",
    "ChatGPT in Marketing",
    "OpenAI Tools AI Text Classifier",
    "OpenAI Tools Point-E",
    "OpenAI Tools Text-to-Image Generator DALL-E",
    "Applications of Artificial Intelligence",
    "Intelligent Wearables and Bionics",
    "AI in Electric Vehicles (EVs)",
    "AI and Metaverse",
    "Impact of Artificial Intelligence on Workforce and Workplace",
    "Future of Artificial Intelligence in Various Industries",
    "Edge AI OR TinyML",
    "Quantum Computing",
    "Evolution of Big Data Analytics",
    "An Overview of Big Data Analytics",
    "Applications of Big Data Analytics",
    "Database Management for Data Science",
    "Getting Started with Internet of Things",
    "Applications of IoT",
    "Industrial Internet of Things or IIoT",
    "Digital Payments",
    "An Overview of Cloud Computing",
    "Applications of Cloud Computing",
    "Service Models in Cloud Computing",
    "Popular Software Tools and Techniques Used in Cloud Computing",
    "An Overview of Cybersecurity",
    "Applications of Cybersecurity",
    "Types of Cyber Attacks",
    "Data Privacy and User Data Control",
    "Deepfake",
    "Evolution of Blockchain",
    "Getting Started with Blockchain",
    "Applications of Blockchain in Finance Industry",
    "Impact of Blockchain on Workforce & Workplace",
    "Getting Started with Robotic Process Automation",
    "3 Core Technologies of Robotic Process Automation",
    "Applications of Robotic Process Automation in Banking & Insurance Industry",
    "Getting Started with Web, Mobile Development and Marketing",
    "5Ds of Digital Marketing",
    "Digital Storytelling",
    "Getting Started with 3D Printing & Modeling",
    "Digital Manufacturing",
    "Future of 3D Printing & Modeling in Various Industries",
    "Getting Started with Augmented Reality and Virtual Reality",
    "Pre-requisites for Augmented Reality & Virtual Reality",
    "Metaverse",
    "Applications of Augmented Reality & Virtual Reality in Banking & Insurance",
    "VR Best Practices and Challenges",
    "AI Ethics",
    "Ethical Considerations of Generative AI"
]

selected_topic = st.selectbox(":rainbow[Choose a topic to begin:]", topics)

filename = selected_topic.replace("✅", "").strip().replace(" ", " ").rstrip() + ".csv"
path = f"./dataset/{filename}"


if not os.path.exists(path):
    st.warning(f"⚠️ Content for this topic is missing. Showing fallback content.")
    path = "./dataset/none.csv"


try:
    df = pd.read_csv(path)
    num_rows = df.shape[0]
    st.markdown(f"### 📝 Lesson: {selected_topic}")
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Failed to load content: {e}")
st.markdown("#### 🗒️ Lesson Topics Summary")
def is_image(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=3)
        content_type = response.headers.get("Content-Type", "")
        return content_type.startswith("image/")
    except:
        return False
for i, row in enumerate(df.itertuples(), start=1):
    st.markdown(f"#### {i}. {row.Topic}")
    if is_image(row.URL):
        st.image(row.URL, caption=row.Topic, use_column_width=True)
    elif "youtube.com" in row.URL or "youtu.be" in row.URL:
        # Embed YouTube video
        st.video(row.URL)
    else:
        prompt = f"Create a detailed summary of {row.URL} without loosing any information. don't specifically include the name of blog, be data heavy and explain it roughly. and include a table whenever possible (not exceeding 2-3 columns / use additional tables if yu want to express more) and say why it is. reduce errors"
        gem_response = model.generate_content(prompt)
        safe_html = f"""
<div style="overflow-x: auto; white-space: normal; word-wrap: break-word; font-size:12px;">
<pre style="white-space: pre-wrap;">{gem_response.text}</pre>
</div>
"""


        st.markdown(safe_html, unsafe_allow_html=True)
        print(gem_response.text)

    load_bar.progress((i//num_rows)*100)
st.markdown("---")
st.markdown("<p style='text-align: center;'>Made with 💛 by <a href='https://github.com/ByteJoseph'><b>Joseph</b></a></p>", unsafe_allow_html=True)
# I will implement this later :)
# st.subheader("🧠 Quick Quiz")

# question = "What is a strong password made of?"
# options = ["Only numbers", "Common words", "A mix of letters, numbers, and symbols"]
# answer = st.radio(question, options)

# if st.button("Submit Answer"):
#     if answer == options[2]:
#         st.success("Correct! 🔐")
#     else:
#         st.error("Oops! Try again.")
# st.markdown("---")

