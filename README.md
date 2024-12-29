# ComfyUI Agent Plugin for Open WebUI

A plugin that adds intelligent image generation capabilities to Open WebUI using ComfyUI with CLIP-guided refinement.

## Installation

```bash
cd backend/extensions/plugins
git clone https://github.com/TonyMugwump/open-webui-comfyui-plugin.git comfyui-agent
```

## Usage

```python
from comfyui_agent import generate_image, analyze_image

# Generate image
result = generate_image(
    description="A beautiful sunset over mountains",
    width=512,
    height=512,
    steps=20,
    cfg_scale=7.0
)

# Analyze image
score = analyze_image(
    image_path=result["image_path"],
    description="A beautiful sunset over mountains"
)
```

## Configuration

Environment variables:
- `COMFYUI_API_URL`: ComfyUI API URL (default: http://comfyui:8188)
- `PLUGIN_DATA_DIR`: Data directory (default: /app/backend/data)
