from setuptools import setup, find_packages

setup(
    name="gitlab_projects_downloader",
    version="0.1.0",
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
            'gitlab-exporter=gitlab_projects_downloader.__init__:main',
        ],
    },
    author="Alberto Barrago(alBz)",
    author_email="alberto.barrago@gmail.com",
    description="A simple service for download from gitlab your projects in tgz",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AlbertoBarrago/gitlab_projects_exporter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
