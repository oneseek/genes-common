from setuptools import setup, find_packages

setup(
    name="genes-common",
    version="1.0.0",
    description="Common modules for genes project",
    author="Fangzhen Fu",
    author_email="fangzhenfutao@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pymongo==4.13.2",
        "python-dotenv>=1.0.1",
        "redis>=5.0.1",
        "pymysql>=1.1.0",
        "sqlalchemy>=2.0.0",
        "oss2==2.17.0",  # Aliyun OSS SDK
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 