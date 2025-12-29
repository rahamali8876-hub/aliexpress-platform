# FROM python:3.12-slim

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# # ---- system dependencies ----
# RUN apt-get update && apt-get install -y \
#     gcc \
#     build-essential \
#     libpq-dev \
#     netcat-openbsd \
#     librdkafka-dev \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# # ---- install uv ----
# RUN pip install --no-cache-dir uv

# # ---- copy dependency files first ----
# COPY pyproject.toml uv.lock ./

# # ---- install deps into system python ----
# RUN uv pip install --system --requirement uv.lock

# # ---- copy app code ----
# COPY . .

# # ---- entrypoint ----
# COPY docker/django/entrypoint.sh /usr/local/bin/entrypoint.sh
# RUN chmod +x /usr/local/bin/entrypoint.sh

# ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]




FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


# ---- system dependencies ----
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    librdkafka-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# 🚨 ENTRYPOINT MUST BE OUTSIDE /app (Codespaces noexec fix)
COPY docker/django/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
