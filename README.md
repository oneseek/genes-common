# Genes Common

Common shared modules for the genes project ecosystem.

## Overview

This package provides common functionality that can be shared across multiple genes projects, including:

- **Configuration Management**: Centralized configuration handling with environment variable support
- **Database Connections**: MongoDB connection utilities
- **Logging**: Standardized logging setup and configuration

## Installation

### Basic installation
```bash
pip install -e .
```

### With specific database clients
The package automatically detects available database clients. All database clients are included by default, but you can install only what you need:

```bash
# For MongoDB only
pip install -e . pymongo

# For Redis only  
pip install -e . redis

# For MySQL only
pip install -e . pymysql sqlalchemy

# For all databases (default)
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
from genes_common import (
    get_mongo_client, get_mongo_db, 
    get_redis_client, 
    get_mysql_engine, get_mysql_session, get_mysql_connection,
    close_connections
)

# MongoDB
client = get_mongo_client()
db = get_mongo_db()

# Redis (if redis is installed)
redis_client = get_redis_client()

# MySQL (if pymysql and sqlalchemy are installed)
# SQLAlchemy engine for connection pooling
engine = get_mysql_engine()

# SQLAlchemy session for ORM operations
session = get_mysql_session()

# Raw MySQL connection for direct SQL operations
connection = get_mysql_connection()

# Close all connections (useful in application shutdown)
close_connections()
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
- `REDIS_HOST`: Redis host (default: redis)
- `REDIS_PORT`: Redis port (default: 6379)
- `MYSQL_HOST`: MySQL host (default: mysql)
- `MYSQL_PORT`: MySQL port (default: 3306)
- `MYSQL_USER`: MySQL username
- `MYSQL_PASSWORD`: MySQL password
- `MYSQL_DATABASE`: MySQL database name

### Application
- `APP_NAME`: Application name
- `ENVIRONMENT`: Environment (development/production)
- `DEBUG`: Debug mode (True/False)
- `SECRET_KEY`: Application secret key

### Security
- `API_TOKEN`: API access token
- `JWT_SECRET_KEY`: JWT signing secret key
- `JWT_ALGORITHM`: JWT algorithm (default: HS256)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration in minutes (default: 30)
- `REQUIRE_API_TOKEN`: Whether to require API token validation in production (default: true)
- `ADMIN_USERNAME`: Admin username for dashboard
- `ADMIN_PASSWORD`: Admin password for dashboard
- `ADMIN_EMAIL`: Admin email for dashboard

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