# ComfyUI Agent Plugin for Open WebUI

A plugin that adds intelligent image generation capabilities to Open WebUI using ComfyUI with CLIP-guided refinement.

## Features

- Generate images using ComfyUI with automatic parameter adjustment
- Analyze images using CLIP for similarity scoring
- Docker and standard environment support
- Progressive prompt refinement based on feedback

## Installation

### Docker Installation

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

### Standard Installation

```bash
pip install -e .
```

## Usage

### In Python

```python
from comfyui_agent import generate_image, analyze_image

# Generate an image
result = generate_image(
    description="A beautiful sunset over mountains",
    width=512,
    height=512,
    steps=20,
    cfg_scale=7.0
)

# Analyze the image
analysis = analyze_image(
    image_path=result["image_path"],
    description="A beautiful sunset over mountains"
)
```

### In Open WebUI

The plugin provides two functions that can be used in conversations:

1. `generate_image`: Generate an image from a text description
```
Assistant: Let me generate that image for you.
Function: generate_image
Parameters:
  description: "A beautiful sunset over mountains"
  width: 512
  height: 512
  steps: 20
  cfg_scale: 7.0
```

2. `analyze_image`: Analyze how well an image matches a description
```
Assistant: Let me analyze how well the image matches your description.
Function: analyze_image
Parameters:
  image_path: "/path/to/image.png"
  description: "A beautiful sunset over mountains"
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

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

## License

MIT License
