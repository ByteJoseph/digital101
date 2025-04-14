import streamlit as st
import pandas as pd
import requests,time
import google.generativeai as genai
from pathlib import Path
from streamlit_js_eval import streamlit_js_eval
# from streamlit_scroll_to_top import scroll_to_here
genai.configure(api_key=st.secrets["api"]["gemini_key"])
model = genai.GenerativeModel('gemini-2.0-flash')
st.markdown("""<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">""", unsafe_allow_html=True)

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

def set_topic_index(new_index, key):
    streamlit_js_eval(js_expressions=f"localStorage.setItem('current_st_index', '{new_index}');", key=key)
    st.session_state.current_st_index = new_index
    st.rerun()

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
topic_index = topics.index(selected_topic)
load_bar.progress((topic_index + 1) / len(topics))

if topic_index < len(topics) - 1:
    if st.button("Next Topic", icon="▶", use_container_width=True,type="primary"):
        set_topic_index(topic_index + 1, "set-next-index")

if topic_index > 0:
    if st.button("Prev Topic", icon="◀", use_container_width=True):
        set_topic_index(topic_index - 1, "set-prev-index")

filename = selected_topic.replace("✅", "").strip() + ".csv"
path = Path("dataset") / filename

if not path.exists():
    st.warning("⚠️ Content for this topic is missing. Showing fallback content.")
    path = Path("dataset") / "none.csv"
else:
    msg = st.toast('Generating Response...', icon="🌐")

@st.cache_data
def load_csv(file_path):
    return pd.read_csv(file_path)

@st.cache_data(show_spinner=False)
def get_gemini_summary(prompt):
    return model.generate_content(prompt).text

try:
    df = load_csv(path)
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
    st.markdown("---")
    load_bar.progress((topic_index + 1) / len(topics))
    if not isinstance(row.URL, str) or not row.URL.strip():
        st.info(f"⚠️ No content available for topic {row.Topic}.")
        continue

    st.markdown(f"#### {i}. {row.Topic}")

    if is_image(row.URL):
        st.image(row.URL, caption=row.Topic, use_container_width=True)
    elif "youtube.com" in row.URL or "youtu.be" in row.URL:
        st.video(row.URL)
        with st.spinner("Wait, Generating.."):
          prompt = f"Summarize the topic {row.Topic} from the video."
          summary = get_gemini_summary(prompt)
          st.markdown(f"**Generated Summary:** {summary}", unsafe_allow_html=True)
    else:
        with st.spinner("Wait, Generating.."):
          prompt = f"Summarize the content from this URL in detail without losing key information. Do not mention the blog source or include any tables.\n\nURL: {row.URL} include points to revise faster,TL;DR, and Did you know? etc"
          summary = get_gemini_summary(prompt)
          st.markdown(f"**Generative Summary:** {summary}", unsafe_allow_html=True)
    st.markdown("---")
    
msg.toast("Success",icon="✔")
streamlit_js_eval(js_expressions="window.scrollTo(0, 0)", key="scroller")
if topic_index != len(topics) - 1:
    placeholder = st.empty()
    # js_code = """
    #  <script>
    # window.scrollTo({ top: 0, behavior: 'smooth' });
    # </script>
    #  """
    
    if st.button("Next Topic ",use_container_width=True,type="primary",icon="▶"):
        # streamlit_js_eval(js_expressions="window.location.href = 'https://www.example.com';", key="redirect")
        set_topic_index(topic_index + 1, "set-next-index")
else:
    
    if st.button("Go to the Beginning", use_container_width=True, type="primary"):
        st.session_state.clear()
        set_topic_index(0, "set-start-index")

st.markdown("---")
st.markdown("<p style='text-align: center;'>Made with 💛</p>", unsafe_allow_html=True)
