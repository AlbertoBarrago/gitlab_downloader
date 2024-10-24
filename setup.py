"""Setup module"""
from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="gitlab_projects_downloader",
    version="0.4.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "python-dotenv",
        "pylint",
        "astroid",
        "certifi",
        "charset-normalizer",
        "dill",
        "isort",
        "mccabe",
        "tomlkit",
        "urllib3"
    ],
    entry_points={
        'console_scripts': [
            'gitlab_downloader=gitlab_downloader.__init__:main',
        ],
    },
    author="alBz",
    author_email="alberto.barrago@gmail.com",
    description="A simple service for downloading your projects from GitLab in tgz format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlbertoBarrago/gitlab_projects_exporter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.7',
)
