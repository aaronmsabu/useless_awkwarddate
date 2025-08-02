# save as: streamlit_app.py
import streamlit as st
import cv2
import numpy as np
import time
from datetime import datetime
from final_awkwardness_detector import UltimateAwkwardnessDetector
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av

# Page configuration
st.set_page_config(page_title="Ultimate Dating Awkwardness Detector", page_icon="🎭", layout="wide")

# Initialize session state variables if they don't exist
if 'detector' not in st.session_state:
    st.session_state.detector = None
if 'awkwardness_history' not in st.session_state:
    st.session_state.awkwardness_history = []
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'processing_active' not in st.session_state:
    st.session_state.processing_active = False
if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
if 'last_frame_time' not in st.session_state:
    st.session_state.last_frame_time = time.time()
if 'current_score' not in st.session_state:
    st.session_state.current_score = 0
if 'current_frame' not in st.session_state:
    st.session_state.current_frame = None

# Title and introduction
st.title("🎭 Ultimate Awkwardness Detector")
st.write("The world's most advanced (and useless) social skills analyzer!")

# Sidebar controls
st.sidebar.header("Settings")
enable_memes = st.sidebar.checkbox("Enable Meme Mode", value=True)
enable_audio = st.sidebar.checkbox("Enable Audio Alerts", value=False)
sensitivity = st.sidebar.slider("Awkwardness Sensitivity", 0.5, 2.0, 1.0)

# Create two columns for the main interface
col1, col2 = st.columns([3, 2])

# Video processor class for real-time processing
class AwkwardnessVideoProcessor(VideoProcessorBase):
    def __init__(self, enable_memes, enable_audio, sensitivity):
        self.detector = UltimateAwkwardnessDetector(enable_memes=enable_memes, enable_audio=enable_audio)
        self.sensitivity = sensitivity
        st.session_state.detector = self.detector
        st.session_state.start_time = time.time()
        st.session_state.processing_active = True
        st.session_state.awkwardness_history = []
        
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # Process the frame with the awkwardness detector
        result_frame = self.detector.process_frame(img)
        
        # Apply sensitivity multiplier
        self.detector.awkwardness_score *= self.sensitivity
        
        # Store current score in session state for display
        st.session_state.current_score = self.detector.awkwardness_score
        st.session_state.current_frame = result_frame
        
        # Store history for graph
        current_time = time.time()
        if current_time - st.session_state.last_frame_time > 0.5:  # Limit data points
            st.session_state.awkwardness_history.append(self.detector.awkwardness_score)
            st.session_state.last_frame_time = current_time
            
            # Keep only the last 50 points
            if len(st.session_state.awkwardness_history) > 50:
                st.session_state.awkwardness_history = st.session_state.awkwardness_history[-50:]
        
        return av.VideoFrame.from_ndarray(result_frame, format="bgr24")

# RTC Configuration (use Google's STUN servers)
rtc_config = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Main interface with WebRTC streamer
with col1:
    # WebRTC streamer for real-time video
    ctx = webrtc_streamer(
        key="awkwardness-detector",
        video_processor_factory=lambda: AwkwardnessVideoProcessor(
            enable_memes=enable_memes,
            enable_audio=enable_audio,
            sensitivity=sensitivity
        ),
        rtc_configuration=rtc_config,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )
    
    # Display the current frame if available (as a backup)
    if st.session_state.current_frame is not None and not ctx.state.playing:
        st.image(st.session_state.current_frame, channels="BGR")

# Generate report button
with st.sidebar:
    if st.session_state.detector is not None:
        if st.button("Generate Awkwardness Report"):
            report = st.session_state.detector.generate_final_report()
            st.session_state.report = report
            st.session_state.report_generated = True

# Right column for stats and feedback
with col2:
    if st.session_state.detector is not None and st.session_state.processing_active:
        # Current awkwardness score
        st.subheader("Live Awkwardness Metrics")
        
        # Create a metric display
        current_score = st.session_state.current_score
        
        # Determine status based on score
        if current_score < 5:
            status = "😊 Smooth & Confident"
            st.success(f"Awkwardness Score: {current_score:.1f}")
        elif current_score < 15:
            status = "😐 Slightly Nervous"
            st.info(f"Awkwardness Score: {current_score:.1f}")
        elif current_score < 30:
            status = "😅 Getting Uncomfortable"
            st.warning(f"Awkwardness Score: {current_score:.1f}")
        elif current_score < 50:
            status = "😰 Major Awkwardness"
            st.error(f"Awkwardness Score: {current_score:.1f}")
        else:
            status = "🚨 SOCIAL CATASTROPHE!"
            st.error(f"Awkwardness Score: {current_score:.1f} - CRITICAL!")
        
        st.write(status)
        
        # Session stats
        if st.session_state.start_time:
            session_duration = time.time() - st.session_state.start_time
            st.write(f"Session Duration: {session_duration/60:.1f} minutes")
        
        # Show awkwardness history chart
        if len(st.session_state.awkwardness_history) > 1:
            st.subheader("Awkwardness Over Time")
            st.line_chart(st.session_state.awkwardness_history)
        
        # Show some stats from the detector
        if hasattr(st.session_state.detector, 'stats'):
            st.subheader("Behavior Analysis")
            stats = st.session_state.detector.stats
            st.write(f"Face Touches: {stats['face_touches']}")
            st.write(f"Eye Contact Breaks: {stats['eye_contact_breaks']}")
            st.write(f"Peak Awkwardness: {stats['peak_awkwardness']:.1f}")
    
    # Display report if generated
    if st.session_state.report_generated and hasattr(st.session_state, 'report'):
        st.subheader("📊 Awkwardness Analysis Report")
        for line in st.session_state.report:
            st.write(line)

# Run with: streamlit run streamlit_app.py