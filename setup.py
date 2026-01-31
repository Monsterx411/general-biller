"""
Setup configuration for General Biller - Enterprise Bill Payment System
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="general-biller",
    version="2.0.0",
    author="Monsterx411",
    author_email="support@general-biller.com",
    description="Production-ready enterprise bill payment system for USA and Canada with bank-grade security",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Monsterx411/general-biller",
    project_urls={
        "Bug Tracker": "https://github.com/Monsterx411/general-biller/issues",
        "Documentation": "https://github.com/Monsterx411/general-biller/blob/main/API_DOCUMENTATION.md",
        "Source Code": "https://github.com/Monsterx411/general-biller",
        "Security": "https://github.com/Monsterx411/general-biller/blob/main/SECURITY.md",
    },
    packages=find_packages(exclude=["tests*", "frontend*", "mobile*", "desktop*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Framework :: Flask",
        "Environment :: Web Environment",
        "Natural Language :: English",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "python-dotenv>=0.20.0",
        "pydantic>=1.9.0",
        "cryptography>=38.0.0",
        "flask>=2.2.0",
        "gunicorn>=20.1.0",
        "flask-cors>=3.0.10",
        "SQLAlchemy>=2.0.0",
        "psycopg2-binary>=2.9.9",
        "PyJWT>=2.8.0",
        "marshmallow>=3.20.0",
        "alembic>=1.12.0",
        "flask-restx>=0.5.1",
        "python-dateutil>=2.8.2",
        "passlib>=1.7.4",
        "flask-limiter>=3.5.0",
        "pyotp>=2.9.0",
        "qrcode>=7.4.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "general-biller=main:main",
        ],
    },
    keywords=[
        "bill payment",
        "loan management",
        "payment processing",
        "banking",
        "fintech",
        "USA",
        "Canada",
        "ACH",
        "EFT",
        "credit card",
        "mortgage",
        "personal loan",
        "auto loan",
        "enterprise",
        "security",
        "compliance",
        "PCI DSS",
        "GLBA",
        "PIPEDA",
    ],
    license="MIT",
    license_files=["LICENSE"],
)
