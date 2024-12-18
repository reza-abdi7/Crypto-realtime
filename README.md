# Crypto Real-time Analytics Platform

> **Disclaimer**: This is a portfolio project showcasing an end-to-end ML system in production. The implemented trading strategies and analysis should not be used for actual trading decisions. This project serves as a demonstration of architectural design and implementation of production-ready ML services.

## Project Overview

This project demonstrates the implementation of a real-time cryptocurrency analytics system that combines market data, news sentiment, and technical analysis to showcase a production-grade machine learning system. The platform processes real-time cryptocurrency data through various microservices, implementing modern software engineering practices and MLOps principles.

## Architecture

The system is built using a microservices architecture with the following key components:

### Core Services
- **Trades Service**: Processes real-time trade data from cryptocurrency exchanges
- **Candles Service**: Aggregates trade data into OHLCV candles
- **News Service**: Collects and processes cryptocurrency-related news
- **Sentiment Analysis**: Analyzes news sentiment using LLM
- **Technical Analysis**: Computes various technical indicators
- **Feature Store**: Centralizes feature management for ML models

### Key Technologies
- **Python**: Primary programming language
- **Docker**: Containerization and deployment
- **Docker Compose**: Simplified local development
- **quixstreams(Kafka)**: Real-time data streaming
- **Pydantic**: Data validation and settings management

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.9+
- Git
- uv (Python package installer)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/reza-abdi7/crypto-realtime.git
cd crypto-realtime
```

2. Start the services:
```bash
docker-compose up -d
```

## Project Structure

```
crypto-realtime/
├── Services/
│   ├── trades/          # Real-time trade data processing
│   ├── candles/         # OHLCV candle aggregation
│   ├── news/            # News data collection
│   ├── sentiment/       # Sentiment analysis
│   ├── ta/              # Technical analysis
│   └── to-feature-store/# Feature management
├── docker-compose/      # Docker deployment configs
└── README.md
```

## Development

### Code Quality
- Pre-commit hooks for code formatting and linting
- Type hints and docstrings
- Pydantic models for robust data validation


## Features

- Real-time trade data processing
- Technical indicator calculation
- News sentiment analysis
- Feature engineering pipeline
- Model training and deployment
- Real-time predictions
- API endpoints for data access

## Contributing

This is a portfolio project, but suggestions and improvements are welcome:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request


## Disclaimer

This project is for educational and demonstration purposes only. The implemented strategies, analysis, and predictions should not be used for actual trading decisions. Always conduct your own research and consult with financial advisors before making any investment decisions.
