# Genes Common

Common shared modules for the genes project ecosystem.

## Overview

This package provides common functionality that can be shared across multiple genes projects, including:

- **Configuration Management**: Centralized configuration handling with environment variable support
- **Database Connections**: MongoDB connection utilities
- **Logging**: Standardized logging setup and configuration

## Installation

```bash
pip install -e .
```

## Usage

### Configuration

```python
from genes_common import settings

# Access database URI
print(settings.MONGODB_URI)

# Access API configuration
print(settings.API_TOKEN)
```

### Database

```python
from genes_common import get_mongo_client, get_mongo_db

# Get MongoDB client
client = get_mongo_client()

# Get database instance
db = get_mongo_db()
```

### Logging

```python
from genes_common import setup_logging

# Setup logger for your module
logger = setup_logging(__name__)
logger.info("Application started")
```

## Environment Variables

The following environment variables can be configured:

### Database
- `MONGODB_HOST`: MongoDB host (default: mongodb)
- `MONGODB_PORT`: MongoDB port (default: 27017)
- `MONGODB_USER`: MongoDB username
- `MONGODB_PASSWORD`: MongoDB password
- `MONGODB_DATABASE`: MongoDB database name
- `MONGODB_URI`: Complete MongoDB URI (overrides individual settings)

### Application
- `APP_NAME`: Application name
- `ENVIRONMENT`: Environment (development/production)
- `DEBUG`: Debug mode (True/False)
- `SECRET_KEY`: Application secret key

### Logging
- `LOG_LEVEL`: Logging level (default: INFO)
- `LOG_FILE`: Log file path
- `LOG_DIR`: Log directory path

## Development

1. Clone the repository
2. Install in development mode: `pip install -e .`
3. Run tests: `pytest`

## License

[Your License Here] 