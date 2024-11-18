FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    openslide-tools \
    libopenslide0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .