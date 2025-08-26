# Use Python 3.10 base image for compatibility with rasa>=3.6.0
FROM mcr.microsoft.com/devcontainers/python:1-3.10-bullseye

# Install system dependencies for audio and GUI support
RUN apt-get update && apt-get install -y \
    # Audio dependencies for pyaudio and speech recognition
    portaudio19-dev \
    libasound2-dev \
    alsa-utils \
    pulseaudio \
    # GUI dependencies for tkinter (already included but ensure available)
    python3-tk \
    tk-dev \
    # Additional development tools
    git \
    curl \
    wget \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set up audio for containerized environment
RUN usermod -a -G audio vscode

# Upgrade pip to latest version
RUN pip install --upgrade pip

# Set working directory
WORKDIR /workspace

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Set environment variables for audio
ENV PULSE_USER=vscode
ENV PULSE_RUNTIME_PATH=/run/user/1000/pulse

# Create directories for user runtime
RUN mkdir -p /run/user/1000 && chown vscode:vscode /run/user/1000