# 🚀 Shorty - The Ultimate URL Shortener with QR Codes

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128+-green.svg)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Tired of sharing ugly, long URLs? Meet Shorty - your elegant solution for link management!** Shorty transforms cumbersome web addresses into sleek, shareable links while generating QR codes for instant mobile access. Perfect for marketers, developers, and anyone who values clean, professional communication.

---

## ✨ What Makes Shorty Amazing?

Imagine sharing a link that's not only short but also comes with a beautiful QR code ready for print, social media, or anywhere you need it. Shorty is more than just a URL shortener - it's a complete link management platform that tracks clicks, ensures security, and scales with your needs.

Whether you're running a marketing campaign, building a SaaS product, or just want to tidy up your social media posts, Shorty delivers professional-grade link shortening with enterprise-level reliability.

---

## 🎯 Key Features

### 🔗 **Smart URL Shortening**
- Generate unique 7-character short links instantly
- Automatic URL normalization and validation
- Intelligent duplicate detection (coming soon)

### 📱 **QR Code Generation**
- High-quality QR codes generated on-demand
- Downloadable PNG format
- Customizable styling options

### 📊 **Analytics & Tracking**
- Real-time click tracking
- Last accessed timestamps
- Comprehensive usage statistics

### 🛡️ **Security & Reliability**
- Rate limiting (5 requests/minute) to prevent abuse
- Input validation and sanitization
- Private network blocking for security
- Comprehensive error handling

### 🌐 **Modern Web Interface**
- Responsive design that works on all devices
- One-click copy functionality
- Toast notifications for user feedback
- Clean, intuitive user experience

### 🔧 **Developer-Friendly API**
- RESTful JSON API
- Rate-limited endpoints
- Comprehensive documentation (Swagger/ReDoc)
- Easy integration with existing applications

### 🐳 **Docker Ready**
- Containerized deployment
- Easy scaling and management
- Production-ready configurations

---

## 🛠 Quick Installation

### Docker (Recommended)
```bash
# Option 1: Pull the pre-built Docker image
docker pull pratham003/shorty:latest
docker run -p 8080:8080 --env-file .env pratham003/shorty:latest
```

```bash
# Option 2: Build and run with Docker Compose
# Clone the repository
git clone https://github.com/Prathamdas3/shorty
cd shorty

# Copy environment file
cp .env.example .env

# Edit .env with your settings
nano .env

# Run with Docker Compose
docker-compose up -d
```

That's it! Shorty will be running at `http://localhost:8080`.

### Manual Setup
```bash
# Install Python dependencies
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env file with your database URL and settings

# Run database migrations
uv run alembic upgrade head

# Start the application
uv run uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
```

---

## 🎮 How to Use Shorty

### Web Interface
1. **Visit the homepage** - Open your browser to Shorty's web interface
2. **Enter your URL** - Paste any long URL you want to shorten
3. **Get instant results** - Receive your short link and QR code immediately
4. **Copy or download** - Copy the link or download the QR code for your needs

The interface includes smart validation to ensure only safe, valid URLs are shortened.

### API Usage
Shorty provides a powerful REST API for programmatic access:

```bash
curl -X POST "http://localhost:8080/api/link" \
     -H "Content-Type: application/json" \
     -d '{"link": "https://www.example.com/very/long/url/that/needs/shortening"}'
```

Response:
```json
{
  "status": "success",
  "data": {
    "link": "http://localhost:8080/AbCdEfG",
    "qr": "iVBORw0KGgoAAAANSUhEUgAA..."
  },
  "message": "Successfully generated the link"
}
```

---

## 📡 API Reference

### POST `/api/link`
Generate a new short link and QR code.

**Request Body:**
```json
{
  "link": "https://example.com/your-long-url"
}
```

**Rate Limit:** 5 requests per minute per IP

**Response (200):**
```json
{
  "status": "success",
  "data": {
    "link": "http://your-domain.com/short-id",
    "qr": "base64-encoded-png"
  },
  "message": "Successfully generated the link"
}
```

**Error Responses:**
- `400` - Invalid URL format
- `429` - Rate limit exceeded
- `500` - Server error

### GET `/{short_id}`
Redirect to the original URL (automatic redirect).

---

## 🧪 Development

### Local Development Setup
```bash
# Install dependencies (including dev dependencies)
uv sync

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html

# Lint code
uv run ruff check .

# Format code
uv run ruff format .
```

### Project Structure
```
shorty/
├── app/
│   ├── api/          # API routes and routers
│   ├── core/         # Configuration, logging, templates
│   ├── db/           # Database models and initialization
│   ├── models/       # Pydantic models
│   ├── services/     # Business logic (links, QR codes)
│   └── web/          # Web routes and handlers
├── tests/            # Comprehensive test suite
├── alembic/          # Database migrations
└── docker-compose.yml
```

### Environment Variables
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/shorty
ENV=development
FRONTEND_URL=http://localhost:8080
SITE_URL=http://localhost:8080
SITE_DESCRIPTION=Shorty is a free URL shortener with QR code generation
```

---

## 🤝 Contributing

We love contributions! Here's how you can help make Shorty even better:

1. **Fork the repository** at https://github.com/Prathamdas3/shorty
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Write tests** for your changes
4. **Ensure all tests pass** (`pytest`)
5. **Submit a pull request** with a clear description

### Development Guidelines
- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation for API changes
- Ensure Docker compatibility

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Ready to shorten your first link?** 🚀 Get started with Shorty today and experience the future of URL management!</content>
<parameter name="filePath">README.md