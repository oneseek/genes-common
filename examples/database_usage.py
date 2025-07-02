#!/usr/bin/env python3
"""
示例：如何使用 genes-common 数据库客户端
"""

from genes_common import (
    get_mongo_client, get_mongo_db,
    get_redis_client,
    get_mysql_engine, get_mysql_session, get_mysql_connection,
    close_connections,
    settings
)


def mongodb_example():
    """MongoDB 使用示例"""
    print("=== MongoDB Example ===")
    try:
        # 获取 MongoDB 客户端和数据库
        client = get_mongo_client()
        db = get_mongo_db()
        
        # 使用示例
        collection = db.test_collection
        
        # 插入文档
        result = collection.insert_one({"name": "test", "value": 123})
        print(f"Inserted document with ID: {result.inserted_id}")
        
        # 查询文档
        doc = collection.find_one({"name": "test"})
        print(f"Found document: {doc}")
        
        # 删除测试文档
        collection.delete_one({"name": "test"})
        print("Test document deleted")
        
    except Exception as e:
        print(f"MongoDB error: {e}")


def redis_example():
    """Redis 使用示例"""
    print("\n=== Redis Example ===")
    try:
        # 获取 Redis 客户端
        redis_client = get_redis_client()
        
        # 设置键值
        redis_client.set("test_key", "test_value", ex=60)  # 60秒过期
        print("Set test_key = test_value")
        
        # 获取值
        value = redis_client.get("test_key")
        print(f"Got test_key = {value}")
        
        # 删除键
        redis_client.delete("test_key")
        print("Deleted test_key")
        
    except Exception as e:
        print(f"Redis error: {e}")


def mysql_example():
    """MySQL 使用示例"""
    print("\n=== MySQL Example ===")
    try:
        # 方法1: 使用 SQLAlchemy Engine (推荐用于原生SQL)
        engine = get_mysql_engine()
        with engine.connect() as connection:
            result = connection.execute("SELECT 1 as test_value")
            row = result.fetchone()
            print(f"Engine query result: {row}")
        
        # 方法2: 使用 SQLAlchemy Session (推荐用于ORM)
        session = get_mysql_session()
        try:
            result = session.execute("SELECT 2 as test_value")
            row = result.fetchone()
            print(f"Session query result: {row}")
        finally:
            session.close()
        
        # 方法3: 使用原生连接 (用于特殊需求)
        with get_mysql_connection() as connection:
            result = connection.execute("SELECT 3 as test_value")
            row = result.fetchone()
            print(f"Raw connection query result: {row}")
            
    except Exception as e:
        print(f"MySQL error: {e}")


def configuration_example():
    """配置示例"""
    print("\n=== Configuration Example ===")
    print(f"MongoDB URI: {settings.MONGODB_URI}")
    print(f"MySQL URI: {settings.SQLALCHEMY_DATABASE_URI}")
    print(f"Redis: {settings.database.redis_host}:{settings.database.redis_port}")
    print(f"Environment: {settings.ENVIRONMENT}")


def main():
    """主函数"""
    print("Genes Common Database Clients Usage Examples")
    print("=" * 50)
    
    # 显示配置
    configuration_example()
    
    # 注意：以下示例需要实际的数据库连接才能运行
    # 在生产环境中取消注释以下行：
    
    # mongodb_example()
    # redis_example()
    # mysql_example()
    
    print("\n=== Connection Management ===")
    print("Don't forget to close connections when shutting down:")
    print("close_connections()")
    
    # 实际关闭连接
    close_connections()
    print("All connections closed.")


if __name__ == "__main__":
    main() 