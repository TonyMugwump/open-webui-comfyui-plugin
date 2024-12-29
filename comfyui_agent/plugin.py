"""Core plugin functionality."""
import os
import json
import logging
import requests
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
            
    def generate_image(self, description: str, **kwargs) -> Dict[str, Any]:
        """Generate an image using ComfyUI."""
        try:
            workflow = self._prepare_workflow(prompt=description, **kwargs)
            response = requests.post(f"{self.api_url}/prompt", json={"prompt": workflow})
            response.raise_for_status()
            result = response.json()
            return {
                "success": True,
                "image_path": os.path.join(self.outputs_dir, f"{result['id']}.png"),
                "workflow_id": result['id']
            }
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return {"success": False, "error": str(e)}
            
    def analyze_image(self, image_path: str, description: str) -> Dict[str, Any]:
        """Analyze image using CLIP."""
        try:
            from transformers import CLIPProcessor, CLIPModel
            import torch
            
            device = "cuda" if torch.cuda.is_available() else "cpu"
            model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
            processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            
            image = Image.open(image_path)
            inputs = processor(text=[description], images=[image], return_tensors="pt", padding=True)
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = model(**inputs)
                score = outputs.logits_per_image[0][0].item()
            
            return {"success": True, "score": score, "image_path": image_path}
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return {"success": False, "error": str(e)}
            
    def _prepare_workflow(self, **kwargs) -> Dict[str, Any]:
        """Prepare ComfyUI workflow."""
        workflow_path = os.path.join(os.path.dirname(__file__), 'workflows/base.json')
        with open(workflow_path) as f:
            workflow = json.load(f)
            
        workflow['nodes'][1]['inputs']['text'] = kwargs.get('prompt', '')
        workflow['nodes'][4]['inputs']['width'] = kwargs.get('width', 512)
        workflow['nodes'][4]['inputs']['height'] = kwargs.get('height', 512)
        workflow['nodes'][3]['inputs']['steps'] = kwargs.get('steps', 20)
        workflow['nodes'][3]['inputs']['cfg'] = kwargs.get('cfg_scale', 7.0)
        
        return workflow

agent = ComfyUIAgent()
generate_image = agent.generate_image
analyze_image = agent.analyze_image
