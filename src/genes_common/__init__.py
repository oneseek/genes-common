"""
Genes Common Module

Common shared modules for the genes project including:
- Configuration management
- Database connections
- Logging utilities
"""

__version__ = "1.0.0"

from .config import Settings, settings
from .db import (
    get_mongo_client, get_mongo_db, 
    get_redis_client, 
    get_mysql_engine, get_mysql_session, get_mysql_connection,
    close_connections
)
from .logging import setup_logging
from .aliyun_oss import OSSClient

__all__ = [
    "Settings",
    "settings", 
    "get_mongo_client",
    "get_mongo_db",
    "get_redis_client",
    "get_mysql_engine",
    "get_mysql_session", 
    "get_mysql_connection",
    "close_connections",
    "setup_logging",
    "OSSClient",
] 