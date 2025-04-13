import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
from pathlib import Path
from streamlit_js_eval import streamlit_js_eval

genai.configure(api_key=st.secrets["api"]["gemini_key"])
model = genai.GenerativeModel('gemini-2.0-flash')
st.markdown("""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
""", unsafe_allow_html=True)

st.title("Digital 101")
st.markdown("Welcome to my revision hub!")
load_bar = st.progress(0)

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

if "current_st_index" not in st.session_state:
    stored_index = streamlit_js_eval(
        js_expressions="localStorage.getItem('current_st_index');",
        key="get-current-st-index",
        want_return_value=True
    )
    try:
        st.session_state.current_st_index = max(0, min(int(stored_index or 0), len(topics) - 1))
    except (ValueError, TypeError):
        st.session_state.current_st_index = 0

index = st.session_state.current_st_index

selected_topic = st.selectbox("🎯 Choose a topic to begin:", topics, index=index)
load_bar.progress((index + 1) / len(topics))
if st.button("Next Topic",icon="▶",use_container_width=True) and index < len(topics) - 1:
        new_index = index + 1
        streamlit_js_eval(
            js_expressions=f"localStorage.setItem('current_st_index', '{new_index}');",
            key="set-next-index"
        )
        st.session_state.current_st_index = new_index
        st.rerun()
if index > 0:
 if st.button("Prev Topic",icon="◀",use_container_width=True) and index > 0:
        new_index = index - 1
        streamlit_js_eval(
            js_expressions=f"localStorage.setItem('current_st_index', '{new_index}');",
            key="set-prev-index"
        )
        st.session_state.current_st_index = new_index
        st.rerun()

filename = selected_topic.replace("✅", "").strip() + ".csv"
path = Path("dataset") / filename

if not path.exists():
    st.warning("⚠️ Content for this topic is missing. Showing fallback content.")
    path = Path("dataset") / "none.csv"
else:
    msg = st.toast('Generating Response...',icon="🌐")

try:
    df = pd.read_csv(path)
    num_rows = df.shape[0]
    st.markdown(f"### 📝 Lesson: {selected_topic}")
    st.dataframe(df, use_container_width=True)
except Exception as e:
    st.error(f"Failed to load content: {e}")
    st.stop()

st.markdown("#### 🗒️ Lesson Topics Summary")

def is_image(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=3)
        content_type = response.headers.get("Content-Type", "")
        return content_type.startswith("image/")
    except:
        return False

for i, row in enumerate(df.itertuples(), start=1):
    load_bar.progress((index + 1) / len(topics))
    if not isinstance(row.URL, str) or not row.URL.strip():
        st.info(f"⚠️ No content available for topic {row.Topic}.")
        continue

    st.markdown(f"#### {i}. {row.Topic}")
    
    if is_image(row.URL):
        st.image(row.URL, caption=row.Topic, use_container_width=True)
    elif "youtube.com" in row.URL or "youtu.be" in row.URL:
        st.video(row.URL)
        prompt = f"Summarize the topic {row.Topic} from the video."
        gem_response = model.generate_content(prompt)
        st.markdown(f"**AI Summary:** {gem_response.text}", unsafe_allow_html=True)
    else:
        prompt = f"Summarize the content from this URL in detail without losing key information. Do not mention the blog source or include any tables.\n\nURL: {row.URL}"
        gem_response = model.generate_content(prompt)
        st.markdown(f"**AI Summary:** {gem_response.text}", unsafe_allow_html=True)

    
msg.toast("Success")
if st.button("Continue",use_container_width=True,type="primary") and index < len(topics) - 1:
        new_index = index + 1
        streamlit_js_eval(
            js_expressions=f"localStorage.setItem('current_st_index', '{new_index}');",
            key="set-next-index"
        )
        st.session_state.current_st_index = new_index
        st.rerun()
st.markdown("---")
st.markdown("<p style='text-align: center;'>Made with 💛 by <a href='https://github.com/ByteJoseph'><b>Joseph</b></a></p>", unsafe_allow_html=True)
