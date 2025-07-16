# Audio Transcript Service

This project is a speech-to-text service powered by OpenAI's Whisper model, running locally via Docker. It provides an API for transcribing audio files to text.

## Features
- Local deployment (no cloud required)
- Uses OpenAI Whisper for high-quality transcription
- Simple API interface

## Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation & Usage
1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd audio_transcript
   ```
2. Start the service:
   ```bash
   docker-compose up
   ```
   This will build and start both the backend and frontend containers.

## API Usage
Once running, access the service through the provided frontend interface ([http://localhost:8501](http://localhost:8501)). Direct API usage is not required for typical users.

## Project Structure
- `backend/` - Python backend service (Whisper model)
- `frontend/` - Optional frontend interface
- `docker-compose.yml` - Multi-container orchestration

## Stopping the Service
To stop the service, press `Ctrl+C` in the terminal or run:
```bash
docker-compose down
```

## License
MIT
