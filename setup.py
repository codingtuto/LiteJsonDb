from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="LiteJsonDb",
    version="3.4.5",
    author="Coding Team",
    author_email="codingteamgroup@gmail.com",
    description="A lightweight JSON-based database system. It's designed for simplicity and ease of use.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/codingtuto/LiteJsonDb/",
    packages=["LiteJsonDb"], 
    python_requires=">=3.7",
    install_requires=[
        "cryptography",  
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Setuptools Plugin",
        "Environment :: Console",
    ],
)
