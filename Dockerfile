FROM python:3.12-slim
LABEL authors="albz"

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install -r requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "/app/gitlab_downloader/__init__.py"]
