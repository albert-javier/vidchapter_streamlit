import pandas as pd
import json
import requests
import validators
import streamlit as st
from streamlit import session_state as ss
from streamlit_player import st_player
from urllib.parse import urlparse
from urllib.parse import parse_qs

# --- App Styles ---
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #e5e5f7;
    }
    .title {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- App Title ---
st.markdown('<h1 class="title">AI-Powered Video Chaptering</h1>', unsafe_allow_html=True)
st.markdown('<h6 class="title" style="font-weight: normal;">Revolutionize your video content with intelligent, automated chapter creation.</h6>', unsafe_allow_html=True)

st.divider()

# --- Session State Initialization ---
if "df" not in ss:
    ss.df = pd.DataFrame(columns=["Time", "Chapter Title", "Link"])  # Placeholder DataFrame

if "video_url" not in ss:
    ss.video_url = None

if "selected_chapter" not in ss:
    ss.selected_chapter = None
    
if "is_error" not in ss:
    ss.is_error = 0

# --- Input Section ---
st.write("### YouTube Video URL Input")
video_url = st.text_input("Paste a YouTube URL link here", value="https://www.youtube.com/watch?v=SCd5SDLamK0")

# --- Function Definitions ---
def render_table_headers(columns, extra_column="Action"):
    """Render the headers for the table."""
    header_cols = st.columns(len(columns) + 1)  # +1 for the Action column
    for i, col_name in enumerate(columns + [extra_column]):
        header_cols[i].write(f"**{col_name}**")

def generate_chapters(video_url):
    """Mock chapter generation logic (replace with actual API call)."""
    
    parsed_url = urlparse(video_url)
    captured_value = parse_qs(parsed_url.query)['v'][0]

    print("youtube video id:",captured_value)
    
        
    # # URL to send the request to
    # url = "http://127.0.0.1:5000/vidchap/chaptering"

    # # Headers to indicate JSON content
    # headers = {
    #     "Content-Type": "application/json",
    #     # "Authorization": "Bearer your_api_token"  # Optional, for authenticated APIs
    # }

    # # JSON body to send
    # jdata = {
    #     "video_id": captured_value
    # }

    # data = None
    
    # try:
    #     # Sending POST request with JSON body
    #     response = requests.post(url, headers=headers, json=jdata)

    #     # Check response status code
    #     if response.status_code == 200:
    #         print("Success:", response.json())  # or response.text for raw response
            
    #         # str1 = str(response.json())
    #         # data = json.loads(str1)["results"]
            
    #         data = response.json()["results"]
                        
    #     else:
    #         print(f"Failed with status code {response.status_code}: {response.text}")

    # except requests.exceptions.RequestException as e:
    #     print("An error occurred:", e)    
        
        
    # if data is None:
    #     return pd.DataFrame(columns=["Time", "Chapter Title", "Link"])  # Placeholder DataFrame
        
    
    
    #DUMMY DATA
    response = """
    {
        "results": [
            {"start_time": 0.0, "end_time": 20.0, "prediction": "advertisement", "video_id": "SCd5SDLamK0"},
            {"start_time": 20.0, "end_time": 69.0, "prediction": "introduction", "video_id": "SCd5SDLamK0"},
            {"start_time": 69.0, "end_time": 135.0, "prediction": "outro", "video_id": "SCd5SDLamK0"},
            {"start_time": 135.0, "end_time": 169.0, "prediction": "how to claim your company page", "video_id": "SCd5SDLamK0"}
        ]
    }
    """
    data = json.loads(response)["results"]
    
    
    
    
    df = pd.DataFrame(data)
    df.rename(columns={"start_time": "Start Time", "end_time": "End Time", "prediction": "Chapter Title"}, inplace=True)
    df["Time"] = df["Start Time"].astype(str) + " - " + df["End Time"].astype(str)
    df["Link"] = "https://www.youtube.com/watch?v=" + df["video_id"] + "&t=" + df["Start Time"].astype(str) + "s"
    return df[["Time", "Chapter Title", "Link"]]

# --- Generate Chapters ---
if st.button("Generate Chapter List"):
    if validators.url(video_url) and "youtube.com/watch" in video_url:
        ss.video_url = video_url
        
        with st.spinner("Processing... Please wait!"):
            ss.df = generate_chapters(video_url)
            
        if(ss.df.empty):
            st.error("Error in generating chapters. Please try again later.")
            ss.is_error = 1
            
        else:
            ss.is_error = 0
            st.success("Chapters generated successfully!")
            
    else:
        st.error("Please enter a valid YouTube video URL.")

# --- Display Chapters Table ---
st.write("### Generated Chapters")
if ss.df.empty:
    if ss.is_error == 1:
        st.error("Error in generating chapters. Please try again later.")
    else:
        st.warning("No chapters generated yet. Please provide a valid video URL and click 'Generate Chapter List'.")
else:
    render_table_headers(list(ss.df.columns))
    for index, row in ss.df.iterrows():
        cols = st.columns(len(ss.df.columns) + 1)
        for col_index, (col_name, cell_value) in enumerate(row.items()):
            cols[col_index].write(cell_value)
        if cols[-1].button(f"Play Chapter {index + 1}", key=f"play_chapter_{index}"):
            ss.video_url = row["Link"]
            ss.selected_chapter = row["Chapter Title"].title()

# --- Play Selected Chapter ---
if ss.video_url:
    st.divider()
    st.markdown(f"### {ss.selected_chapter or 'Selected Chapter'}")
    st_player(ss.video_url, playing=True, controls=True, key="video_player")
