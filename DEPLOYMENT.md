# Valor AI - Deployment Guide

Complete deployment guide for Valor AI Mango Analysis system.

## 🎯 Overview

Valor AI is designed for dual deployment:
- **Web API**: FastAPI backend for web/mobile clients
- **Mobile Apps**: Offline-capable Android/iOS applications

## 📋 Prerequisites

### System Requirements
- Python 3.9+
- 2GB RAM minimum (4GB recommended)
- Internet connection (for online mode with OpenAI)

### API Keys
- OpenAI API key (for online analysis)
- Optional: Offline models (for no-internet scenarios)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/your-org/valor-fruit-classifier.git
cd valor-fruit-classifier

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your OpenAI API key
# Windows: notepad .env
# Linux/Mac: nano .env
```

**Required `.env` configuration:**
```bash
OPENAI_API_KEY=your_actual_openai_api_key_here
USE_OFFLINE_MODE=false
DEFAULT_LANGUAGE=en
```

### 3. Run Development Server

```bash
# Using the new v2 API
uvicorn app.main_v2:app --reload --host 0.0.0.0 --port 8000
```

Access the API:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📱 Deployment Options

### Option 1: Web API (FastAPI)

#### Local Development
```bash
uvicorn app.main_v2:app --reload
```

#### Production with Gunicorn
```bash
pip install gunicorn

gunicorn app.main_v2:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

#### Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/
COPY .env .env

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main_v2:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and run:**
```bash
# Build image
docker build -t valor-ai:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  --name valor-api \
  valor-ai:latest
```

#### Cloud Deployment (Render/Railway/Fly.io)

**render.yaml:**
```yaml
services:
  - type: web
    name: valor-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main_v2:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: OPENAI_API_KEY
        sync: false
      - key: USE_OFFLINE_MODE
        value: false
```

Deploy to Render:
```bash
# Connect GitHub repo and Render will auto-deploy
# Or use Render CLI:
render deploy
```

### Option 2: Mobile Deployment (Offline Mode)

For farmers with limited internet access, deploy offline models on mobile devices.

#### Strategy for Offline Mode

1. **Convert to TensorFlow Lite**
   - Quantize models for smaller size
   - Optimize for mobile CPUs
   - Target: <50MB total app size

2. **Model Hosting Options**
   - **On-device**: Bundle models in APK/IPA
   - **Download on first launch**: Fetch from CDN
   - **Hybrid**: Critical models on-device, others download

#### TensorFlow Lite Conversion (Coming Soon)

```python
# Example conversion script
import tensorflow as tf

# Load trained model
model = tf.keras.models.load_model('models/ripeness_classifier.h5')

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

# Save
with open('models/ripeness_classifier.tflite', 'wb') as f:
    f.write(tflite_model)
```

## 🌍 Multi-Language Support

Valor supports 4 languages out of the box:

| Language | Code | Target Users |
|----------|------|--------------|
| English | `en` | Urban consumers, international |
| Yoruba | `yo` | Southwest Nigeria farmers |
| Igbo | `ig` | Southeast Nigeria vendors |
| Hausa | `ha` | Northern Nigeria farmers |

**Usage in API:**
```bash
curl -X POST "http://localhost:8000/analyze/full" \
  -F "file=@mango.jpg" \
  -F "language=yo"
```

**Response will be localized:**
```json
{
  "recommendation": {
    "action": "buy",
    "message": "O dara lati ra",  // Yoruba: "Good to buy"
    "reason": "Perfect ripeness for consumption"
  }
}
```

## 📊 API Endpoints

### Core Endpoints

| Endpoint | Method | Description | Use Case |
|----------|--------|-------------|----------|
| `/` | GET | Welcome & API info | Quick health check |
| `/health` | GET | System status | Monitoring |
| `/analyze/full` | POST | Complete analysis | Primary endpoint |
| `/analyze/classify` | POST | Fruit classification only | Pre-screening |
| `/analyze/ripeness` | POST | Ripeness only | Purchase decisions |
| `/analyze/disease` | POST | Disease only | Farm management |

### Example Requests

#### Full Analysis
```bash
curl -X POST "http://localhost:8000/analyze/full" \
  -H "accept: application/json" \
  -F "file=@mango.jpg" \
  -F "language=en"
```

**Response:**
```json
{
  "language": "en",
  "analysis_mode": "online",
  "fruit_classification": {
    "is_mango": true,
    "variety": "Kent",
    "confidence": 95,
    "notes": "Large yellow mango"
  },
  "ripeness": {
    "ripeness_stage": "ripe",
    "confidence": 90,
    "color_description": "Yellow with red blush",
    "recommendation": "Perfect for eating",
    "days_to_optimal": 0
  },
  "disease": {
    "is_diseased": false,
    "diseases_detected": [],
    "confidence": 88,
    "severity": null
  },
  "recommendation": {
    "action": "buy",
    "message": "Good to buy",
    "reason": "Perfect ripeness for consumption"
  }
}
```

## 🔒 Security Best Practices

### Production Checklist

- [ ] Never commit `.env` files (add to `.gitignore`)
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS (use Nginx reverse proxy or Cloudflare)
- [ ] Rate limit API endpoints (prevent abuse)
- [ ] Implement authentication (JWT/API keys) for production
- [ ] Monitor OpenAI API usage to prevent cost overruns
- [ ] Set up logging and error tracking (Sentry)

### Rate Limiting (Optional)

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/analyze/full")
@limiter.limit("10/minute")  # 10 requests per minute per IP
async def analyze_full(...):
    ...
```

## 💰 Cost Considerations

### OpenAI API Costs (GPT-4 Vision)

- **Model**: GPT-4o (recommended for vision tasks)
- **Cost**: ~$0.01 per analysis (varies by image detail)
- **Monthly estimates**:
  - 100 analyses/day: ~$30/month
  - 500 analyses/day: ~$150/month
  - 1000 analyses/day: ~$300/month

### Cost Optimization Strategies

1. **Cache responses**: Store results for identical images
2. **Use offline mode**: Deploy TFLite models for free inference
3. **Hybrid approach**:
   - Online for vendors/consumers (can afford)
   - Offline for farmers (limited budget)
4. **Batch processing**: Queue multiple analyses
5. **Image optimization**: Compress/resize before sending to API

## 📈 Monitoring & Analytics

### Key Metrics to Track

1. **Usage Metrics**
   - Total analyses per day/month
   - Analysis type breakdown (classify/ripeness/disease)
   - Language distribution
   - Response times

2. **Accuracy Metrics**
   - Confidence score distributions
   - User feedback (thumbs up/down)
   - Manual validation sampling

3. **Business Metrics**
   - User personas breakdown (farmer/vendor/consumer)
   - Geographic distribution (states in Nigeria)
   - Offline vs online mode usage

### Logging Setup

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('valor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Log each analysis
logger.info(f"Analysis: user_id={user_id}, language={lang}, is_mango={result}")
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. OpenAI API Key Not Working
```bash
# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"

# If invalid, generate new key at platform.openai.com
```

#### 2. Module Not Found Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check installed packages
pip list | grep openai
```

#### 3. Slow Response Times
- **Cause**: High-resolution images sent to OpenAI
- **Solution**: Resize images before analysis

```python
# Add to preprocessing
def optimize_image(image: Image.Image, max_size=1024):
    if max(image.size) > max_size:
        image.thumbnail((max_size, max_size), Image.LANCZOS)
    return image
```

#### 4. Out of Memory (Mobile)
- Use quantized TFLite models (8-bit instead of 32-bit)
- Reduce image resolution to 224x224 or 128x128
- Unload models after inference

## 🔄 Update & Maintenance

### Updating the API

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Restart service
# Docker:
docker restart valor-api

# Systemd:
sudo systemctl restart valor

# PM2 (Node process manager):
pm2 restart valor-api
```

### Database for Logging (Optional)

For production, consider adding SQLite/PostgreSQL:

```sql
CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    user_id VARCHAR(100),
    language VARCHAR(2),
    is_mango BOOLEAN,
    ripeness VARCHAR(20),
    disease_detected BOOLEAN,
    confidence FLOAT,
    user_feedback INT  -- 1 for helpful, -1 for not helpful
);
```

## 📞 Support & Contact

- **Issues**: GitHub Issues
- **Email**: support@valor-ai.ng
- **WhatsApp**: +234-XXX-XXX-XXXX (for farmers)
- **Documentation**: https://docs.valor-ai.ng

## 🎯 Roadmap

### MVP (Current)
- [x] OpenAI Vision API integration
- [x] Multi-language support (4 languages)
- [x] FastAPI with comprehensive docs
- [ ] Offline model implementation

### Phase 2
- [ ] Mobile app (React Native/Flutter)
- [ ] TFLite models for offline use
- [ ] User authentication & history
- [ ] Feedback & rating system

### Phase 3
- [ ] NGO partnerships & farmer training
- [ ] Advanced analytics dashboard
- [ ] Treatment marketplace integration
- [ ] Voice-based interface (for low-literacy farmers)

---

**Built with ❤️ for Nigerian farmers, vendors, and consumers.**

**Target**: Reduce mango waste by 20% in 6 months | ≥85% accuracy across models
