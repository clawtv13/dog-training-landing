FROM n8nio/n8n:latest

USER root

# Install Python, ffmpeg, and required tools
RUN apk add --no-cache \
    python3 \
    py3-pip \
    ffmpeg \
    ffmpeg-libs

# Install Python packages
RUN pip3 install --no-cache-dir \
    openai \
    anthropic \
    requests

USER node

# Start n8n
CMD ["n8n"]
