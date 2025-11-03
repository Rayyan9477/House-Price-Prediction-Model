# House Price Prediction CI/CD Pipeline

[![Code Quality](https://github.com/Rayyan9477/House-Price-Prediction-Model/actions/workflows/code-quality.yml/badge.svg)](https://github.com/Rayyan9477/House-Price-Prediction-Model/actions/workflows/code-quality.yml)
[![Testing](https://github.com/Rayyan9477/House-Price-Prediction-Model/actions/workflows/testing.yml/badge.svg)](https://github.com/Rayyan9477/House-Price-Prediction-Model/actions/workflows/testing.yml)
[![Deploy](https://github.com/Rayyan9477/House-Price-Prediction-Model/actions/workflows/deploy.yml/badge.svg)](https://github.com/Rayyan9477/House-Price-Prediction-Model/actions/workflows/deploy.yml)

## Table of Contents
- [Introduction](#introduction)
- [CI/CD Pipeline Overview](#cicd-pipeline-overview)
- [Branch Strategy](#branch-strategy)
- [Workflows](#workflows)
- [Application Features](#application-features)
- [Installation](#installation)
- [Usage](#usage)
- [Docker Deployment](#docker-deployment)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [Contact](#contact)

## Introduction
This project is a machine learning-powered web application that predicts house prices using a RandomForest regression model. The application is built with Streamlit for an interactive user interface. The project implements a comprehensive CI/CD pipeline using GitHub Actions, ensuring code quality, automated testing, and seamless deployment to Docker Hub.

## CI/CD Pipeline Overview

### Pipeline Architecture
The CI/CD pipeline follows a three-branch strategy with automated workflows:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│     dev     │───▶│    test     │───▶│    main     │───▶│ Docker Hub  │
│             │    │             │    │             │    │             │
│ Code Quality│    │ Unit Testing│    │ Deployment  │    │ Container   │
│ Check       │    │ Coverage    │    │ Email Alert │    │ Registry    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## Branch Strategy

### 1. Development Branch (`dev`)
- **Purpose**: Feature development and initial code validation
- **Triggers**: 
  - Code quality checks with flake8
  - Security scanning with bandit
  - PEP 8 compliance verification
- **Protection**: Requires admin approval for merges

### 2. Test Branch (`test`)
- **Purpose**: Comprehensive testing and validation
- **Triggers**:
  - Automated unit tests
  - Integration tests
  - Code coverage analysis
- **Protection**: Requires successful test completion

### 3. Main Branch (`main`)
- **Purpose**: Production-ready code
- **Triggers**:
  - Docker image build and push to Docker Hub
  - Email notifications to administrators
  - Security scanning of container images

## Workflows

### 1. Code Quality Workflow (`.github/workflows/code-quality.yml`)
**Trigger**: Push to `dev` branch or PR to `dev`

**Features**:
- Python syntax validation
- flake8 linting with PEP 8 compliance
- Security vulnerability scanning with bandit
- Code complexity analysis

### 2. Testing Workflow (`.github/workflows/testing.yml`)
**Trigger**: Push to `test` branch or PR to `test`

**Features**:
- Comprehensive unit test execution
- Code coverage reporting
- Model validation testing
- Streamlit application startup testing

### 3. Deployment Workflow (`.github/workflows/deploy.yml`)
**Trigger**: Push to `main` branch or merged PR to `main`

**Features**:
- Docker image building and optimization
- Multi-tag versioning (latest, branch, SHA)
- Push to Docker Hub registry
- Container security scanning
- Email notifications to administrators

## Application Features

The Streamlit application provides an interactive web interface for house price prediction:

### User Interface
- **Property Type Selection**: Choose from House, Flat, Penthouse, or Studio
- **Location Input**: Text input for specific location (e.g., G-10, DHA Defence)
- **City Selection**: Dropdown for major cities (Islamabad, Rawalpindi, Lahore, Karachi)
- **Numeric Inputs**: Bedrooms, Bathrooms, and Area in Marla
- **Purpose Selection**: For Sale or For Rent

### Prediction Features
- **Real-time Prediction**: Instant price prediction using the trained ML model
- **Model Information**: Display of the current model type and accuracy
- **Model Retraining**: Button to retrain the model with fresh data

### Model Details
- **Algorithm**: RandomForest Regressor (best performing model)
- **Accuracy**: R2 score displayed for transparency
- **Features**: 7 input features for comprehensive prediction

## Installation

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Rayyan9477/House-Price-Prediction-Model.git
   cd House-Price-Prediction-Model
   ```

2. **Switch to development branch**:
   ```bash
   git checkout dev
   ```

3. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

   The application will be available at `http://localhost:8501`

### Testing Setup

1. **Run unit tests**:
   ```bash
   pytest tests/ -v
   ```

2. **Run tests with coverage**:
   ```bash
   pytest tests/ --cov=app --cov-report=html
   ```

## Docker Deployment

### Building Docker Image

```bash
docker build -t house-price-prediction .
```

### Running Container

```bash
docker run -p 8501:8501 house-price-prediction
```

### Using Docker Compose (Optional)

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
```

Run with:
```bash
docker-compose up
```

## Dependencies

### Core Dependencies
- **Streamlit 1.28.0**: Web framework for interactive applications
- **pandas 2.0.3**: Data manipulation and analysis
- **numpy 1.24.3**: Numerical computing
- **scikit-learn 1.3.0**: Machine learning algorithms

### Development Dependencies
- **pytest 7.4.0**: Testing framework
- **flake8 6.0.0**: Code linting and style checking
- **pytest-cov**: Code coverage reporting

## Contributing

### Development Workflow

1. **Fork the repository**
2. **Create feature branch from `dev`**:
   ```bash
   git checkout dev
   git checkout -b feature/your-feature-name
   ```

3. **Make changes and commit**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

4. **Push changes**:
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request to `dev` branch**

### Pull Request Process

1. **dev → test**: Feature completion, triggers testing workflow
2. **test → master**: Testing success, triggers deployment workflow
3. **Admin approval required** for all merges

### Code Standards

- Follow PEP 8 style guidelines
- Maintain code coverage above 80%
- Add unit tests for new features
- Update documentation for API changes

## Required GitHub Secrets

Configure the following secrets in your GitHub repository:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `DOCKER_HUB_USERNAME` | Docker Hub username | `rayyan9477` |
| `DOCKER_HUB_ACCESS_TOKEN` | Docker Hub access token | `dckr_pat_...` |
| `EMAIL_USERNAME` | SMTP email username | `your-email@gmail.com` |
| `EMAIL_PASSWORD` | SMTP email app password | `app-specific-password` |

## Project Structure

```
House-Price-Prediction-Model/
├── .github/
│   └── workflows/
│       ├── code-quality.yml
│       ├── testing.yml
│       └── deploy.yml
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── app.py                 # Streamlit application
├── House_dataset.csv      # Training dataset
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── .dockerignore         # Docker ignore rules
├── Readme.md            # Project documentation
└── LICENSE              # License file
```

## Video Demonstration

Watch the video demonstration of the project:

![House Price Prediction Demo](https://github.com/Rayyan9477/House-Price-Prediction-Model/blob/main/video.mp4)

Click the link to watch demo.

## Contact

- **Email**: rayyanahmed265@yahoo.com
- **GitHub**: [Rayyan9477](https://github.com/Rayyan9477)
- **LinkedIn**: [Rayyan Ahmed](https://www.linkedin.com/in/rayyan-ahmed9477/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
