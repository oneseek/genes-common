import logging
from typing import Optional, Any
from pymongo import MongoClient
from pymongo.database import Database
from .config import settings

# 尝试导入 Redis，如果没有安装则设为 None
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    redis = None
    REDIS_AVAILABLE = False

# 尝试导入 MySQL 相关模块，如果没有安装则设为 None
try:
    import pymysql
    import sqlalchemy
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.pool import QueuePool
    MYSQL_AVAILABLE = True
except ImportError:
    pymysql = None
    sqlalchemy = None
    create_engine = None
    sessionmaker = None
    QueuePool = None
    MYSQL_AVAILABLE = False

logger = logging.getLogger(__name__)

# Global connection instances
_mongo_client: Optional[MongoClient] = None
_redis_client = None
_mysql_engine = None
_mysql_session_factory = None


def get_mongo_client() -> MongoClient:
    """Get MongoDB client instance."""
    global _mongo_client
    if _mongo_client is None:
        try:
            logger.info(f"Connecting to MongoDB: {settings.MONGODB_URI}")
            _mongo_client = MongoClient(settings.MONGODB_URI)
            # Test connection
            _mongo_client.admin.command('ping')
            logger.info("Connected to MongoDB successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    return _mongo_client


def get_mongo_db() -> Database:
    """Get MongoDB database instance."""
    client = get_mongo_client()
    return client[settings.database.mongodb_database]


def get_redis_client():
    """Get Redis client instance (if available)."""
    if not REDIS_AVAILABLE:
        raise ImportError("Redis is not installed. Install with: pip install redis")
    
    global _redis_client
    if _redis_client is None:
        try:
            _redis_client = redis.Redis(
                host=settings.database.redis_host,
                port=settings.database.redis_port,
                db=0,  # Default to DB 0
                decode_responses=True
            )
            # Test connection
            _redis_client.ping()
            logger.info("Connected to Redis successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    return _redis_client


def get_mysql_engine():
    """Get MySQL SQLAlchemy engine instance (if available)."""
    if not MYSQL_AVAILABLE:
        raise ImportError("MySQL dependencies are not installed. Install with: pip install pymysql sqlalchemy")
    
    global _mysql_engine
    if _mysql_engine is None:
        try:
            database_uri = settings.SQLALCHEMY_DATABASE_URI
            logger.info(f"Connecting to MySQL: {database_uri.replace(settings.database.mysql_password, '***')}")
            
            _mysql_engine = create_engine(
                database_uri,
                poolclass=QueuePool,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False  # Set to True for SQL query logging
            )
            
            # Test connection
            with _mysql_engine.connect() as connection:
                connection.execute(sqlalchemy.text("SELECT 1"))
            
            logger.info("Connected to MySQL successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MySQL: {e}")
            raise
    return _mysql_engine


def get_mysql_session():
    """Get MySQL SQLAlchemy session instance (if available)."""
    if not MYSQL_AVAILABLE:
        raise ImportError("MySQL dependencies are not installed. Install with: pip install pymysql sqlalchemy")
    
    global _mysql_session_factory
    if _mysql_session_factory is None:
        engine = get_mysql_engine()
        _mysql_session_factory = sessionmaker(bind=engine)
    
    return _mysql_session_factory()


def get_mysql_connection():
    """Get MySQL raw connection (if available)."""
    if not MYSQL_AVAILABLE:
        raise ImportError("MySQL dependencies are not installed. Install with: pip install pymysql sqlalchemy")
    
    engine = get_mysql_engine()
    return engine.connect()


def close_connections():
    """Close all database connections."""
    global _mongo_client, _redis_client, _mysql_engine, _mysql_session_factory
    
    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None
        logger.info("MongoDB connection closed")
    
    if _redis_client and REDIS_AVAILABLE:
        _redis_client.close()
        _redis_client = None
        logger.info("Redis connection closed")
    
    if _mysql_engine and MYSQL_AVAILABLE:
        _mysql_engine.dispose()
        _mysql_engine = None
        _mysql_session_factory = None
        logger.info("MySQL connections closed")
