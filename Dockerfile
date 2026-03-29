FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean

COPY . /app

ENV PYTHONPATH=/app:/app/src

EXPOSE 8000

# CMD ["python3", "app.py"]
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]