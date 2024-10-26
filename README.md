# gitlab-downloader 
[![Pylint and Deploy to PyPI](https://github.com/AlbertoBarrago/gitlab_downloader/actions/workflows/pylint.yml/badge.svg)](https://github.com/AlbertoBarrago/gitlab_downloader/actions/workflows/pylint.yml)
[![PyPI](https://img.shields.io/pypi/v/gitlab-projects-downloader?color=26272B&labelColor=090422)](https://pypi.org/project/gitlab-projects-downloader/)


### Motivation
Every day someone ask me to export something from X and import into Y  from gitlab; so...

## ENV 
```dotenv
GITLAB_URL=""
ACCESS_TOKEN=""
EXPORT_FOLDER="./gitlab_exports"
```

## Installation
You can install the package via `PyPi`:

```bash
pip install gitlab-projects-downloader
```

## Docker 
```bash 
 docker run --rm -it ghcr.io/albertobarrago/gitlab-downloader-ghcr:latest
```

Enjoy 🚀 