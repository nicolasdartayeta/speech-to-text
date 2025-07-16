FROM python:3.13

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY .env .

# Set the working directory inside the container
WORKDIR /src

# Copy the requirements file and install dependencies
# We do this separately to leverage Docker's layer caching.
# If requirements.txt doesn't change, this layer won't be rebuilt.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

# Command to run the FastAPI app using a production-grade server
# We expose port 8000 inside the container
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "backend:app"]