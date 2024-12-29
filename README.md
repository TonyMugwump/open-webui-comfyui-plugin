# ComfyUI Agent Plugin for Open WebUI

A plugin that adds intelligent image generation capabilities to Open WebUI using ComfyUI with CLIP-guided refinement.

## Features

- Generate images using ComfyUI with automatic parameter adjustment
- Analyze images using CLIP for similarity scoring
- Real-time progress updates via WebSocket
- Progressive prompt refinement based on feedback

## Installation

1. Create required directories:
```bash
mkdir -p open-webui/data/outputs/comfyui \
         open-webui/data/cache/comfyui \
         open-webui/data/logs/comfyui \
         open-webui/extensions/plugins
```

2. Clone the plugin:
```bash
cd open-webui/extensions/plugins
git clone https://github.com/TonyMugwump/open-webui-comfyui-plugin.git comfyui-agent
```

3. Update your docker-compose.yml:
```yaml
services:
  open-webui:
    volumes:
      - ./open-webui/data:/app/backend/data
      - ./open-webui/extensions:/app/backend/extensions
    environment:
      - COMFYUI_API_URL=http://comfyui:8188

  comfyui:
    image: comfyanonymous/comfyui:latest
    ports:
      - "8188:8188"
    volumes:
      - ./comfyui:/app/comfyui
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

## Usage

### In Open WebUI Chat

The plugin provides two functions that can be used in conversations:

1. Generate an image:
```
Assistant: Let me generate that image for you.
Function: generate_image
Parameters:
  description: "A beautiful sunset over mountains"
  negative_prompt: "ugly, blurry, low quality"
  width: 512
  height: 512
  steps: 20
  cfg_scale: 7.0
  model: "flux.1-dev"
  sampler: "euler"
  scheduler: "normal"
  seed: -1
```

2. Analyze an image:
```
Assistant: Let me analyze how well the image matches your description.
Function: analyze_image
Parameters:
  image_path: "/path/to/image.png"
  description: "A beautiful sunset over mountains"
```

### In Python

```python
from comfyui_agent import generate_image, analyze_image

# Generate an image
result = generate_image(
    description="A beautiful sunset over mountains",
    negative_prompt="ugly, blurry, low quality",
    width=512,
    height=512,
    steps=20,
    cfg_scale=7.0,
    model="flux.1-dev",
    sampler="euler",
    scheduler="normal",
    seed=-1
)

if result["success"]:
    print(f"Image generated at: {result['image_path']}")
    
    # Analyze the generated image
    analysis = analyze_image(
        image_path=result["image_path"],
        description="A beautiful sunset over mountains"
    )
    
    if analysis["success"]:
        print(f"Image similarity score: {analysis['score']}")
```

## Configuration

Environment variables:
- `COMFYUI_API_URL`: URL of the ComfyUI API (default: http://comfyui:8188)
- `PLUGIN_DATA_DIR`: Base directory for plugin data (default: /app/backend/data)

## Development

1. Clone the repository:
```bash
git clone https://github.com/TonyMugwump/open-webui-comfyui-plugin.git
cd open-webui-comfyui-plugin
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
pytest
```

## License

MIT License
