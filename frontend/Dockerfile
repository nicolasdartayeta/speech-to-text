FROM python:3.13

# Set the working directory inside the container
WORKDIR /src

# Copy the requirements file and install dependencies
# We do this separately to leverage Docker's layer caching.
# If requirements.txt doesn't change, this layer won't be rebuilt.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the frontend application code
COPY ./src .

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit app
# --server.address 0.0.0.0 is crucial to make it accessible from outside the container
CMD ["streamlit", "run", "frontend.py", "--server.port", "8501", "--server.address", "0.0.0.0"]