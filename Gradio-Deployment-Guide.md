# 🚀 Gradio Deployment Guide

A comprehensive guide to deploying Gradio applications and managing Hugging Face tokens.

## 📋 Table of Contents
- [Deployment Options](#deployment-options)
- [Token Management](#token-management)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## 🎯 Deployment Options

### 1. Hugging Face Spaces
**Recommended for:**
- Quick deployments
- Free hosting
- Easy sharing
- Automatic updates

**Steps:**
1. Create a new Space on Hugging Face
2. Choose Gradio as the SDK
3. Push your code to the Space
4. Your app will be automatically deployed

```python
# app.py
import gradio as gr

def greet(name):
    return f"Hello {name}!"

demo = gr.Interface(
    fn=greet,
    inputs="text",
    outputs="text"
)

demo.launch()  # For local testing
```

### 2. Custom Server Deployment
**Recommended for:**
- Production environments
- Custom domains
- More control
- Higher resource needs

**Steps:**
1. Set up a server (AWS, GCP, Azure, etc.)
2. Install requirements
3. Run with gunicorn or similar

```bash
# Install requirements
pip install gradio gunicorn

# Run with gunicorn
gunicorn app:app.server --bind 0.0.0.0:7860
```

### 3. Docker Deployment
**Recommended for:**
- Consistent environments
- Easy scaling
- Container orchestration

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 7860

CMD ["python", "app.py"]
```

## 🔑 Token Management

### 1. Environment Variables
Store your HF token in environment variables:

```python
# .env file
HF_TOKEN=your_token_here
```

```python
# app.py
import os
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
```

### 2. Configuration File
Create a config file (don't commit to git):

```python
# config.py
HF_TOKEN = "your_token_here"
```

### 3. Secure Storage
For production, use secure storage solutions:

- AWS Secrets Manager
- Google Secret Manager
- Azure Key Vault

## ⚡ Best Practices

### 1. Security
- Never commit tokens to git
- Use environment variables
- Implement rate limiting
- Add authentication if needed

### 2. Performance
- Cache expensive operations
- Use async functions
- Optimize model loading
- Monitor resource usage

### 3. Error Handling
```python
import gradio as gr

def process_input(input_text):
    try:
        # Your processing logic
        return result
    except Exception as e:
        return f"Error: {str(e)}"

demo = gr.Interface(
    fn=process_input,
    inputs="text",
    outputs="text",
    examples=[["Example input"]]
)
```

### 4. Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_input(input_text):
    logger.info(f"Processing input: {input_text}")
    # Your logic here
```

## 🔧 Troubleshooting

### Common Issues

1. **Token Authentication Failed**
   - Check token validity
   - Verify environment variables
   - Ensure proper token format

2. **Deployment Failures**
   - Check logs
   - Verify requirements
   - Test locally first

3. **Performance Issues**
   - Monitor memory usage
   - Check CPU utilization
   - Optimize model loading

### Debugging Tips

1. Enable debug mode:
```python
demo.launch(debug=True)
```

2. Check logs:
```bash
tail -f /var/log/your-app.log
```

3. Monitor resources:
```bash
htop  # or similar system monitor
```

## 📚 Resources

### Documentation
- [Gradio Documentation](https://gradio.app/docs/)
- [Hugging Face Spaces](https://huggingface.co/spaces)
- [Deployment Guide](https://gradio.app/deploying-to-a-shared-url/)

### Community
- [Gradio Discord](https://discord.gg/feTf9x3ZSB)
- [Hugging Face Forums](https://discuss.huggingface.co/)
- [GitHub Discussions](https://github.com/gradio-app/gradio/discussions)

## 🚀 Quick Start

1. Create your Gradio app:
```python
import gradio as gr

def process(input_text):
    return f"Processed: {input_text}"

demo = gr.Interface(
    fn=process,
    inputs="text",
    outputs="text"
)

if __name__ == "__main__":
    demo.launch()
```

2. Deploy to Hugging Face:
```bash
# Install huggingface_hub
pip install huggingface_hub

# Login (only needed once)
huggingface-cli login

# Create and push to Space
git init
git add .
git commit -m "Initial commit"
git push
```

3. Monitor your deployment:
- Check Space logs
- Monitor resource usage
- Set up alerts if needed

## 📝 License

This guide is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
