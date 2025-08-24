# Production-ready container
FROM python:3.12-slim


ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1 \
PIP_NO_CACHE_DIR=1


WORKDIR /app


# Install deps first for layer caching
COPY requirements.txt .
RUN pip install -r requirements.txt


# Copy app
COPY . .


EXPOSE 8000


# Use gunicorn for prod
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000", "--workers", "2", "--threads", "4"]
