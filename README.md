# Valor AI: Produce Quality Analysis System

AI-powered quality assessment for fruits and vegetables using computer vision.

## Overview

Valor AI provides automated analysis of produce quality through image recognition, helping farmers, vendors, and consumers make informed decisions about fruit and vegetable freshness, ripeness, and health.

### Core Features

- Fruit and vegetable identification
- Ripeness stage classification (underripe, ripe, overripe, spoiled)
- Disease and defect detection
- Multi-language support (English, Yoruba, Igbo, Hausa)
- RESTful API with comprehensive documentation

### Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | FastAPI |
| AI Engine | OpenAI GPT-4 Vision |
| Image Processing | Pillow |
| Configuration | Pydantic Settings |
| Server | Uvicorn |

## Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/fruit-classifier.git
cd fruit-classifier

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_openai_api_key_here
USE_OFFLINE_MODE=false
DEFAULT_LANGUAGE=en
```

### Running the API

```bash
# Development mode
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs for interactive API documentation.

## API Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/analyze/full` | POST | Complete analysis (classification + ripeness + disease) |
| `/analyze/classify` | POST | Produce identification only |
| `/analyze/ripeness` | POST | Ripeness assessment only |
| `/analyze/disease` | POST | Disease detection only |

### Usage Examples

#### Complete Analysis

```bash
curl -X POST "http://localhost:8000/analyze/full" \
  -F "file=@produce.jpg" \
  -F "language=en"
```

#### Python Client

```python
import requests

url = "http://localhost:8000/analyze/full"
files = {"file": open("produce.jpg", "rb")}
data = {"language": "en"}

response = requests.post(url, files=files, data=data)
result = response.json()

print(f"Type: {result['fruit_classification']['fruit_type']}")
print(f"Ripeness: {result['ripeness']['ripeness_stage']}")
print(f"Diseased: {result['disease']['is_diseased']}")
```

#### JavaScript/Frontend

```javascript
const formData = new FormData();
formData.append('file', imageFile);
formData.append('language', 'en');

fetch('http://localhost:8000/analyze/full', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => console.log(data));
```

## Multi-Language Support

The API supports four languages:

| Code | Language | Target Users |
|------|----------|--------------|
| `en` | English | International users |
| `yo` | Yoruba | Southwest Nigeria |
| `ig` | Igbo | Southeast Nigeria |
| `ha` | Hausa | Northern Nigeria |

Example with language parameter:

```bash
curl -X POST "http://localhost:8000/analyze/full" \
  -F "file=@produce.jpg" \
  -F "language=yo"
```

## Response Format

### Full Analysis Response

```json
{
  "language": "en",
  "analysis_mode": "online",
  "fruit_classification": {
    "fruit_type": "mango",
    "variety": "Kent",
    "confidence": 95,
    "notes": "Large yellow fruit"
  },
  "ripeness": {
    "ripeness_stage": "ripe",
    "confidence": 90,
    "color_description": "Yellow with red blush",
    "recommendation": "Ready to eat",
    "days_to_optimal": null
  },
  "disease": {
    "is_diseased": false,
    "diseases_detected": [],
    "confidence": 88,
    "severity": "low"
  },
  "recommendation": {
    "action": "buy",
    "message": "Good to buy",
    "reason": "Perfect ripeness for consumption"
  }
}
```

## Project Structure

```
fruit-classifier/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── ai_service.py     # AI analysis logic
│   ├── config.py         # Settings and translations
│   ├── schemas.py        # Data models
│   └── utils.py          # Utilities
├── models/               # Model files (for offline mode)
├── .env                  # Configuration (do not commit)
├── requirements.txt      # Dependencies
├── DEPLOYMENT.md         # Deployment guide
└── README.md             # This file
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | OpenAI API key |
| `USE_OFFLINE_MODE` | `false` | Enable offline inference |
| `DEFAULT_LANGUAGE` | `en` | Default response language |
| `API_HOST` | `0.0.0.0` | Server host |
| `API_PORT` | `8000` | Server port |

### Costs

Using OpenAI GPT-4 Vision:
- Approximately $0.01 per analysis
- 100 analyses/day = approximately $30/month
- 1000 analyses/day = approximately $300/month

Consider implementing offline mode for high-volume usage.

## Performance Targets

| Metric | Target |
|--------|--------|
| Accuracy | 85 percent or higher |
| Response Time | Under 5 seconds |
| Uptime | 99.9 percent |
| Concurrent Users | 100 or more |

## Security

- API keys stored in environment variables
- No personal data collected
- Images processed in-memory only
- HTTPS enforced in production
- Rate limiting recommended

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
uvicorn app.main:app --port 8001
```

**OpenAI API errors:**
- Verify API key is correct
- Check account has credits
- Review OpenAI status page

**Image upload fails:**
- Ensure file is JPEG or PNG
- Check file size (max 10MB recommended)
- Verify image is not corrupted

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit pull request

## License

MIT License - see LICENSE file for details

## Support

- Documentation: http://localhost:8000/docs
- Issues: GitHub Issues
- Email: support@valor-ai.ng

## Roadmap

### Current (v2.0)
- OpenAI Vision API integration
- Multi-language support
- RESTful API with documentation

### Planned (v2.1)
- Offline TensorFlow Lite models
- User authentication
- Analysis history
- Batch processing

### Future (v3.0)
- Mobile applications (iOS/Android)
- Advanced analytics dashboard
- Custom model training
- Voice interface support

## Acknowledgments

- OpenAI for GPT-4 Vision API
- FastAPI framework
- Nigerian agricultural community for domain expertise

---

Built for agricultural quality control and food safety assessment.
