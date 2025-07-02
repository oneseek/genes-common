"""
Genes Common Module

Common shared modules for the genes project including:
- Configuration management
- Database connections
- Logging utilities
"""

__version__ = "1.0.0"

from .config import Settings, settings
from .db import get_mongo_client, get_mongo_db
from .logging import setup_logging

__all__ = [
    "Settings",
    "settings", 
    "get_mongo_client",
    "get_mongo_db",
    "setup_logging",
] 