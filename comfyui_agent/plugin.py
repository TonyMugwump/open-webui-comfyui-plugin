"""Core plugin functionality."""
import os
import json
import uuid
import base64
import logging
import requests
import websocket
from pathlib import Path
from typing import Dict, Any, Optional
from PIL import Image

logger = logging.getLogger(__name__)

class ComfyUIAgent:
    def __init__(self):
        self.api_url = os.getenv('COMFYUI_API_URL', 'http://comfyui:8188')
        self.data_dir = os.getenv('PLUGIN_DATA_DIR', '/app/backend/data')
        self.outputs_dir = os.path.join(self.data_dir, 'outputs/comfyui')
        self.cache_dir = os.path.join(self.data_dir, 'cache/comfyui')
        self.logs_dir = os.path.join(self.data_dir, 'logs/comfyui')
        
        for dir_path in [self.outputs_dir, self.cache_dir, self.logs_dir]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            
    def generate_image(
        self,
        description: str,
        negative_prompt: str = "ugly, blurry, low quality",
        width: int = 512,
        height: int = 512,
        steps: int = 20,
        cfg_scale: float = 7.0,
        model: str = "flux.1-dev",
        sampler: str = "euler",
        scheduler: str = "normal",
        seed: int = -1,
    ) -> Dict[str, Any]:
        """Generate an image using ComfyUI."""
        try:
            workflow = {
                "3": {
                    "class_type": "KSampler",
                    "inputs": {
                        "cfg": cfg_scale,
                        "denoise": 1,
                        "model": ["4", 0],
                        "negative": ["6", 0],
                        "positive": ["5", 0],
                        "sampler_name": sampler,
                        "scheduler": scheduler,
                        "seed": seed,
                        "steps": steps
                    }
                },
                "4": {
                    "class_type": "CheckpointLoaderSimple",
                    "inputs": {
                        "ckpt_name": model
                    }
                },
                "5": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "clip": ["4", 1],
                        "text": description
                    }
                },
                "6": {
                    "class_type": "CLIPTextEncode",
                    "inputs": {
                        "clip": ["4", 1],
                        "text": negative_prompt
                    }
                },
                "7": {
                    "class_type": "VAEDecode",
                    "inputs": {
                        "samples": ["3", 0],
                        "vae": ["4", 2]
                    }
                },
                "8": {
                    "class_type": "SaveImage",
                    "inputs": {
                        "filename_prefix": "ComfyUI",
                        "images": ["7", 0]
                    }
                }
            }

            client_id = str(uuid.uuid4())
            server_address = self.api_url.replace('http://', '')
            
            response = requests.post(f"http://{server_address}/prompt", json={
                "prompt": workflow,
                "client_id": client_id
            })
            response.raise_for_status()
            
            ws = websocket.WebSocket()
            ws.connect(f"ws://{server_address}/ws?clientId={client_id}")
            
            while True:
                out = ws.recv()
                if out:
                    message = json.loads(out)
                    if message['type'] == 'executing':
                        logger.info(f"Executing node: {message['data']['node']}")
                    elif message['type'] == 'progress':
                        logger.info(f"Progress: {message['data']['value']*100:.0f}%")
                    elif message['type'] == 'executed':
                        if 'output' in message['data']:
                            output = message['data']['output']
                            if 'images' in output:
                                image_data = output['images'][0]
                                image_binary = base64.b64decode(image_data.split(",")[1])
                                image_path = os.path.join(self.outputs_dir, f"{client_id}.png")
                                with open(image_path, "wb") as f:
                                    f.write(image_binary)
                                return {
                                    "success": True,
                                    "image_path": image_path,
                                    "client_id": client_id
                                }
                    elif message['type'] == 'error':
                        raise Exception(f"ComfyUI error: {message['data']['message']}")
                        
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def analyze_image(
        self,
        image_path: str,
        description: str,
    ) -> Dict[str, Any]:
        """Analyze how well an image matches a description using CLIP."""
        try:
            from transformers import CLIPProcessor, CLIPModel
            import torch
            
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
            processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            
            image = Image.open(image_path)
            inputs = processor(
                text=[description],
                images=[image],
                return_tensors="pt",
                padding=True
            )
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = model(**inputs)
                score = outputs.logits_per_image[0][0].item()
            
            return {
                "success": True,
                "score": score,
                "image_path": image_path
            }
            
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return {
                "success": False,
                "error": str(e)
            }

agent = ComfyUIAgent()
generate_image = agent.generate_image
analyze_image = agent.analyze_image
