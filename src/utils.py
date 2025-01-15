import torch
from diffusers.utils import export_to_video
import tempfile

def generate_video_frames(pipe, prompt, num_frames=49, seed=42):
    """
    Generate video frames using the provided model pipeline.
    
    Args:
        pipe: The CogVideoX pipeline
        prompt (str): Text prompt for video generation
        num_frames (int): Number of frames to generate
        seed (int): Random seed for reproducibility
        
    Returns:
        torch.Tensor: Generated video frames
    """
    # Create generator based on available device
    if torch.cuda.is_available():
        generator = torch.Generator(device="cuda")
    else:
        generator = torch.Generator()
    generator.manual_seed(seed)
    
    video = pipe(
        prompt=prompt,
        num_videos_per_prompt=1,
        num_inference_steps=50,
        num_frames=num_frames,
        guidance_scale=6,
        generator=generator,
    ).frames[0]
    
    return video

def save_video(frames, fps=8):
    """
    Save video frames to a temporary file.
    
    Args:
        frames (torch.Tensor): Video frames to save
        fps (int): Frames per second for the output video
        
    Returns:
        str: Path to the saved video file
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
        export_to_video(frames, tmpfile.name, fps=fps)
        return tmpfile.name