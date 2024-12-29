"""Functions exported to Open WebUI."""
import json
from typing import Dict, Any
from comfyui_agent.plugin import generate_image, analyze_image

def get_functions() -> Dict[str, Any]:
    """Return the functions that will be exposed to Open WebUI."""
    return json.loads("""{
        "generate_image": {
            "name": "generate_image",
            "description": "Generate an image using ComfyUI with CLIP-guided refinement",
            "parameters": {
                "description": {
                    "type": "string",
                    "description": "Text description of the image to generate"
                },
                "negative_prompt": {
                    "type": "string",
                    "description": "Negative prompt to guide what not to generate",
                    "default": "ugly, blurry, low quality"
                },
                "width": {
                    "type": "integer",
                    "description": "Image width",
                    "default": 512
                },
                "height": {
                    "type": "integer",
                    "description": "Image height",
                    "default": 512
                },
                "steps": {
                    "type": "integer",
                    "description": "Number of sampling steps",
                    "default": 20
                },
                "cfg_scale": {
                    "type": "number",
                    "description": "Classifier-free guidance scale",
                    "default": 7.0
                },
                "model": {
                    "type": "string",
                    "description": "Model checkpoint to use",
                    "default": "flux.1-dev"
                },
                "sampler": {
                    "type": "string",
                    "description": "Sampling method",
                    "default": "euler"
                },
                "scheduler": {
                    "type": "string",
                    "description": "Scheduler type",
                    "default": "normal"
                },
                "seed": {
                    "type": "integer",
                    "description": "Random seed (-1 for random)",
                    "default": -1
                }
            },
            "function": "generate_image"
        },
        "analyze_image": {
            "name": "analyze_image",
            "description": "Analyze how well an image matches a description using CLIP",
            "parameters": {
                "image_path": {
                    "type": "string",
                    "description": "Path to the image file"
                },
                "description": {
                    "type": "string",
                    "description": "Text description to compare against"
                }
            },
            "function": "analyze_image"
        }
    }""")
