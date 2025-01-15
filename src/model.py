import torch
from diffusers import CogVideoXPipeline

def load_model():
    """
    Load and configure the CogVideoX model.
    Returns:
        CogVideoXPipeline: The loaded and configured model pipeline
    """
    pipe = CogVideoXPipeline.from_pretrained(
        "THUDM/CogVideoX-5b",
        torch_dtype=torch.bfloat16
    )
    pipe.enable_model_cpu_offload()
    pipe.vae.enable_tiling()
    return pipe
