import streamlit as st
import requests

API_URL = 'http://backend:8000'
st.title("Friendly audio to text app")

options = {
    0: "Record",
    1: "Upload audio file"
}

permitted_audio_formats = ['wav', 'flac', 'alac', 'mp3', 'aac', 'm4a']

if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None

if 'transcribe_disabled' not in st.session_state:
    st.session_state.transcribe_disabled = False

summarize = st.checkbox('Summarize')

selection = st.segmented_control(
    "Select wheter you want to record yourself or upload an audio file: ",
    options=options.keys(),
    format_func=lambda option: options[option],
    selection_mode="single"
)

def handle_input():
    if selection == 0:
        st.session_state.audio_data = st.session_state.audio_input
    elif selection == 1:
        st.session_state.audio_data = st.session_state.audio_upload

def disable_button():
    st.session_state.transcribe_disabled = True

def enable_button():
    st.session_state.transcribe_disabled = False

if selection is None:
    st.write("No option selected yet")
elif selection == 0:
    recording = st.audio_input(
        label="Start recording!",
        key="audio_input",
        on_change=handle_input
    )
elif selection == 1:
    uploaded_file = st.file_uploader(
        label="Select audio file",
        key="audio_upload",
        type=permitted_audio_formats,
        on_change=handle_input
    )

status_placeholder = st.empty()

if st.session_state.audio_data:
    col1, col2 = st.columns([0.8, 0.2])

    with col1:
        st.audio(st.session_state.audio_data)

    with col2:
        button_clicked = st.button(
            label="Transcribe",
            type="primary",
            icon=":material/call_made:",
            on_click=disable_button,
            disabled=st.session_state.transcribe_disabled
        )

    if button_clicked:
        with status_placeholder.container():
            import time as _time
            start_time = _time.time()
            with st.spinner("⏳ Processing... it may take a couple of minutes", show_time=True):
                # Prepare file for API call
                audio_data = st.session_state.audio_data
                if hasattr(audio_data, 'read'):  # Uploaded file
                    audio_data.seek(0)
                    files = {'audio_file': (audio_data.name, audio_data, audio_data.type)}
                else:  # Recorded audio (bytes)
                    files = {'audio_file': ("recording.wav", audio_data, "audio/wav")}
                try:
                    response = requests.post(f"{API_URL}/transcribe?summarize={summarize}", files=files)
                    result = response.json()
                except Exception as e:
                    result = {'error': str(e)}
            elapsed_time = _time.time() - start_time
            result['processing_time_seconds'] = f'{round(elapsed_time, 2)}'
        enable_button()
        st.write(result)

