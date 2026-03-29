FROM n8nio/n8n:latest

USER root

# Install ffmpeg
RUN apk add --no-cache \
    ffmpeg \
    ffmpeg-libs

USER node

# Start n8n normally
CMD ["n8n"]
