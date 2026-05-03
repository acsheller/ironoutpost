FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /workspace

# ---- System deps ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    git bash curl vim less procps \
    libsdl2-2.0-0 libglib2.0-0 libgl1 \
    libx11-6 libxext6 libxrender1 libsm6 libice6 \
    && rm -rf /var/lib/apt/lists/*

# ---- Build args for UID/GID ----
ARG USERNAME=dev
ARG MY_UID=1000
ARG MY_GID=1000

# ---- Create user ----
RUN groupadd -g ${MY_GID} ${USERNAME} \
    && useradd -m -u ${MY_UID} -g ${MY_GID} -s /bin/bash ${USERNAME}

# ---- Python deps ----
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt

# ---- Switch to non-root user ----
USER ${USERNAME}

CMD ["sleep", "infinity"]