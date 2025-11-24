import streamlit as st
import pyttsx3
import tempfile

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Page Settings
st.set_page_config(page_title="Text-to-Speech", page_icon="🎤", layout="centered")
st.title("🎤 Text-to-Speech Converter")
st.write("Convert text into speech with language, voice gender, speed control, and file support.")

# ---------------------------
# File Upload Feature
# ---------------------------
uploaded_file = st.file_uploader("Upload a text file (.txt)", type=["txt"])
file_text = ""

if uploaded_file:
    file_text = uploaded_file.read().decode("utf-8")
    st.success("File loaded successfully!")
    st.text_area("File Content:", file_text, height=200)

# ---------------------------
# Manual Text Input
# ---------------------------
st.subheader("Or Enter Text Manually")
manual_text = st.text_area("Enter your text:", height=150)

# Combine file text & manual text
text_to_convert = file_text if file_text else manual_text

# ---------------------------
# Voice Gender
# ---------------------------
voice_gender = st.selectbox("Select Voice Gender", ["Female", "Male"])

voices = engine.getProperty("voices")
if voice_gender == "Male":
    engine.setProperty("voice", voices[0].id)  # Usually male
else:
    engine.setProperty("voice", voices[1].id)  # Usually female

# ---------------------------
# Speed Control
# ---------------------------
speed = st.slider("Select Speech Speed (Words Per Minute)", 100, 250, 150)
engine.setProperty("rate", speed)

# ---------------------------
# Convert Button
# ---------------------------
if st.button("🔊 Convert to Speech"):
    if not text_to_convert.strip():
        st.warning("Please enter some text or upload a file!")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            temp_filename = tmp_file.name

        # Save speech to file
        engine.save_to_file(text_to_convert, temp_filename)
        engine.runAndWait()

        st.success("Speech generated successfully!")

        # Audio Player
        st.audio(temp_filename, format="audio/mp3")

        # Download Button
        with open(temp_filename, "rb") as f:
            st.download_button(
                label="Download Audio",
                data=f,
                file_name="speech_output.mp3",
                mime="audio/mp3"
            )
