import streamlit as st
import torch
import os
from model import load_model
from utils import generate_video_frames, save_video

def main():
    st.title("🎬 Local AI Video Generation")
    st.write("Generate creative videos using AI! Enter your prompt below.")
    
    # Display CUDA information
    st.sidebar.write("### System Information")
    st.sidebar.write(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        st.sidebar.write(f"Current device: {torch.cuda.get_device_name(0)}")
        st.sidebar.write(f"CUDA version: {torch.version.cuda}")

    # Model loading with spinner
    if 'model' not in st.session_state:
        with st.spinner("Loading model... This might take a few minutes."):
            st.session_state.model = load_model()
        st.success("Model loaded successfully!")

    # User inputs
    prompt = st.text_area(
        "Enter your prompt:",
        height=100,
        placeholder="Example: A panda playing guitar in a bamboo forest..."
    )
    
    col1, col2 = st.columns(2)
    with col1:
        num_frames = st.slider("Number of frames(8 Frames=1 second video)", min_value=8, max_value=64, value=49)
    with col2:
        seed = st.number_input("Random seed( for the randomness of video) ", min_value=0, max_value=1000000, value=42)

    # Generate button
    if st.button("🎨 Generate Video"):
        if not prompt:
            st.warning("Please enter a prompt first!")
            return
        
        with st.spinner("🎬 Generating your video... This might take a while."):
            try:
                frames = generate_video_frames(
                    st.session_state.model,
                    prompt,
                    num_frames=num_frames,
                    seed=seed
                )
                
                if frames is not None:
                    video_path = save_video(frames)
                    
                    # Display the video
                    st.success("✨ Video generated successfully!")
                    st.video(video_path)
                    
                    # Add download button
                    with open(video_path, 'rb') as file:
                        st.download_button(
                            label="📥 Download Video",
                            data=file,
                            file_name="generated_video.mp4",
                            mime="video/mp4"
                        )
                    
                    # Clean up temporary file
                    os.unlink(video_path)
            except Exception as e:
                st.error(f"Error generating video: {str(e)}")

if __name__ == "__main__":
    main()