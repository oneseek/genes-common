import os
from typing import Any, Dict, Optional
from datetime import timedelta
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class DatabaseConfig:
    """数据库配置"""
    # MySQL settings
    mysql_host: str = field(default_factory=lambda: os.getenv("MYSQL_HOST", "mysql"))
    mysql_port: int = field(default_factory=lambda: int(os.getenv("MYSQL_PORT", "3306")))
    mysql_user: str = field(default_factory=lambda: os.getenv("MYSQL_USER", "gene_user"))
    mysql_password: str = field(default_factory=lambda: os.getenv("MYSQL_PASSWORD", "gene_password"))
    mysql_database: str = field(default_factory=lambda: os.getenv("MYSQL_DATABASE", "gene_db"))
    
    # MongoDB settings
    mongodb_host: str = field(default_factory=lambda: os.getenv("MONGODB_HOST", "mongodb"))
    mongodb_port: int = field(default_factory=lambda: int(os.getenv("MONGODB_PORT", "27017")))
    mongodb_user: str = field(default_factory=lambda: os.getenv("MONGODB_USER", "gene_user"))
    mongodb_password: str = field(default_factory=lambda: os.getenv("MONGODB_PASSWORD", "gene_password"))
    mongodb_database: str = field(default_factory=lambda: os.getenv("MONGODB_DATABASE", "gene_db"))
    mongodb_test_host: str = field(default_factory=lambda: os.getenv("MONGODB_TEST_HOST", "mongodb_test"))
    
    # Redis settings
    redis_host: str = field(default_factory=lambda: os.getenv("REDIS_HOST", "redis"))
    redis_port: int = field(default_factory=lambda: int(os.getenv("REDIS_PORT", "6379")))
    
    @property
    def sqlalchemy_database_uri(self) -> str:
        """Get the SQLAlchemy database URI."""
        return f"mysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
    
    @property
    def mongodb_uri(self) -> str:
        """Get the MongoDB URI."""
        return os.getenv(
            "MONGODB_URI",
            f"mongodb://{self.mongodb_user}:{self.mongodb_password}@{self.mongodb_host}:{self.mongodb_port}/?authSource=admin",
        )


@dataclass
class AppConfig:
    """应用配置"""
    # FastAPI settings
    app_name: str = field(default_factory=lambda: os.getenv("APP_NAME", "oneseek-gene-backend"))
    environment: str = field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "True").lower() == "true")
    secret_key: str = field(default_factory=lambda: os.getenv("SECRET_KEY", "your-secret-key-here"))
    
    # Server settings
    host: str = field(default_factory=lambda: os.getenv("APP_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("APP_PORT", "5000")))
    
    # API settings
    api_title: str = "Gene Backend API"
    api_version: str = "1.0.0"
    openapi_version: str = "3.0.2"
    openapi_url_prefix: str = "/"
    openapi_swagger_ui_path: str = "/docs"
    openapi_swagger_ui_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"


@dataclass
class SecurityConfig:
    """安全配置"""
    # API Token settings
    api_token: str = field(default_factory=lambda: os.getenv("API_TOKEN", "your-api-token-here"))
    
    # JWT settings
    jwt_secret_key: str = field(default_factory=lambda: os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key-here"))
    jwt_algorithm: str = field(default_factory=lambda: os.getenv("JWT_ALGORITHM", "HS256"))
    jwt_access_token_expires: timedelta = field(default_factory=lambda: timedelta(days=1))
    jwt_access_token_expire_minutes: int = field(default_factory=lambda: int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")))
    jwt_refresh_token_expires: timedelta = field(default_factory=lambda: timedelta(days=30))
    
    # Admin user settings (for dashboard)
    admin_username: str = field(default_factory=lambda: os.getenv("ADMIN_USERNAME", "admin"))
    admin_password: str = field(default_factory=lambda: os.getenv("ADMIN_PASSWORD", "admin123"))
    admin_email: str = field(default_factory=lambda: os.getenv("ADMIN_EMAIL", "admin@oneseek.com"))


@dataclass
class ExternalServiceConfig:
    """外部服务配置"""
    # NCBI settings
    ncbi_email: str = field(default_factory=lambda: os.getenv("NCBI_EMAIL", ""))
    ncbi_api_key: str = field(default_factory=lambda: os.getenv("NCBI_API_KEY", ""))
    
    # Celery settings
    celery_broker_url: str = field(default_factory=lambda: os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"))
    celery_result_backend: str = field(default_factory=lambda: os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"))


@dataclass
class LoggingConfig:
    """日志配置"""
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    log_file: str = field(default_factory=lambda: os.getenv("LOG_FILE", "gene_backend.log"))
    log_dir: str = field(default_factory=lambda: os.getenv("LOG_DIR", "/app/logs"))
    log_format: str = field(default_factory=lambda: os.getenv(
        "LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ))
    log_date_format: str = field(default_factory=lambda: os.getenv("LOG_DATE_FORMAT", "%Y-%m-%d %H:%M:%S"))


@dataclass
class BusinessConfig:
    """业务配置"""
    # Gene predict settings
    gene_predict_bp_range: int = field(default_factory=lambda: int(os.getenv("GENE_PREDICT_BP_RANGE", "2030")))


class ConfigValidator(ABC):
    """配置验证器基类"""
    
    @abstractmethod
    def validate(self, config: Any) -> bool:
        """验证配置"""
        pass


class DatabaseConfigValidator(ConfigValidator):
    """数据库配置验证器"""
    
    def validate(self, config: DatabaseConfig) -> bool:
        """验证数据库配置"""
        if not config.mysql_host or not config.mysql_user:
            raise ValueError("MySQL host and user must be provided")
        if not config.mongodb_host or not config.mongodb_user:
            raise ValueError("MongoDB host and user must be provided")
        if config.mysql_port <= 0 or config.mongodb_port <= 0:
            raise ValueError("Database ports must be positive integers")
        return True


class SecurityConfigValidator(ConfigValidator):
    """安全配置验证器"""
    
    def validate(self, config: SecurityConfig) -> bool:
        """验证安全配置"""
        # 在生产环境中严格验证API token
        from os import getenv
        environment = getenv("ENVIRONMENT", "development")
        require_api_token = getenv("REQUIRE_API_TOKEN", "true").lower() == "true"
        
        if environment == "production" and require_api_token:
            if not config.api_token or config.api_token == "your-api-token-here":
                raise ValueError("API token must be set and not use default value in production")
        
        if len(config.jwt_secret_key) < 8:  # 放宽开发环境要求
            raise ValueError("JWT secret key must be at least 8 characters long")
        return True


class Settings:
    """统一设置管理器"""
    
    def __init__(self, validate: bool = True):
        self.database = DatabaseConfig()
        self.app = AppConfig()
        self.security = SecurityConfig()
        self.external = ExternalServiceConfig()
        self.logging = LoggingConfig()
        self.business = BusinessConfig()
        
        # 在开发环境中可以跳过验证
        if validate and self.app.environment != "development":
            self.validate_all()
        elif validate and self.app.environment == "development":
            try:
                self.validate_all()
            except ValueError as e:
                print(f"Development environment config warning: {e}")
                print("Continuing with relaxed validation for development...")
    
    def validate_all(self) -> None:
        """验证所有配置"""
        validators = [
            (self.database, DatabaseConfigValidator()),
            (self.security, SecurityConfigValidator()),
        ]
        
        for config, validator in validators:
            try:
                validator.validate(config)
            except ValueError as e:
                print(f"Configuration validation error: {e}")
                # 在生产环境中应该抛出异常，开发环境中可以只打印警告
                if self.app.environment == "production":
                    raise
    
    def get_fastapi_config(self) -> Dict[str, Any]:
        """获取FastAPI配置字典"""
        return {
            "DEBUG": self.app.debug,
            "SECRET_KEY": self.app.secret_key,
            "API_TOKEN": self.security.api_token,
            "APP_NAME": self.app.app_name,
            "ENVIRONMENT": self.app.environment,
        }
    
    def get_celery_config(self) -> Dict[str, Any]:
        """获取Celery配置字典"""
        return {
            "broker_url": self.external.celery_broker_url,
            "result_backend": self.external.celery_result_backend,
            "task_serializer": "json",
            "accept_content": ["json"],
            "result_serializer": "json",
            "timezone": "UTC",
            "enable_utc": True,
        }
    
    # 向后兼容的属性访问
    @property
    def API_TOKEN(self) -> str:
        return self.security.api_token
    
    @property
    def MONGODB_URI(self) -> str:
        return self.database.mongodb_uri
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return self.database.sqlalchemy_database_uri
    
    # Celery配置向后兼容
    @property
    def celery_broker_url(self) -> str:
        return self.external.celery_broker_url
    
    @property
    def celery_result_backend(self) -> str:
        return self.external.celery_result_backend
    
    @property
    def CELERY_BROKER_URL(self) -> str:
        return self.external.celery_broker_url
    
    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return self.external.celery_result_backend
    
    # 其他常用配置向后兼容
    @property
    def DEBUG(self) -> bool:
        return self.app.debug
    
    @property
    def SECRET_KEY(self) -> str:
        return self.app.secret_key
    
    @property
    def ENVIRONMENT(self) -> str:
        return self.app.environment
    
    @property
    def NCBI_EMAIL(self) -> str:
        return self.external.ncbi_email
    
    @property
    def NCBI_API_KEY(self) -> str:
        return self.external.ncbi_api_key
    
    # 日志配置向后兼容
    @property
    def LOG_LEVEL(self) -> str:
        return self.logging.log_level
    
    @property
    def LOG_FILE(self) -> str:
        return self.logging.log_file
    
    @property
    def LOG_DIR(self) -> str:
        return self.logging.log_dir
    
    @property
    def LOG_FORMAT(self) -> str:
        return self.logging.log_format
    
    @property
    def LOG_DATE_FORMAT(self) -> str:
        return self.logging.log_date_format
    
    # 业务配置向后兼容
    @property
    def GENE_PREDICT_BP_RANGE(self) -> int:
        return self.business.gene_predict_bp_range
    
    # 数据库配置向后兼容
    @property
    def MYSQL_HOST(self) -> str:
        return self.database.mysql_host
    
    @property
    def MYSQL_PORT(self) -> int:
        return self.database.mysql_port
    
    @property
    def MYSQL_USER(self) -> str:
        return self.database.mysql_user
    
    @property
    def MYSQL_PASSWORD(self) -> str:
        return self.database.mysql_password
    
    @property
    def MYSQL_DATABASE(self) -> str:
        return self.database.mysql_database
    
    @property
    def MONGODB_HOST(self) -> str:
        return self.database.mongodb_host
    
    @property
    def MONGODB_PORT(self) -> int:
        return self.database.mongodb_port
    
    @property
    def MONGODB_USER(self) -> str:
        return self.database.mongodb_user
    
    @property
    def MONGODB_PASSWORD(self) -> str:
        return self.database.mongodb_password
    
    @property
    def MONGODB_DATABASE(self) -> str:
        return self.database.mongodb_database
    
    @property
    def REDIS_HOST(self) -> str:
        return self.database.redis_host
    
    @property
    def REDIS_PORT(self) -> int:
        return self.database.redis_port
    
    # 应用配置向后兼容
    @property
    def APP_HOST(self) -> str:
        return self.app.host
    
    @property
    def APP_PORT(self) -> int:
        return self.app.port
    
    @property
    def APP_NAME(self) -> str:
        return self.app.app_name
    
    # 认证配置向后兼容
    @property
    def ADMIN_USERNAME(self) -> str:
        return self.security.admin_username
    
    @property
    def ADMIN_EMAIL(self) -> str:
        return self.security.admin_email
    
    @property
    def ADMIN_PASSWORD(self) -> str:
        return self.security.admin_password
    
    @property
    def JWT_SECRET_KEY(self) -> str:
        return self.security.jwt_secret_key
    
    @property
    def JWT_ALGORITHM(self) -> str:
        return self.security.jwt_algorithm
    
    @property
    def JWT_ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        return self.security.jwt_access_token_expire_minutes
    
    # 主机和端口配置向后兼容
    @property
    def HOST(self) -> str:
        return self.app.host
    
    @property  
    def PORT(self) -> int:
        return self.app.port


# 全局设置实例
settings = Settings()

# 兼容性别名
APP_NAME = settings.app.app_name
ENVIRONMENT = settings.app.environment
DEBUG = settings.app.debug
