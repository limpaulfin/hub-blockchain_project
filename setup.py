#!/usr/bin/env python3
"""
Hub Blockchain Project Setup
Dự án Tiểu Luận Cá Nhân - TS. Nguyễn Hoài Đức
Trường Đại học Ngân Hàng TP.HCM
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
def read_requirements():
    """Read requirements from requirements.txt"""
    requirements = []
    try:
        with open('requirements.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
    except FileNotFoundError:
        pass
    return requirements

setup(
    name="hub-blockchain",
    version="1.0.0",
    author="TS. Nguyễn Hoài Đức",
    author_email="",
    description="Blockchain Implementation for Supply Chain Management - Academic Research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hub-blockchain/blockchain-project",
    
    packages=find_packages(),
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    
    python_requires=">=3.8",
    
    install_requires=read_requirements(),
    
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'mypy>=1.0.0',
            'black>=22.0.0',
            'isort>=5.10.0',
        ],
        'visualization': [
            'matplotlib>=3.5.0',
            'networkx>=2.8.0',
        ],
        'web': [
            'flask>=2.2.0',
            'flask-cors>=3.0.10',
        ],
        'crypto': [
            'cryptography>=3.4.8',
        ],
    },
    
    entry_points={
        'console_scripts': [
            'hub-blockchain=main:main',
            'blockchain-demo=main:demo_mode',
            'blockchain-mine=main:mining_mode',
        ],
    },
    
    include_package_data=True,
    
    package_data={
        'core': ['*.json'],
        'config': ['*.json', '*.yaml'],
        'docs': ['*.md'],
    },
    
    keywords=[
        'blockchain',
        'cryptocurrency',
        'supply-chain',
        'distributed-systems',
        'cryptography',
        'peer-to-peer',
        'consensus',
        'proof-of-work',
        'proof-of-stake',
        'education',
        'research',
        'hub',
        'vietnam',
    ],
    
    project_urls={
        'Documentation': 'https://github.com/hub-blockchain/blockchain-project/docs',
        'Source': 'https://github.com/hub-blockchain/blockchain-project',
        'Tracker': 'https://github.com/hub-blockchain/blockchain-project/issues',
    },
) 