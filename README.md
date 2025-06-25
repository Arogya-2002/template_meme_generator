# 🎭 Emotion-Based Meme Generator API

A FastAPI-powered intelligent meme generator that detects emotions from facial expressions and creates contextual memes with multilingual support.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

- **Intelligent Face Detection**: Uses MTCNN for accurate face detection in images
- **Emotion Classification**: Leverages Vision Transformer (ViT) for precise emotion recognition
- **Dynamic Meme Generation**: Creates contextual memes based on detected emotions
- **Multilingual Support**: Generates captions in Telugu and English
- **RESTful API**: Easy-to-use FastAPI endpoints with automatic documentation
- **File Upload Support**: Accepts JPG and PNG image formats

## 🏗️ Architecture

### Core Technologies
- **Face Detection**: `facenet-pytorch` (MTCNN)
- **Emotion Classification**: `trpakov/vit-face-expression` (Vision Transformer)
- **Image Processing**: Pillow with custom Telugu font support
- **Backend Framework**: FastAPI with async support

### Supported Emotions
The model can detect and generate memes for the following emotions:
- Happy 😊
- Sad 😢
- Angry 😠
- Surprised 😲
- Fear 😨
- Disgust 🤢
- Neutral 😐

## 📂 Project Structure

```
meme-generator-api/
├── app.py                          # FastAPI application entry point
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── fonts/                          # Font assets
│   └── NotoSansTelugu-Regular.ttf  # Telugu font file
├── artifacts/                      # Generated artifacts
│   └── data/                       # Cached images and temp files
├── logs/                           # Application logs
└── src/                            # Source code
    ├── components/                 # Core components
    │   ├── classify_emotion.py     # Emotion classification logic
    │   ├── detect_face.py          # Face detection implementation
    │   └── meme_generator.py       # Meme generation utilities
    ├── pipeline/                   # Processing pipelines
    │   ├── emotion_pipeline.py     # End-to-end emotion processing
    │   └── template_meme_pipeline.py # Meme template processing
    ├── entity/                     # Data models and configurations
    │   ├── artifact.py             # Artifact definitions
    │   └── config.py               # Configuration models
    ├── constants/                  # Global constants
    ├── exceptions/                 # Custom exception classes
    ├── logger/                     # Logging configuration
    └── utils/                      # Helper utilities
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/meme-generator-api.git
   cd meme-generator-api
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app:app --reload
   ```

5. **Access the API**
   - **API Base URL**: http://127.0.0.1:8000
   - **Interactive Documentation**: http://127.0.0.1:8000/docs
   - **Alternative Docs**: http://127.0.0.1:8000/redoc

## 📡 API Reference

### Generate Meme Endpoint

**Endpoint**: `POST /generate-meme/`

**Description**: Upload an image to detect emotions and generate a contextual meme.

**Request Format**:
- **Content-Type**: `multipart/form-data`
- **Parameter**: `image` (file) - JPG or PNG image file

**Response**: 
- **Content-Type**: `image/png`
- **Body**: Generated meme image as downloadable file

**Example Usage**:

```bash
# Using cURL
curl -X POST "http://127.0.0.1:8000/generate-meme/" \
  -F "image=@path/to/your/image.jpg" \
  --output generated_meme.png

# Using Python requests
import requests

with open('your_image.jpg', 'rb') as f:
    response = requests.post(
        'http://127.0.0.1:8000/generate-meme/',
        files={'image': f}
    )
    
with open('generated_meme.png', 'wb') as f:
    f.write(response.content)
```

**Status Codes**:
- `200`: Meme generated successfully
- `400`: Invalid image format or processing error
- `422`: Validation error
- `500`: Internal server error

## 🛠️ Configuration

### Font Configuration
The application uses `NotoSansTelugu-Regular.ttf` for Telugu text rendering. Ensure the font file is present in the `fonts/` directory for proper multilingual support.

### Environment Variables
Create a `.env` file for configuration:
```env
# API Configuration
HOST=127.0.0.1
PORT=8000
DEBUG=True

# Model Configuration
EMOTION_MODEL=trpakov/vit-face-expression
CONFIDENCE_THRESHOLD=0.5

# File Configuration
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=jpg,jpeg,png
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v
```

For coverage report:
```bash
pytest --cov=src tests/
```

## 🐳 Docker Deployment

Build and run with Docker:
```bash
# Build image
docker build -t meme-generator-api .

# Run container
docker run -p 8000:8000 meme-generator-api
```

## 🔮 Roadmap

- [ ] **Enhanced Multilingual Support**: Add support for more Indian languages
- [ ] **Web Interface**: React-based frontend with drag-and-drop functionality
- [ ] **Template System**: Predefined meme templates categorized by emotion
- [ ] **Batch Processing**: Support for multiple image processing
- [ ] **Cloud Storage**: Integration with AWS S3/Google Cloud Storage
- [ ] **Performance Optimization**: Caching and async processing improvements
- [ ] **Mobile App**: React Native companion app
- [ ] **Social Sharing**: Direct integration with social media platforms

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face** for the pre-trained Vision Transformer model
- **facenet-pytorch** team for the MTCNN implementation
- **FastAPI** community for the excellent framework
- Inspired by modular ML project architectures

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/meme-generator-api/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/meme-generator-api/discussions)
- **Email**: your-email@example.com

---

<div align="center">
  <strong>Built with ❤️ for the meme community</strong>
</div>