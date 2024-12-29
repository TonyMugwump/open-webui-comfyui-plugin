from setuptools import setup, find_packages

setup(
    name="open-webui-comfyui-plugin",
    version="0.1.0",
    description="ComfyUI Agent Plugin for Open WebUI",
    packages=find_packages(),
    package_data={'comfyui_agent': ['workflows/*.json']},
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.36.0",
        "Pillow>=11.0.0",
        "requests>=2.31.0",
        "numpy>=1.24.0",
    ],
    python_requires=">=3.8",
)
