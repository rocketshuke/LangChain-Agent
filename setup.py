"""Setup script for LangChain Agent project."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = []
    for line in fh:
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("---"):
            # Strip comments at end of line
            if "#" in line:
                line = line.split("#")[0].strip()
            if line:
                requirements.append(line)

setup(
    name="langchain-agent",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An intelligent agent system powered by LangChain with knowledge base management, "
                "multi-tool support, and web UI.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/langchain-agent",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "langchain-agent=app_server:app",
        ],
    },
)
